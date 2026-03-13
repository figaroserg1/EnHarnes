#!/usr/bin/env python3
"""typecheck.py — Universal type checker with auto-detection of project type.

Auto-detects project type and runs the appropriate type checker:
  - Rust (Cargo.toml)    → cargo check
  - Node.js (package.json) → npm run typecheck (if script exists)
  - Python (pyproject.toml/requirements.txt) → pyright or mypy

Override via HARNESS_TYPECHECK_CMD environment variable.

Usage:
    python scripts/linters/typecheck.py
    or: make typecheck
    or: HARNESS_TYPECHECK_CMD="mypy src/" make typecheck
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def run(cmd: list[str], **kwargs) -> int:
    result = subprocess.run(cmd, cwd=ROOT, **kwargs)
    return result.returncode


def main() -> int:
    # Override
    override = os.environ.get("HARNESS_TYPECHECK_CMD", "").strip()
    if override:
        return subprocess.run(override, shell=True, cwd=ROOT).returncode

    # Rust
    if (ROOT / "Cargo.toml").exists() and shutil.which("cargo"):
        return run(["cargo", "check", "--quiet"])

    # Node.js
    if (ROOT / "package.json").exists() and shutil.which("node") and shutil.which("npm"):
        try:
            pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
            if pkg.get("scripts", {}).get("typecheck"):
                return run(["npm", "run", "-s", "typecheck"])
        except (json.JSONDecodeError, OSError):
            pass

    # Python
    if (ROOT / "pyproject.toml").exists() or (ROOT / "requirements.txt").exists():
        if shutil.which("pyright"):
            return run(["pyright"])
        if shutil.which("mypy"):
            return run(["mypy", "src/"])
        print("[typecheck] No type checker found (pyright/mypy). Skipping — install one to enable.")
        return 0

    print("No default typecheck command detected.")
    print("Set HARNESS_TYPECHECK_CMD or customize scripts/linters/typecheck.py.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
