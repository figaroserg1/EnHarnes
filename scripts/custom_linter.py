#!/usr/bin/env python3
"""Markdown and naming convention linter.

Checks:
1) Every TODO: has owner marker [HUMAN|AI|AI->HUMAN].
2) Every EXAMPLE includes '(REPLACE ME)'.
3) File naming conventions: kebab-case for src/ files.
4) Layer directory names match ARCHITECTURE.md.
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
OWNER_RE = re.compile(r"TODO:\s*\[(HUMAN|AI|AI->HUMAN)\]")
KEBAB_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*\.[a-z]+$")
LAYER_DIRS = {"Types", "Config", "Repo", "Service", "Runtime", "UI", "Providers"}

errors: list[str] = []
warnings: list[str] = []

# --- Markdown checks ---
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

# --- Naming convention checks (src/ only) ---
src_dir = ROOT / "src"
if src_dir.is_dir():
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

# --- Output ---
for w in warnings:
    print(f"  [WARN] {w}")

if errors:
    print("Documentation lint errors:")
    for err in errors:
        print(f"  [ERROR] {err}")
    sys.exit(1)

if warnings:
    print(f"OK: {len(warnings)} warning(s), no blocking errors.")
else:
    print("OK: all lint checks passed.")
