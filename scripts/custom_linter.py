#!/usr/bin/env python3
"""Minimal custom linter for scaffold consistency.

Checks:
1) Every TODO line includes an owner marker: [HUMAN], [AI], [AI->HUMAN]
2) Warn if EXAMPLE marker appears without REPLACE ME tag.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "README.md", ROOT / "METHOD.md", ROOT / "QUICKSTART.md", ROOT / "docs"]
OWNER_RE = re.compile(r"TODO:\s*\[(HUMAN|AI|AI->HUMAN)\]")

errors = []
warnings = []


def iter_files():
    for target in TARGETS:
        if target.is_file():
            yield target
        elif target.is_dir():
            for p in target.rglob("*.md"):
                yield p


for file_path in iter_files():
    for idx, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
        if re.search(r"^\s*[-*]\s*TODO:", line) and not OWNER_RE.search(line):
            errors.append(f"{file_path.relative_to(ROOT)}:{idx} TODO без owner-маркера")
        if "EXAMPLE" in line and "REPLACE ME" not in line:
            warnings.append(f"{file_path.relative_to(ROOT)}:{idx} EXAMPLE без пометки REPLACE ME")

if warnings:
    print("Warnings:")
    for w in warnings:
        print(f"  - {w}")

if errors:
    print("Errors:")
    for e in errors:
        print(f"  - {e}")
    sys.exit(1)

print("OK: scaffold lint checks passed")
