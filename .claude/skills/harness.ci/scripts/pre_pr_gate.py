#!/usr/bin/env python3
"""pre_pr_gate.py — Pre-PR gate: runs 4 checks equivalent to CI.

Steps:
  1. Lint (make lint) — TODO linter + code conventions + structural
  2. Doc-drift (check_doc_drift.py) — risk-policy.json references
  3. Watch-path reminders — changed files matching risk-policy watch paths
  4. Entropy spot-check — orphan scripts, blank setpoints

Exit code:
  0 — all checks passed, ready for PR
  1 — failures found, fix before PR

Usage:
    python scripts/harness/pre_pr_gate.py
    or: make review
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def run_make(target: str) -> int:
    return subprocess.run(["make", target], cwd=ROOT).returncode


def check_watch_paths() -> None:
    policy_path = ROOT / "policies" / "risk-policy.json"
    if not policy_path.exists():
        print("  No risk-policy.json found. Skipping.")
        return

    policy = json.loads(policy_path.read_text(encoding="utf-8"))

    # Gather changed files from git
    changed: set[str] = set()
    for diff_args in [["--cached", "--name-only"], ["--name-only"]]:
        result = subprocess.run(
            ["git", "diff"] + diff_args,
            capture_output=True, text=True, cwd=ROOT,
        )
        if result.returncode == 0:
            changed.update(line for line in result.stdout.strip().splitlines() if line)

    if not changed:
        print("  No changed files detected. Skipping watch-path check.")
        return

    reminders = []
    for rule in policy.get("docsDriftRules", []):
        watch = rule.get("watch", "")
        docs = rule.get("docs", [])
        touched = [f for f in changed if f.startswith(watch)]
        if touched:
            for doc in docs:
                reminders.append(f"  VERIFY: {doc} (you changed files in '{watch}')")

    if reminders:
        print("  Docs you should verify before PR:")
        for r in reminders:
            print(r)
    else:
        print("  No watch-path matches. No extra docs to verify.")


def run_entropy() -> None:
    entropy_script = ROOT / ".claude" / "skills" / "harness.linters" / "scripts" / "entropy" / "entropy_check.py"
    if entropy_script.exists():
        result = subprocess.run([sys.executable, str(entropy_script)], cwd=ROOT)
        if result.returncode != 0:
            print("  [WARN] Entropy issues found (non-blocking for PR).")
    else:
        print("  [SKIP] entropy_check.py not found.")


def main() -> int:
    print("=== Pre-PR Gate ===")
    print("Run this before opening a PR. Equivalent to what CI checks.")
    failures = 0

    # 1. Lint (composite: lint-todos + lint-src + lint-structural)
    print("\n-- Step 1/4: Lint --")
    if run_make("lint") != 0:
        failures += 1

    # 2. Doc-drift
    print("\n-- Step 2/4: Doc-drift check --")
    rc = subprocess.run(
        [sys.executable, str(ROOT / ".claude/skills/harness.linters/scripts/doc-health/check_doc_drift.py")], cwd=ROOT,
    ).returncode
    if rc != 0:
        failures += 1

    # 3. Watch-path reminders
    print("\n-- Step 3/4: Changed-file doc reminders --")
    check_watch_paths()

    # 4. Entropy spot-check
    print("\n-- Step 4/4: Entropy spot-check --")
    run_entropy()

    print("\n================================")
    if failures > 0:
        print(f"FAIL: {failures} check(s) failed. Fix before opening PR.")
        return 1
    else:
        print("PASS: all self-review checks passed. Ready for PR.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
