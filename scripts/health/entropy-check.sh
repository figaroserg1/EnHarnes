#!/usr/bin/env bash
# =============================================================================
# entropy-check.sh — Обнаружение признаков деградации проекта (энтропии)
# =============================================================================
#
# ЧТО ДЕЛАЕТ:
#   Ищет 5 типов «энтропии» — мелких проблем, которые накапливаются и
#   превращаются в технический долг:
#     1. Unreplaced examples — плейсхолдеры «REPLACE ME» в docs/, которые
#        забыли заменить на реальное содержание.
#     2. Orphan scripts — скрипты в scripts/*.sh, которые не упоминаются
#        ни в Makefile, ни в GitHub Actions. Значит, они никем не вызываются
#        и, вероятно, мертвый код.
#     3. Blank setpoints — пустые target: в evals/control-loop-metrics.yaml,
#        из-за чего метрики не сравниваются с целевыми значениями.
#     4. Large Python files — файлы в src/ > 500 строк, которые стоит
#        разбить на модули.
#     5. Missing doc references — ссылки из risk-policy.json, которые
#        ведут на несуществующие файлы.
#
# ЗАЧЕМ НУЖЕН:
#   Проект растёт, а мелкие проблемы остаются незамеченными. Этот скрипт —
#   «термометр энтропии»: если он находит много проблем, значит пора
#   провести cleanup-спринт. Запускается как часть agent_self_review.sh
#   (шаг 5/5, non-blocking) и может запускаться отдельно.
#
# ИСПОЛЬЗОВАНИЕ:
#   bash scripts/entropy-check.sh
#
# КОД ВОЗВРАТА:
#   0 — проблем не найдено
#   1 — найдены проблемы (подробности в stdout)
# =============================================================================
set -euo pipefail

echo "=== Entropy Check ==="
ERRORS=0

# 1. Find EXAMPLE (REPLACE ME) placeholders still present in docs
echo ""
echo "-- Unreplaced examples in docs --"
if grep -r "REPLACE ME" docs/ --include="*.md" -l 2>/dev/null; then
  ERRORS=$((ERRORS + 1))
fi

# 2. Find scripts not referenced in Makefile or CI
echo ""
echo "-- Scripts not referenced in Makefile or CI --"
for script in scripts/*.sh; do
  name=$(basename "$script")
  if ! grep -qr "$name" Makefile .github/workflows/ 2>/dev/null; then
    echo "  ORPHAN: $script"
    ERRORS=$((ERRORS + 1))
  fi
done

# 3. Find blank setpoint targets in control-loop-metrics.yaml
echo ""
echo "-- Blank setpoints in evals/control-loop-metrics.yaml --"
if [ -f evals/control-loop-metrics.yaml ]; then
  if grep -q "target: $" evals/control-loop-metrics.yaml 2>/dev/null; then
    echo "  WARNING: some setpoint targets are empty"
    ERRORS=$((ERRORS + 1))
  fi
fi

# 4. Find Python files exceeding soft file-size limit (500 lines)
echo ""
echo "-- Python files over 500 lines (soft limit) --"
find src/ -name "*.py" 2>/dev/null | while read -r f; do
  lines=$(wc -l < "$f")
  if [ "$lines" -gt 500 ]; then
    echo "  LARGE FILE ($lines lines): $f"
  fi
done

# 5. Check risk-policy.json doc references still resolve
echo ""
echo "-- Checking risk-policy.json doc references --"
if [ -f risk-policy.json ]; then
  python3 - <<'EOF'
import json, sys
from pathlib import Path

policy = json.loads(Path("risk-policy.json").read_text())
missing = []
for rule in policy.get("docsDriftRules", []):
    for doc in rule.get("docs", []):
        if not Path(doc).exists():
            missing.append(doc)
if missing:
    print("  MISSING DOCS referenced in risk-policy.json:")
    for m in missing:
        print(f"    {m}")
    sys.exit(1)
else:
    print("  All doc references resolve.")
EOF
fi

echo ""
if [ "$ERRORS" -gt 0 ]; then
  echo "Entropy check found $ERRORS issue(s). Review above."
  exit 1
else
  echo "OK: no entropy issues found."
fi
