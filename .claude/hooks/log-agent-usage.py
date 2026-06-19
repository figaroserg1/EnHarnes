#!/usr/bin/env python3
"""PostToolUse hook: log every subagent (Task) launch to logs/agent-usage.toon.

Harness visibility tool. Records WHICH subagent was launched, WHEN, and the
request it was given — one row per invocation. Launch-only (PostToolUse); it
does not capture agent results.

Standalone by design: it imports nothing from the project's source tree — the
harness must not couple to product code. The output is a simple
tab-separated log with a TOON-style header line, nothing more.

Contract: read PostToolUse payload from stdin, never raise, always exit 0 —
a logging hook must not break tool execution.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HEADER = "agent_invocations{ts,agent,details}"
LOG_REL = Path("logs") / "agent-usage.toon"
PROMPT_CAP = 2000  # keep rows bounded; full prompt lives in the session transcript


def main() -> None:
    raw = sys.stdin.read()
    payload = json.loads(raw)

    if payload.get("tool_name") != "Task":
        return  # only subagent launches are of interest

    tool_input = payload.get("tool_input") or {}
    agent = tool_input.get("subagent_type") or "unknown"
    prompt = (tool_input.get("prompt") or "")[:PROMPT_CAP]
    details = {
        "description": tool_input.get("description") or "",
        "prompt": prompt,
    }

    # Resolve logs/ relative to the project root the hook runs in (cwd from payload).
    root = Path(payload.get("cwd") or ".")
    log_path = root / LOG_REL
    log_path.parent.mkdir(parents=True, exist_ok=True)

    ts = datetime.now(timezone.utc).isoformat()
    row = f"{ts}\t{agent}\t{json.dumps(details, ensure_ascii=False)}\n"

    new_file = not log_path.exists() or log_path.stat().st_size == 0
    with log_path.open("a", encoding="utf-8") as fh:
        if new_file:
            fh.write(HEADER + "\n")
        fh.write(row)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # Visibility is best-effort: never let logging fail a tool call.
        pass
    sys.exit(0)
