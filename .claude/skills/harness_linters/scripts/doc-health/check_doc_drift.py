#!/usr/bin/env python3
"""Doc-drift checker: reads risk-policy.json and verifies all referenced docs exist.

Runs in CI and during agent self-review. Catches stale doc references
before they become invisible to agents.

Exit code 1 if any referenced doc is missing.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
POLICY_PATH = ROOT / "policies" / "risk-policy.json"


def get_changed_files() -> set[str]:
    """Get files changed in current branch vs main (for PR context)."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "origin/main...HEAD"],
            capture_output=True, text=True, cwd=ROOT
        )
        if result.returncode == 0:
            return set(result.stdout.strip().splitlines())
    except FileNotFoundError:
        pass
    return set()


def main() -> None:
    if not POLICY_PATH.exists():
        print("[doc-drift] risk-policy.json not found; skipping.")
        return

    policy = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
    rules = policy.get("docsDriftRules", [])
    changed = get_changed_files()

    missing_docs: list[str] = []
    drift_warnings: list[str] = []

    for rule in rules:
        watch = rule.get("watch", "")
        docs = rule.get("docs", [])

        # Check all doc references resolve
        for doc in docs:
            if not (ROOT / doc).exists():
                missing_docs.append(
                    f"  MISSING: {doc} (referenced by watch path '{watch}'). "
                    f"Fix: create the file or update risk-policy.json."
                )

        # If changed files match watch path, warn about docs to verify
        if changed:
            touched = [f for f in changed if f.startswith(watch)]
            if touched:
                for doc in docs:
                    drift_warnings.append(
                        f"  VERIFY: {doc} — code changed in '{watch}' ({len(touched)} file(s)). "
                        f"Ensure doc still reflects current code."
                    )

    if drift_warnings:
        print("[doc-drift] Docs to verify (changed code in watched paths):")
        for w in drift_warnings:
            print(w)

    if missing_docs:
        print("[doc-drift] Missing doc references:")
        for m in missing_docs:
            print(m)
        sys.exit(1)

    print("[doc-drift] OK: all doc references resolve.")


if __name__ == "__main__":
    main()
