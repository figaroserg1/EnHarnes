#!/usr/bin/env python3
"""Register this repo's Claude Code hooks into the operator's settings.json.

`.claude/settings.json` is often git-ignored (per-operator config, not repo), in
which case hook *registration* can never ship in a commit — it is an
operator-local step. This script is the tracked source of truth for that step:
it holds the canonical
registration block and merges it idempotently into `.claude/settings.json`,
creating the file if absent and leaving any unrelated settings untouched.

Invoked by `make install-hooks` (alongside the git pre-commit hook). Safe to run
repeatedly: a hook already present (matched by its script filename under the same
event) is left as-is, never duplicated.

The complement to this is `hooks_registered.py` (a lint check): this script
*installs* the registration, that one *verifies* it.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

# Canonical registration: (event, matcher | None, hook script filename, status message).
# The command uses $CLAUDE_PROJECT_DIR so it resolves from whatever checkout runs it.
CANONICAL = [
    ("PreToolUse", "Bash", "validate-bash.py", "Validating bash command"),
    ("UserPromptSubmit", None, "prompt-validator.py", "Scanning prompt for secrets"),
    ("PostToolUse", "Task", "log-agent-usage.py", "Logging subagent launch"),
    ("Stop", None, "post-response-sync.py", "Syncing doc indexes"),
]


def _find_root() -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return Path(result.stdout.strip())
    except FileNotFoundError:
        pass
    return Path(__file__).resolve().parents[4]


def _command_for(script: str) -> str:
    return f'python3 "$CLAUDE_PROJECT_DIR/.claude/hooks/{script}"'


def _already_registered(event_entries: list, script: str) -> bool:
    for matcher_entry in event_entries:
        for hook in matcher_entry.get("hooks", []) or []:
            if script in (hook.get("command") or ""):
                return True
    return False


def main() -> int:
    root = _find_root()
    settings_path = root / ".claude" / "settings.json"

    # Every referenced hook script must actually exist before we wire it.
    hooks_dir = root / ".claude" / "hooks"
    missing = [s for _, _, s, _ in CANONICAL if not (hooks_dir / s).exists()]
    if missing:
        print(f"[install-claude-hooks] ERROR: hook script(s) not found: {', '.join(missing)}")
        return 1

    if settings_path.exists():
        try:
            settings = json.loads(settings_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            print(f"[install-claude-hooks] ERROR: {settings_path} is not valid JSON: {exc}")
            return 1
    else:
        settings = {}

    hooks = settings.setdefault("hooks", {})
    added = 0
    for event, matcher, script, status in CANONICAL:
        event_entries = hooks.setdefault(event, [])
        if _already_registered(event_entries, script):
            continue
        entry: dict = {}
        if matcher is not None:
            entry["matcher"] = matcher
        entry["hooks"] = [{
            "type": "command",
            "command": _command_for(script),
            "statusMessage": status,
        }]
        event_entries.append(entry)
        added += 1
        print(f"[install-claude-hooks] + {event}: {script}")

    if added:
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
        print(f"[install-claude-hooks] OK: {added} hook(s) registered in {settings_path}.")
        print("[install-claude-hooks] Restart the Claude Code session to load them.")
    else:
        print("[install-claude-hooks] OK: all hooks already registered; nothing to do.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
