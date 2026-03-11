---
allowed-tools: Bash, Read, Grep, Glob
description: Run entropy scan and doc gardener, report findings
---

Run entropy and documentation health checks.

## Steps

1. Run `make entropy` — scan for stale placeholders, orphan scripts, blank setpoints, large files, broken doc references.
2. Run `make gardener` — check for stale verification headers, broken links, sparse indexes, doc lint, doc drift.
3. Summarize all findings in a table:
   - Issue type
   - File affected
   - Severity (blocking / warning)
   - Suggested fix
4. If any issues found, ask whether to fix them now or log in `docs/exec-plans/tech-debt-tracker.md`.
