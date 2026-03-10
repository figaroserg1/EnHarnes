#!/usr/bin/env python3
"""Python source guard: enforces Golden Principle mechanical rules on src/ Python files.

Checks (per docs/GOLDEN_PRINCIPLES.md):
  Rule 3 — No direct Repo imports from UI layer.
  Rule 4 — No bare print() statements in production src/ code.
  Rule 5 — File size: warn at 500 lines, hard error at 1500 lines.
  Rule 12 — Cross-cutting imports must go through Providers only.

Runs as part of `make check`. Complements the AST structural tests in
tools/structural-tests/ which enforce layer dependency rules.
"""

import os
import re
import sys

PRINT_RE = re.compile(r"^\s*print\(")
REPO_IMPORT_RE = re.compile(r"from\s+\S*Repo\b|import\s+\S*Repo\b")
CROSS_CUT_RE = re.compile(r"from\s+\S*(auth|logging|tracing|secrets|config_loader)\b", re.IGNORECASE)
PROVIDERS_IMPORT_RE = re.compile(r"from\s+\S*Providers\b|import\s+\S*Providers\b")
SOFT_LIMIT = 500
HARD_LIMIT = 1500

warnings: list[str] = []
errors: list[str] = []


def check_file(path: str) -> None:
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    line_count = len(lines)
    is_ui = os.sep + "UI" + os.sep in path or "/UI/" in path

    if line_count > HARD_LIMIT:
        errors.append(
            f"{path}: {line_count} lines exceeds hard limit ({HARD_LIMIT}). "
            f"Fix: split into smaller modules. See Golden Principle 5 in docs/GOLDEN_PRINCIPLES.md."
        )
    elif line_count > SOFT_LIMIT:
        warnings.append(
            f"{path}: {line_count} lines exceeds soft limit ({SOFT_LIMIT}). "
            f"Fix: consider extracting helpers. See Golden Principle 5."
        )

    for idx, line in enumerate(lines, start=1):
        if PRINT_RE.match(line):
            errors.append(
                f"{path}:{idx}: bare print() in production code. "
                f"Fix: replace with structured logging including service/env/trace_id/operation/result fields. "
                f"See Golden Principle 4."
            )

        # Rule 3: UI must not import Repo directly
        if is_ui and REPO_IMPORT_RE.search(line):
            errors.append(
                f"{path}:{idx}: UI layer imports Repo directly. "
                f"Fix: access data through Service or Runtime layer instead. "
                f"See Golden Principle 3."
            )

        # Rule 12: cross-cutting concerns must go through Providers
        if CROSS_CUT_RE.search(line) and not PROVIDERS_IMPORT_RE.search(line):
            if "/Providers/" not in path and os.sep + "Providers" + os.sep not in path:
                warnings.append(
                    f"{path}:{idx}: possible direct cross-cutting import (auth/logging/tracing/secrets). "
                    f"Fix: route through Providers/ abstraction layer. See Golden Principle 12."
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
