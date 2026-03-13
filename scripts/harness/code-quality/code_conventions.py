#!/usr/bin/env python3
"""Source code quality checks on src/ files.

Reads layer names and file size limits from policies/architecture.yaml.

Checks (per docs/harness/GOLDEN_PRINCIPLES.md):
  Rule 4 — No bare print() statements in production src/ code.
  Rule 5 — File size: warn at soft limit, hard error at hard limit.
  Naming — Files in src/ must be kebab-case.
  Naming — Subdirectories in src/ must match recognized layer names.

Runs as part of `make check`.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

PRINT_RE = re.compile(r"^\s*print\(")
KEBAB_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*\.[a-z]+$")


def _load_architecture() -> tuple[set[str], int, int]:
    """Load layers and file size limits from policies/architecture.yaml."""
    yaml_path = ROOT / "policies" / "architecture.yaml"
    layers: set[str] = set()
    soft, hard = 500, 1500  # defaults
    if not yaml_path.exists():
        return layers, soft, hard
    section = None
    for line in yaml_path.read_text(encoding="utf-8").splitlines():
        stripped = line.split("#")[0].strip()  # strip inline comments
        if not stripped:
            continue
        if stripped == "layers:":
            section = "layers"
            continue
        if stripped in ("allowed_imports:", "cross_cutting_modules:"):
            section = None
            continue
        if stripped == "file_size:":
            section = "file_size"
            continue
        if section == "layers" and stripped.startswith("- "):
            layers.add(stripped[2:].strip())
        elif section == "file_size":
            if stripped.startswith("soft_limit:"):
                soft = int(stripped.split(":")[1].strip())
            elif stripped.startswith("hard_limit:"):
                hard = int(stripped.split(":")[1].strip())
    return layers, soft, hard


LAYER_DIRS, SOFT_LIMIT, HARD_LIMIT = _load_architecture()

warnings: list[str] = []
errors: list[str] = []


def check_python_file(path: str) -> None:
    """Check print() and file size on a Python file."""
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    line_count = len(lines)

    if line_count > HARD_LIMIT:
        errors.append(
            f"{path}: {line_count} lines exceeds hard limit ({HARD_LIMIT}). "
            f"Fix: split into smaller modules. See Golden Principle 5."
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


def check_naming() -> None:
    """Check kebab-case filenames and layer directory names in src/."""
    src_dir = ROOT / "src"
    if not src_dir.is_dir():
        return

    for file_path in src_dir.rglob("*"):
        if ".git/" in str(file_path) or file_path.is_dir():
            continue
        name = file_path.name
        if name.startswith("__"):
            continue
        if not KEBAB_RE.match(name):
            rel = file_path.relative_to(ROOT)
            warnings.append(
                f"{rel}: filename '{name}' is not kebab-case. "
                f"Fix: rename to kebab-case (e.g., 'user-service.py'). "
                f"Convention: files=kebab-case, types=PascalCase, functions=camelCase."
            )

    # Check layer directory names
    for child in src_dir.iterdir():
        if child.is_dir() and not child.name.startswith("."):
            for subdir in child.iterdir():
                if (subdir.is_dir()
                        and subdir.name not in LAYER_DIRS
                        and not subdir.name.startswith(".")
                        and not subdir.name.startswith("__")):
                    warnings.append(
                        f"{subdir.relative_to(ROOT)}: directory '{subdir.name}' is not a recognized layer. "
                        f"Expected: {', '.join(sorted(LAYER_DIRS))}. "
                        f"Fix: use standard layer names or update ARCHITECTURE.md."
                    )


def walk_python() -> None:
    if not os.path.isdir("src"):
        print("[src-checks] src/ not found; skipping")
        return
    for root, _, files in os.walk("src"):
        for name in files:
            if name.endswith(".py"):
                check_python_file(os.path.join(root, name))


if __name__ == "__main__":
    walk_python()
    check_naming()

    for w in warnings:
        print(f"  [WARN] {w}")
    if errors:
        print("Source check violations:")
        for e in errors:
            print(f"  [ERROR] {e}")
        sys.exit(1)
    if warnings:
        print(f"[src-checks] {len(warnings)} warning(s). No blocking errors.")
    else:
        print("[src-checks] OK")
