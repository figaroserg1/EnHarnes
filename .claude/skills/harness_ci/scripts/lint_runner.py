#!/usr/bin/env python3
"""lint.py — Universal linter with auto-detection of project type.

Auto-detects project type and runs the appropriate linter:
  - Rust (Cargo.toml)    → cargo clippy -D warnings
  - Node.js (package.json) → npm run lint (if script exists)
  - Python (pyproject.toml/requirements.txt) → doc_linter + code_conventions

Override via HARNESS_LINT_CMD environment variable.

Usage:
    python scripts/harness/lint.py
    or: make check
    or: HARNESS_LINT_CMD="flake8 src/" make check
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
    override = os.environ.get("HARNESS_LINT_CMD", "").strip()
    if override:
        return subprocess.run(override, shell=True, cwd=ROOT).returncode

    # Rust
    if (ROOT / "Cargo.toml").exists() and shutil.which("cargo"):
        return run(["cargo", "clippy", "--all-targets", "--all-features", "--", "-D", "warnings"])

    # Node.js
    if (ROOT / "package.json").exists() and shutil.which("node") and shutil.which("npm"):
        try:
            pkg = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
            if pkg.get("scripts", {}).get("lint"):
                return run(["npm", "run", "-s", "lint"])
        except (json.JSONDecodeError, OSError):
            pass

    # Python
    if (ROOT / "pyproject.toml").exists() or (ROOT / "requirements.txt").exists():
        py = sys.executable
        S = ".claude/skills"
        rc1 = run([py, f"{S}/harness_linters/scripts/doc-health/doc_linter.py"])
        rc2 = run([py, f"{S}/harness_linters/scripts/code-quality/code_conventions.py"])
        return max(rc1, rc2)

    print("No default lint command detected.")
    print("Set HARNESS_LINT_CMD or customize scripts/harness/lint.py.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
