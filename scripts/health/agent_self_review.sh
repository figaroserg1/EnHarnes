#!/usr/bin/env bash
# =============================================================================
# agent_self_review.sh — Предварительная проверка перед открытием PR
# =============================================================================
#
# ЧТО ДЕЛАЕТ:
#   Последовательно выполняет 5 проверок, эквивалентных тому, что запускает CI:
#     1. Статические проверки (make check) — линтинг документации и исходного кода
#     2. Структурные тесты (make structural) — проверка зависимостей между слоями
#     3. Doc-drift (check_doc_drift.py) — все ссылки в risk-policy.json ведут
#        на существующие файлы
#     4. Watch-path напоминания — если изменённые файлы попадают под watch-пути
#        из risk-policy.json, скрипт подскажет какие доки нужно перепроверить
#     5. Entropy spot-check — поиск забытых плейсхолдеров, orphan-скриптов,
#        пустых setpoints
#
# ЗАЧЕМ НУЖЕН:
#   Агент (или человек) запускает этот скрипт локально перед тем как открыть PR.
#   Это позволяет поймать проблемы до CI и не тратить время на цикл
#   push → CI fail → fix → push. Все 5 шагов — те же самые, что проверяет CI.
#
# ИСПОЛЬЗОВАНИЕ:
#   bash scripts/agent_self_review.sh
#
# КОД ВОЗВРАТА:
#   0 — все проверки пройдены, можно открывать PR
#   1 — есть ошибки, нужно исправить перед PR
# =============================================================================
set -euo pipefail

echo "=== Agent Self-Review ==="
echo "Run this before opening a PR. Equivalent to what CI checks."
FAILURES=0

# 1. Static checks (doc lint + source guard)
echo ""
echo "-- Step 1/5: Static checks --"
make check || FAILURES=$((FAILURES + 1))

# 2. Structural tests (layer dependencies)
echo ""
echo "-- Step 2/5: Structural tests --"
make structural || FAILURES=$((FAILURES + 1))

# 3. Doc-drift check (risk-policy.json references)
echo ""
echo "-- Step 3/5: Doc-drift check --"
python3 scripts/health/check_doc_drift.py || FAILURES=$((FAILURES + 1))

# 4. Verify changed files match risk-policy watch paths
echo ""
echo "-- Step 4/5: Changed-file doc reminders --"
if [ -f policies/risk-policy.json ]; then
  python3 - <<'PYEOF'
import json, subprocess, sys
from pathlib import Path

policy = json.loads(Path("policies/risk-policy.json").read_text())
try:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only"],
        capture_output=True, text=True
    )
    staged = set(result.stdout.strip().splitlines()) if result.returncode == 0 else set()
    result2 = subprocess.run(
        ["git", "diff", "--name-only"],
        capture_output=True, text=True
    )
    unstaged = set(result2.stdout.strip().splitlines()) if result2.returncode == 0 else set()
    changed = staged | unstaged
except FileNotFoundError:
    changed = set()

if not changed:
    print("  No changed files detected. Skipping watch-path check.")
    sys.exit(0)

reminders = []
for rule in policy.get("docsDriftRules", []):
    watch = rule.get("watch", "")
    docs = rule.get("docs", [])
    touched = [f for f in changed if f.startswith(watch)]
    if touched:
        for doc in docs:
            reminders.append(f"  VERIFY: {doc} (you changed files in '{watch}')")

if reminders:
    print("  Docs you should verify before PR:")
    for r in reminders:
        print(r)
else:
    print("  No watch-path matches. No extra docs to verify.")
PYEOF
fi

# 5. Quick entropy spot-check
echo ""
echo "-- Step 5/5: Entropy spot-check --"
if [ -f scripts/health/entropy-check.sh ]; then
  bash scripts/health/entropy-check.sh || echo "  [WARN] Entropy issues found (non-blocking for PR)."
fi

echo ""
echo "================================"
if [ "$FAILURES" -gt 0 ]; then
  echo "FAIL: $FAILURES check(s) failed. Fix before opening PR."
  exit 1
else
  echo "PASS: all self-review checks passed. Ready for PR."
fi
