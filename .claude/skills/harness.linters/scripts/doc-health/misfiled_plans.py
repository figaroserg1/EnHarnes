#!/usr/bin/env python3
"""Misfiled-plan linter: a completed ExecPlan must not sit in active/.

`docs/exec-plans/active/` holds in-flight plans; `done/` holds finished ones.
The dev-loop relocates a plan to `done/` on completion, but that was an inferred
convention, not a codified step — easy to drop right when attention is on
verify/review/commit (see docs/harness-feedback.md, 2026-06-17).

This turns the convention into a deterministic check. To stay high-precision —
a false positive would block CI on a legitimately in-flight plan, which is worse
than the status quo — a plan counts as "complete" only when BOTH signals agree:

  1. Progress is done: it has at least one Progress checkbox and zero unchecked
     `- [ ]` boxes (a crisp signal — active plans carry open boxes, done plans
     don't).
  2. Outcomes is filled: the `## Outcomes & Retrospective` section has real
     content, not a placeholder. Placeholders that mean "not done yet":
       - "(To be filled in at completion.)"
       - "To be written when the task closes ..."
       - "(REPLACE ME)"
       - the template guidance line from OPENAI_PLANS.md
       - whitespace only

Any plan in `active/` that satisfies both is self-contradictory state and gets
flagged with the fix: git mv it to done/.

Runs via `make lint-todos` / `make lint` and standalone.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
ACTIVE_DIR = ROOT / "docs" / "exec-plans" / "active"

SECTION_RE = re.compile(r"^##\s+Outcomes\s*&\s*Retrospective\s*$", re.IGNORECASE)
NEXT_SECTION_RE = re.compile(r"^##\s+")

# Lines that, alone, mean the section is still a placeholder (case-insensitive,
# punctuation/whitespace-insensitive substring match).
PLACEHOLDER_SIGNATURES = [
    "to be filled in at completion",
    "to be written when the task closes",
    "to be written",
    "replace me",
    "summarize outcomes, gaps, and lessons learned",
    "tbd",
]
UNCHECKED_RE = re.compile(r"^\s*[-*]\s+\[ \]")
CHECKED_RE = re.compile(r"^\s*[-*]\s+\[[xX]\]")


def _section_body(text: str) -> list[str] | None:
    """Return the lines of the Outcomes & Retrospective section, or None."""
    lines = text.splitlines()
    body: list[str] = []
    in_section = False
    for line in lines:
        if not in_section:
            if SECTION_RE.match(line):
                in_section = True
            continue
        if NEXT_SECTION_RE.match(line):
            break
        body.append(line)
    return body if in_section else None


def _is_filled(body: list[str]) -> bool:
    for raw in body:
        stripped = raw.strip()
        if not stripped:
            continue
        normalized = re.sub(r"[^a-z0-9 ]", "", stripped.lower())
        if any(sig in normalized for sig in PLACEHOLDER_SIGNATURES):
            continue
        # Any other non-blank, non-placeholder line counts as real content.
        return True
    return False


def _progress_done(text: str) -> bool:
    """True when the plan has checkbox milestones and none are unchecked."""
    has_checked = any(CHECKED_RE.match(line) for line in text.splitlines())
    has_unchecked = any(UNCHECKED_RE.match(line) for line in text.splitlines())
    return has_checked and not has_unchecked


def main() -> int:
    if not ACTIVE_DIR.is_dir():
        print("[misfiled-plans] OK: no active/ directory.")
        return 0

    offenders: list[str] = []
    for plan in sorted(ACTIVE_DIR.glob("*.md")):
        text = plan.read_text(encoding="utf-8")
        body = _section_body(text)
        if body is None:
            continue  # no Outcomes section yet — not a completion signal
        # High precision: require BOTH signals (all milestones checked AND a
        # filled Outcomes) before declaring the plan complete-but-misfiled.
        if _progress_done(text) and _is_filled(body):
            offenders.append(plan.name)

    if offenders:
        print("Misfiled ExecPlan errors:")
        for name in offenders:
            print(
                f"  [ERROR] docs/exec-plans/active/{name}: "
                f"'Outcomes & Retrospective' is filled in, so the plan is complete "
                f"but still in active/. Fix: git mv it to docs/exec-plans/done/."
            )
        return 1

    print("[misfiled-plans] OK: no completed plans left in active/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
