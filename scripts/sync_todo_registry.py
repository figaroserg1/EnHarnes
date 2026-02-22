#!/usr/bin/env python3
"""Minimal helper to count TODO markers across markdown files."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
owner_re = re.compile(r"TODO:\s*\[(HUMAN|AI|AI->HUMAN)\]")

counts = {"HUMAN": 0, "AI": 0, "AI->HUMAN": 0}
for p in root.rglob("*.md"):
    for line in p.read_text(encoding="utf-8").splitlines():
        m = owner_re.search(line)
        if m:
            counts[m.group(1)] += 1

print("TODO owners summary:")
for k, v in counts.items():
    print(f"- {k}: {v}")
