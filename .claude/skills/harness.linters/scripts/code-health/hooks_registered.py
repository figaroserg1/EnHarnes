#!/usr/bin/env python3
"""Hook-registration linter: every Claude Code hook script must be wired.

Every executable hook in `.claude/hooks/` is dead weight unless some settings
source references it. This check makes that gap deterministic instead of relying
on a human noticing — see docs/harness-feedback.md (2026-06-15, the three
"pre-merged" hooks that were never registered and silently no-op'd).

Scope and CI behaviour:
  - `.claude/settings.json` (and `settings.local.json`) may be git-ignored
    (per-operator config, not repo). When that is the case, in CI / a fresh
    checkout there is no settings file to read. When NO settings source exists,
    this check SKIPS (exit 0 with a notice) rather than failing — a missing
    operator file is not a repo defect.
  - When a settings source IS present (a developer's working copy), every
    `.claude/hooks/*.py` must be referenced by command string in some source,
    else the check fails. This catches "fixed/added a hook but forgot to wire
    it" locally, before it reaches the operator.

Runs via `make lint` (composite) and standalone.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HOOKS_DIR = ROOT / ".claude" / "hooks"
SETTINGS_SOURCES = [
    ROOT / ".claude" / "settings.json",
    ROOT / ".claude" / "settings.local.json",
]


def _registered_commands(sources: list[Path]) -> str:
    """Concatenate every hook command string found across settings sources."""
    blob: list[str] = []
    for src in sources:
        try:
            data = json.loads(src.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        hooks = data.get("hooks", {})
        for matchers in hooks.values():
            for matcher in matchers or []:
                for hook in matcher.get("hooks", []) or []:
                    cmd = hook.get("command")
                    if cmd:
                        blob.append(cmd)
    return "\n".join(blob)


def main() -> int:
    hook_files = sorted(p for p in HOOKS_DIR.glob("*.py") if p.name != "__init__.py")
    if not hook_files:
        print("[hooks-registered] OK: no hook scripts to check.")
        return 0

    present = [s for s in SETTINGS_SOURCES if s.exists()]
    if not present:
        print(
            "[hooks-registered] SKIP: no .claude/settings.json present "
            "(operator-local, git-ignored). Cannot verify registration here."
        )
        return 0

    blob = _registered_commands(present)
    unregistered = [p.name for p in hook_files if p.name not in blob]

    if unregistered:
        print("Hook-registration errors:")
        for name in unregistered:
            print(
                f"  [ERROR] .claude/hooks/{name}: present but not registered in "
                f"any settings source ({', '.join(s.name for s in present)}). "
                f"Fix: add a hooks entry pointing at it, or delete the dead hook."
            )
        return 1

    print(f"[hooks-registered] OK: all {len(hook_files)} hook(s) registered.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
