#!/usr/bin/env bash
set -euo pipefail

echo "=== Agent Self-Review ==="

# 1. Static checks
echo ""
echo "-- Static checks --"
make check

# 2. Structural tests
echo ""
echo "-- Structural tests --"
make structural

# 3. Doc drift check: verify risk-policy.json references are still valid
echo ""
echo "-- Doc drift (risk-policy.json) --"
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
    print("WARN: docs listed in risk-policy.json are missing — review them:")
    for m in missing:
        print(f"  {m}")
else:
    print("OK: all doc references resolve.")
EOF
fi

echo ""
echo "=== Self-review complete. ==="
