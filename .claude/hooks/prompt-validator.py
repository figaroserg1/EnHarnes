#!/usr/bin/env python3
"""UserPromptSubmit hook: checks for secrets in prompts before sending.

Scans the user prompt for common secret patterns (API keys, tokens, passwords).
Blocks if a likely secret is detected.
"""

import json
import re
import sys

SECRET_PATTERNS = [
    (r"(?i)(api[_-]?key|apikey)\s*[:=]\s*[\"']?[a-zA-Z0-9]{20,}", "API key detected"),
    (r"(?i)(password|passwd|pwd)\s*[:=]\s*([\"'][^\"']{8,}[\"']|[^\s]{8,})", "Password detected"),
    (r"sk-[a-zA-Z0-9]{32,}", "OpenAI-style secret key detected"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub personal access token detected"),
    (r"(?i)bearer\s+[a-zA-Z0-9\-._~+/]+=*", "Bearer token detected"),
    (r"-----BEGIN (RSA |EC |)PRIVATE KEY-----", "Private key detected"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key detected"),
]


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        return

    # Claude Code passes the prompt under the snake_case key "prompt".
    prompt = data.get("prompt", "")
    if not prompt:
        return

    for pattern, reason in SECRET_PATTERNS:
        if re.search(pattern, prompt):
            json.dump({
                "decision": "block",
                "reason": f"Potential secret found in prompt: {reason}. Remove it before sending.",
            }, sys.stdout)
            return

    # No secret detected: stay silent. A UserPromptSubmit hook's stdout is
    # injected into the prompt context, so emitting anything here would be noise.


if __name__ == "__main__":
    main()
