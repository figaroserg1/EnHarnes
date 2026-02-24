#!/usr/bin/env bash
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
python3 scripts/check_doc_drift.py || FAILURES=$((FAILURES + 1))

# 4. Verify changed files match risk-policy watch paths
echo ""
echo "-- Step 4/5: Changed-file doc reminders --"
if [ -f risk-policy.json ]; then
  python3 - <<'PYEOF'
import json, subprocess, sys
from pathlib import Path

policy = json.loads(Path("risk-policy.json").read_text())
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
if [ -f scripts/entropy-check.sh ]; then
  bash scripts/entropy-check.sh || echo "  [WARN] Entropy issues found (non-blocking for PR)."
fi

echo ""
echo "================================"
if [ "$FAILURES" -gt 0 ]; then
  echo "FAIL: $FAILURES check(s) failed. Fix before opening PR."
  exit 1
else
  echo "PASS: all self-review checks passed. Ready for PR."
fi
