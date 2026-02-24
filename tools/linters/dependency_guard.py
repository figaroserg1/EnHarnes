#!/usr/bin/env python3
"""Python source guard: enforces Golden Principle mechanical rules on src/ Python files.

Checks (per docs/GOLDEN_PRINCIPLES.md):
  Rule 4 — No bare print() statements in production src/ code.
  Rule 5 — File size: warn at 500 lines, hard error at 1500 lines.

Runs as part of `make check`. Complements the AST structural tests in
tools/structural-tests/ which enforce layer dependency rules.
"""

import os
import re
import sys

PRINT_RE = re.compile(r"^\s*print\(")
SOFT_LIMIT = 500
HARD_LIMIT = 1500

warnings: list[str] = []
errors: list[str] = []


def check_file(path: str) -> None:
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    line_count = len(lines)
    if line_count > HARD_LIMIT:
        errors.append(
            f"{path}: {line_count} lines — exceeds hard limit ({HARD_LIMIT}). Split this file."
        )
    elif line_count > SOFT_LIMIT:
        warnings.append(
            f"{path}: {line_count} lines — exceeds soft limit ({SOFT_LIMIT}). Consider splitting."
        )

    for idx, line in enumerate(lines, start=1):
        if PRINT_RE.match(line):
            errors.append(
                f"{path}:{idx}: bare print() — use structured logging with service/env/trace_id/operation/result fields"
            )


def walk() -> None:
    if not os.path.isdir("src"):
        print("[source-guard] src/ not found; skipping")
        return
    for root, _, files in os.walk("src"):
        for name in files:
            if name.endswith(".py"):
                check_file(os.path.join(root, name))


if __name__ == "__main__":
    walk()
    for w in warnings:
        print(f"[WARN] {w}")
    if errors:
        print("Source guard violations:")
        for e in errors:
            print(f"  [ERROR] {e}")
        sys.exit(1)
    if warnings:
        print(f"[source-guard] {len(warnings)} warning(s). No blocking errors.")
    else:
        print("[source-guard] OK")
