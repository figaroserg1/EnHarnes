#!/usr/bin/env python3
"""PreToolUse hook: blocks dangerous bash commands.

Reads tool input from stdin, returns JSON decision to stdout.
Blocks: rm -rf /, force pushes to main, dropping databases, etc.
"""

import json
import re
import sys


BLOCKED_PATTERNS = [
    (r"rm\s+-rf\s+/(?!\S)", "Refusing to rm -rf /"),
    (r"git\s+push\s+.*--force.*\b(main|master)\b", "Force push to main/master is blocked"),
    (r"git\s+push\s+.*\b(main|master)\b.*--force", "Force push to main/master is blocked"),
    (r"git\s+reset\s+--hard\s+origin/(main|master)", "Hard reset to origin main/master is blocked"),
    (r"DROP\s+(DATABASE|TABLE)", "DROP DATABASE/TABLE is blocked"),
    (r"truncate\s+table", "TRUNCATE TABLE is blocked"),
    (r":(){ :\|:& };:", "Fork bomb detected"),
    (r"mkfs\.", "Filesystem format command is blocked"),
    (r"> /dev/sd[a-z]", "Direct device write is blocked"),
]

ASK_PATTERNS = [
    (r"git\s+push", "About to push to remote — confirm?"),
    (r"rm\s+-rf", "Recursive delete — confirm target?"),
    (r"git\s+reset\s+--hard", "Hard reset will discard changes — confirm?"),
    (r"pip\s+install(?!.*-r\s+requirements)", "Installing package outside requirements.txt — confirm?"),
]


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    tool_name = data.get("toolName", "")
    if tool_name != "Bash":
        return

    command = data.get("toolInput", {}).get("command", "")
    if not command:
        return

    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            json.dump({
                "permissionDecision": "deny",
                "reason": reason,
            }, sys.stdout)
            return

    for pattern, reason in ASK_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            json.dump({
                "permissionDecision": "ask",
                "reason": reason,
            }, sys.stdout)
            return


if __name__ == "__main__":
    main()
