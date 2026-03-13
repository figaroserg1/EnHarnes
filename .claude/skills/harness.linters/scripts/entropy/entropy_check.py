#!/usr/bin/env python3
"""entropy_check.py — Detect signs of project degradation (entropy).

Checks:
  1. Orphan scripts — scripts not referenced in Makefile or CI workflows
  2. Blank setpoints — empty target: values in control-loop-metrics.yaml

Note: REPLACE ME placeholders checked by todo_linter.py,
      large files by src_checks.py, doc refs by check_doc_drift.py.

Exit code:
  0 — no issues
  1 — issues found

Usage:
    python scripts/health/entropy_check.py
    or: make check-entropy
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]


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


def main() -> int:
    print("=== Entropy Check ===")
    errors = 0
    errors += check_orphan_scripts()
    errors += check_blank_setpoints()

    print()
    if errors > 0:
        print(f"Entropy check found {errors} issue(s). Review above.")
        return 1
    else:
        print("OK: no entropy issues found.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
