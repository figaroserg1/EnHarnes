#!/usr/bin/env python3
"""doc_health_check.py — Documentation health checker.

Runs 3 checks:
  1. Stale verification headers — docs with 'Verified: YYYY-MM-DD' older than 30 days
  2. Broken internal links — markdown [text](path) pointing to missing files
  3. Sparse index files — auto-discovers all index.md under docs/

Note: doc_linter.py and check_doc_drift.py run separately via `make lint`.

Exit code:
  0 — docs are healthy
  1 — issues found

Usage:
    python .claude/skills/harness.linters/scripts/doc-health/doc_health_check.py
    or: make doc-health
"""

import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
DOCS_DIR = ROOT / "docs"

VERIFIED_RE = re.compile(r"Verified:\s*(\d{4}-\d{2}-\d{2})")
LINK_RE = re.compile(r"\[.*?\]\((?!http)([^)]+)\)")
# Backtick paths: `path/to/file.ext` — must contain / and a file extension
BACKTICK_PATH_RE = re.compile(r"`([^`]*?/[^`]*?\.\w+)`")


def check_stale_headers() -> int:
    """Find docs with verification headers older than 30 days."""
    print("\n-- Stale verification headers --")
    issues = 0
    cutoff = datetime.now() - timedelta(days=30)
    cutoff_str = cutoff.strftime("%Y-%m-%d")

    for md in DOCS_DIR.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        match = VERIFIED_RE.search(text)
        if match and match.group(1) < cutoff_str:
            print(f"  STALE ({match.group(1)}): {md.relative_to(ROOT)}")
            issues += 1

    return issues


def check_broken_links() -> int:
    """Find broken internal links and backtick paths in markdown files."""
    print("\n-- Broken internal references --")
    issues = 0

    # Scan docs/ and root-level markdown (AGENTS.md, ARCHITECTURE.md, etc.)
    md_files = list(DOCS_DIR.rglob("*.md")) if DOCS_DIR.exists() else []
    md_files.extend(ROOT.glob("*.md"))

    for md in md_files:
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue

        # Check markdown links: [text](path)
        for match in LINK_RE.finditer(text):
            ref = match.group(1).split("#")[0]
            if not ref:
                continue
            if not (ROOT / ref).exists() and not (md.parent / ref).exists():
                print(f"  BROKEN: {md.relative_to(ROOT)} -> {ref}")
                issues += 1

        # Check backtick paths: `path/to/file.ext`
        for match in BACKTICK_PATH_RE.finditer(text):
            ref = match.group(1)
            # Skip patterns, commands, templates, and slash-commands
            if any(c in ref for c in ("*", "<", ">", " ")):
                continue
            if ref.startswith("/") or ref.startswith("python"):
                continue
            if not (ROOT / ref).exists():
                print(
                    f"  BROKEN: {md.relative_to(ROOT)} -> {ref}. "
                    f"Fix: update the path or remove the reference."
                )
                issues += 1

    return issues


def check_sparse_indexes() -> int:
    """Check that index.md files have at least 5 lines."""
    print("\n-- Sparse index files --")
    issues = 0
    index_paths = list(DOCS_DIR.rglob("index.md")) if DOCS_DIR.exists() else []
    for idx in index_paths:
        if idx.exists():
            lines = len(idx.read_text(encoding="utf-8").splitlines())
            if lines < 5:
                print(f"  SPARSE: {idx.relative_to(ROOT)} ({lines} lines)")
                issues += 1

    return issues


def main() -> int:
    print("=== Doc Health Check ===")
    issues = 0
    issues += check_stale_headers()
    issues += check_broken_links()
    issues += check_sparse_indexes()

    print()
    if issues > 0:
        print(f"Doc gardener found {issues} area(s) needing attention.")
        return 1
    else:
        print("OK: docs are healthy.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
