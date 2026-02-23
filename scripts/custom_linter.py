#!/usr/bin/env python3
"""Markdown linter for Phase 1 docs.

Checks:
1) Every line containing TODO: has owner marker [HUMAN|AI|AI->HUMAN].
2) Every line containing EXAMPLE must include '(REPLACE ME)'.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
OWNER_RE = re.compile(r"TODO:\s*\[(HUMAN|AI|AI->HUMAN)\]")

errors: list[str] = []

for file_path in ROOT.rglob("*.md"):
    if ".git/" in str(file_path):
        continue

    for idx, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
        if "TODO:" in line and not OWNER_RE.search(line):
            errors.append(f"{file_path.relative_to(ROOT)}:{idx} TODO without owner marker")
        if "EXAMPLE" in line and "REPLACE ME" not in line:
            errors.append(f"{file_path.relative_to(ROOT)}:{idx} EXAMPLE without 'REPLACE ME'")

if errors:
    print("Documentation lint errors:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)

print("OK: documentation lint checks passed")
