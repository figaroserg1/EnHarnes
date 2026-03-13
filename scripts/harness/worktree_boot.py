#!/usr/bin/env python3
"""worktree_boot.py — Create an isolated git worktree for an agent task.

Steps:
  1. Creates worktree at ../worktree_<task-name> on branch task/<task-name>
  2. Auto-detects project type (Python/Node/Rust) and installs dependencies
  3. Runs smoke check (make lint-todos or make lint)

Usage:
    python scripts/dev/worktree_boot.py <task-name>

Example:
    python scripts/dev/worktree_boot.py fix-auth-bug
    # Creates ../worktree_fix-auth-bug on branch task/fix-auth-bug

Cleanup:
    git worktree remove ../worktree_<task-name>
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None, check: bool = False) -> int:
    result = subprocess.run(cmd, cwd=cwd)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result.returncode


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: worktree_boot.py <task-name>")
        return 1

    task_name = sys.argv[1]
    repo_root = Path.cwd()
    worktree_dir = repo_root.parent / f"worktree_{task_name}"
    branch_name = f"task/{task_name}"

    print(f"=== Worktree Boot: {task_name} ===")

    # 1. Create worktree
    if worktree_dir.exists():
        print(f"Worktree {worktree_dir} already exists. Reusing.")
    else:
        print(f"Creating worktree at {worktree_dir} on branch {branch_name}...")
        run(["git", "worktree", "add", str(worktree_dir), "-b", branch_name], cwd=repo_root, check=True)

    # 2. Install dependencies (auto-detect runtime)
    print("\n-- Installing dependencies --")
    if (worktree_dir / "requirements.txt").exists():
        pip = shutil.which("pip") or "pip"
        rc = run([pip, "install", "-r", "requirements.txt"], cwd=worktree_dir)
        if rc != 0:
            run([pip, "install", "pytest"], cwd=worktree_dir)
    elif (worktree_dir / "package.json").exists():
        if shutil.which("bun"):
            run(["bun", "install"], cwd=worktree_dir)
        elif shutil.which("npm"):
            run(["npm", "install"], cwd=worktree_dir)
    elif (worktree_dir / "Cargo.toml").exists():
        run(["cargo", "build"], cwd=worktree_dir)
    else:
        print("No dependency file detected. Installing pytest for structural tests.")
        pip = shutil.which("pip") or "pip"
        run([pip, "install", "pytest"], cwd=worktree_dir)

    # 3. Run smoke check
    print("\n-- Running smoke check --")
    make = shutil.which("make")
    if make and (worktree_dir / "Makefile").exists():
        rc = run([make, "lint-todos"], cwd=worktree_dir)
        if rc != 0:
            run([make, "lint"], cwd=worktree_dir)
    else:
        print("[WARN] make not available or no Makefile. Skipping smoke check.")

    print(f"\n=== Worktree ready at {worktree_dir} (branch: {branch_name}) ===")
    print(f"To clean up: git worktree remove {worktree_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
