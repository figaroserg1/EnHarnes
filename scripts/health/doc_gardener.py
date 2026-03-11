#!/usr/bin/env python3
"""doc_gardener.py — Documentation health checker.

Runs 5 checks:
  1. Stale verification headers — docs with 'Verified: YYYY-MM-DD' older than 30 days
  2. Broken internal links — markdown [text](path) pointing to missing files
  3. Sparse index files — index.md files with fewer than 5 lines
  4. Doc lint — custom_linter.py (TODO ownership, EXAMPLE placeholders)
  5. Doc drift — check_doc_drift.py (risk-policy.json references)

Exit code:
  0 — docs are healthy
  1 — issues found

Usage:
    python scripts/health/doc_gardener.py
    or: make gardener
"""

import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT / "docs"

VERIFIED_RE = re.compile(r"Verified:\s*(\d{4}-\d{2}-\d{2})")
LINK_RE = re.compile(r"\[.*?\]\((?!http)([^)]+)\)")


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
    """Find broken internal links in markdown files."""
    print("\n-- Broken internal references --")
    issues = 0

    for md in DOCS_DIR.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue

        for match in LINK_RE.finditer(text):
            ref = match.group(1).split("#")[0]
            if not ref:
                continue
            # Try relative to repo root, then relative to the file
            if not (ROOT / ref).exists() and not (md.parent / ref).exists():
                print(f"  BROKEN: {md.relative_to(ROOT)} -> {ref}")
                issues += 1

    return issues


def check_sparse_indexes() -> int:
    """Check that index.md files have at least 5 lines."""
    print("\n-- Sparse index files --")
    issues = 0
    index_paths = [
        DOCS_DIR / "design-docs" / "index.md",
        DOCS_DIR / "product-specs" / "index.md",
        DOCS_DIR / "references" / "index.md",
    ]
    for idx in index_paths:
        if idx.exists():
            lines = len(idx.read_text(encoding="utf-8").splitlines())
            if lines < 5:
                print(f"  SPARSE: {idx.relative_to(ROOT)} ({lines} lines)")
                issues += 1

    return issues


def run_doc_lint() -> int:
    """Run custom_linter.py."""
    print("\n-- Doc lint --")
    rc = subprocess.run(
        [sys.executable, "scripts/linters/custom_linter.py"], cwd=ROOT,
    ).returncode
    return 1 if rc != 0 else 0


def run_doc_drift() -> int:
    """Run check_doc_drift.py."""
    print("\n-- Doc drift references --")
    rc = subprocess.run(
        [sys.executable, "scripts/health/check_doc_drift.py"], cwd=ROOT,
    ).returncode
    return 1 if rc != 0 else 0


def main() -> int:
    print("=== Doc Gardener ===")
    issues = 0
    issues += check_stale_headers()
    issues += check_broken_links()
    issues += check_sparse_indexes()
    issues += run_doc_lint()
    issues += run_doc_drift()

    print()
    if issues > 0:
        print(f"Doc gardener found {issues} area(s) needing attention.")
        return 1
    else:
        print("OK: docs are healthy.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
