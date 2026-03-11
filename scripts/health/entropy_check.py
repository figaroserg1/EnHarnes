#!/usr/bin/env python3
"""entropy_check.py — Detect signs of project degradation (entropy).

Checks:
  1. Unreplaced examples — 'REPLACE ME' placeholders left in docs/
  2. Orphan scripts — scripts not referenced in Makefile or CI workflows
  3. Blank setpoints — empty target: values in control-loop-metrics.yaml
  4. Large Python files — src/ files exceeding 500-line soft limit
  5. Missing doc references — risk-policy.json docs pointing to missing files

Exit code:
  0 — no issues
  1 — issues found

Usage:
    python scripts/health/entropy_check.py
    or: make entropy
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def check_unreplaced_examples() -> int:
    """Find REPLACE ME placeholders in docs/."""
    print("\n-- Unreplaced examples in docs --")
    errors = 0
    docs_dir = ROOT / "docs"
    if not docs_dir.exists():
        return 0
    for md in docs_dir.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except OSError:
            continue
        if "REPLACE ME" in text:
            print(f"  PLACEHOLDER: {md.relative_to(ROOT)}")
            errors += 1
    return errors


def check_orphan_scripts() -> int:
    """Find scripts not referenced in Makefile or CI."""
    print("\n-- Scripts not referenced in Makefile or CI --")
    errors = 0

    # Gather reference text from Makefile and workflows
    ref_text = ""
    makefile = ROOT / "Makefile"
    if makefile.exists():
        ref_text += makefile.read_text(encoding="utf-8")
    workflows_dir = ROOT / ".github" / "workflows"
    if workflows_dir.exists():
        for wf in workflows_dir.glob("*.yml"):
            ref_text += wf.read_text(encoding="utf-8")
        for wf in workflows_dir.glob("*.yaml"):
            ref_text += wf.read_text(encoding="utf-8")

    # Check .sh and .py scripts at top level of scripts/
    scripts_dir = ROOT / "scripts"
    if not scripts_dir.exists():
        return 0
    for script in scripts_dir.rglob("*"):
        if script.is_file() and script.suffix in (".sh", ".py", ".cmd"):
            name = script.name
            if name not in ref_text:
                print(f"  ORPHAN: {script.relative_to(ROOT)}")
                errors += 1
    return errors


def check_blank_setpoints() -> int:
    """Find blank target: values in control-loop-metrics.yaml."""
    print("\n-- Blank setpoints in policies/control-loop-metrics.yaml --")
    metrics_path = ROOT / "policies" / "control-loop-metrics.yaml"
    if not metrics_path.exists():
        return 0
    text = metrics_path.read_text(encoding="utf-8")
    blank_targets = re.findall(r"target:\s*$", text, re.MULTILINE)
    if blank_targets:
        print(f"  WARNING: {len(blank_targets)} setpoint target(s) are empty")
        return 1
    return 0


def check_large_files() -> int:
    """Find Python files in src/ exceeding 500 lines."""
    print("\n-- Python files over 500 lines (soft limit) --")
    errors = 0
    src_dir = ROOT / "src"
    if not src_dir.exists():
        return 0
    for py_file in src_dir.rglob("*.py"):
        try:
            lines = len(py_file.read_text(encoding="utf-8").splitlines())
        except OSError:
            continue
        if lines > 500:
            print(f"  LARGE FILE ({lines} lines): {py_file.relative_to(ROOT)}")
            errors += 1
    return errors


def check_missing_doc_refs() -> int:
    """Check risk-policy.json doc references resolve to real files."""
    print("\n-- Checking risk-policy.json doc references --")
    policy_path = ROOT / "policies" / "risk-policy.json"
    if not policy_path.exists():
        return 0
    try:
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print("  [WARN] Could not parse risk-policy.json")
        return 1

    missing = []
    for rule in policy.get("docsDriftRules", []):
        for doc in rule.get("docs", []):
            if not (ROOT / doc).exists():
                missing.append(doc)

    if missing:
        print("  MISSING DOCS referenced in risk-policy.json:")
        for m in missing:
            print(f"    {m}")
        return 1
    else:
        print("  All doc references resolve.")
        return 0


def main() -> int:
    print("=== Entropy Check ===")
    errors = 0
    errors += check_unreplaced_examples()
    errors += check_orphan_scripts()
    errors += check_blank_setpoints()
    errors += check_large_files()
    errors += check_missing_doc_refs()

    print()
    if errors > 0:
        print(f"Entropy check found {errors} issue(s). Review above.")
        return 1
    else:
        print("OK: no entropy issues found.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
