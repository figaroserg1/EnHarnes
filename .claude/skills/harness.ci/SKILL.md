---
name: harness-ci
description: CI observability — health metrics collection via GitHub API, worktree management.
---

# Harness CI

CI observability and developer workflow tools.

## Scripts

- `measure_metrics.py` — Harness health metrics collection via GitHub API (`gh` CLI). Measures PR pass-at-1 rate, merge cycle time, revert rate, human intervention rate, time to CI failure. Reads setpoints from `policies/control-loop-metrics.yaml`.

## Related (not in this skill)

- `scripts/harness/worktree_boot.py` — Git worktree bootstrap for isolated task branches

## Dependencies

- Requires **harness-linters** (linting and pre-PR gates moved there)
- Requires **harness-core** (for policies/)
- Requires `gh` CLI authenticated (`gh auth login`)

## Makefile Targets

No direct Makefile targets. Run manually:

```bash
python .claude/skills/harness.ci/scripts/measure_metrics.py --owner OWNER --repo REPO [--days 30]
```
