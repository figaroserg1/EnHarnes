#!/usr/bin/env python3
"""Stop hook: auto-sync doc indexes if any .md files changed.

Runs after Claude finishes responding. Checks git diff for changed .md files.
If any found, runs sync_doc_indexes.py to keep index.md files current.

Lightweight — only triggers sync, not full gardening.
"""

import subprocess
import sys
from pathlib import Path


def get_changed_md_files() -> list[str]:
    """Get .md files changed since last commit (staged + unstaged)."""
    changed: list[str] = []
    for args in [["--name-only"], ["--cached", "--name-only"]]:
        result = subprocess.run(
            ["git", "diff"] + args,
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            for f in result.stdout.strip().splitlines():
                if f.endswith(".md") and f not in changed:
                    changed.append(f)
    # Also check untracked .md files
    result = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "*.md"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        for f in result.stdout.strip().splitlines():
            if f and f not in changed:
                changed.append(f)
    return changed


def main():
    changed_md = get_changed_md_files()
    if not changed_md:
        return

    # Check if any changed .md is in an indexed directory
    indexed_dirs = ("docs/design-docs/", "docs/product-specs/", "docs/references/")
    needs_sync = any(
        any(f.startswith(d) for d in indexed_dirs)
        for f in changed_md
    )

    if not needs_sync:
        return

    # Find sync script — try project's scripts/ first, then plugin's
    candidates = [
        Path("scripts/generators/sync_doc_indexes.py"),
    ]
    # Also try relative to this hook's location (plugin path)
    hook_dir = Path(__file__).resolve().parent
    plugin_script = hook_dir.parent / "scripts" / "generators" / "sync_doc_indexes.py"
    candidates.append(plugin_script)

    for script in candidates:
        if script.exists():
            result = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True, text=True,
            )
            if result.stdout.strip():
                # Only print if something actually changed
                for line in result.stdout.strip().splitlines():
                    if "Updated:" in line:
                        print(line)
            return


if __name__ == "__main__":
    main()
