#!/usr/bin/env python3
"""build_handbook.py — Generate a single project-handbook.md from key docs.

Concatenates core Phase 1 documents into dist/project-handbook.md with
section separators and source annotations. Useful for LLM context loading
or reading the entire project overview in one file.

Usage:
    python scripts/generators/build_handbook.py
    or: make build

Output:
    dist/project-handbook.md
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIST_DIR = ROOT / "dist"

SOURCES = [
    "README.md",
    "METHOD.md",
    "QUICKSTART.md",
    "ARCHITECTURE.md",
    "docs/design-docs/system-spec.md",
    "docs/design-docs/rules.md",
    "docs/design-docs/architecture.md",
]


def main() -> int:
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    out_file = DIST_DIR / "project-handbook.md"

    parts = [
        "# Project handbook (generated)\n",
        "_Generated from core Phase 1 docs._\n",
    ]

    for rel_path in SOURCES:
        full = ROOT / rel_path
        parts.append(f"\n---\n\n## Source: {rel_path}\n")
        if full.exists():
            parts.append(full.read_text(encoding="utf-8"))
        else:
            parts.append(f"_File not found: {rel_path}_\n")
        parts.append("")

    out_file.write_text("\n".join(parts), encoding="utf-8")
    print(f"Generated: {out_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
