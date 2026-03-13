#!/usr/bin/env python3
"""Documentation linter: checks TODO ownership and EXAMPLE placeholders.

Checks:
  1. TODO markers — every 'TODO:' in markdown must have owner:
     [HUMAN], [AI], or [AI->HUMAN].
  2. EXAMPLE placeholders — every 'EXAMPLE' block must contain
     '(REPLACE ME)' to indicate it's a template.

Runs as part of `make check` (via lint.py).
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[5]
OWNER_RE = re.compile(r"TODO:\s*\[(HUMAN|AI|AI->HUMAN)\]")

errors: list[str] = []

for file_path in ROOT.rglob("*.md"):
    if ".git/" in str(file_path):
        continue

    for idx, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
        if "TODO:" in line and not OWNER_RE.search(line):
            rel = file_path.relative_to(ROOT)
            errors.append(
                f"{rel}:{idx}: TODO without owner marker. "
                f"Fix: add [HUMAN], [AI], or [AI->HUMAN] after 'TODO:'. "
                f"Example: TODO: [AI] Implement feature X"
            )
        if "EXAMPLE" in line and "REPLACE ME" not in line:
            rel = file_path.relative_to(ROOT)
            errors.append(
                f"{rel}:{idx}: EXAMPLE without '(REPLACE ME)'. "
                f"Fix: add '(REPLACE ME)' to indicate this is a template placeholder."
            )

if errors:
    print("Documentation lint errors:")
    for err in errors:
        print(f"  [ERROR] {err}")
    sys.exit(1)
else:
    print("[doc-linter] OK: all checks passed.")
