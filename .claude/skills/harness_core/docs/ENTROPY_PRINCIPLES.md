# Entropy Management

Agents replicate patterns — including bad ones.
Without a scheduled cleanup process, the codebase drifts even when individual PRs look correct.
This document defines what drift looks like and how we fight it.

## Known Drift Sources

- Stale docs after workflow or script changes
- Dead scripts not referenced by CI or Makefile
- TODOs without owners accumulating silently
- Inconsistent naming across layers
- Architectural boundary violations introduced incrementally
- Golden principles that have no corresponding linter check

## Entropy Controls

| Cadence | Action |
|---|---|
| Per PR | `make check` catches lint + structural violations before merge |
| Weekly | Run `scripts/health/entropy_check.py` — scans for stale docs, dead scripts, orphaned TODOs |
| Monthly | Review `docs/exec-plans/tech-debt-tracker.md` — escalate items older than 30 days |
| After refactor | Re-run structural tests and verify `policies/risk-policy.json` doc links still resolve |

## Running the Entropy Check

```bash
python scripts/health/entropy_check.py
```

Output: list of files with potential drift issues. Each item is a candidate for cleanup, not a guaranteed problem. Agent reviews each and resolves or logs in tech-debt-tracker.

## What the Check Looks For

- Markdown files with `EXAMPLE (REPLACE ME)` still present
- Scripts in `scripts/` not referenced in `Makefile` or CI
- TODO items in docs older than 14 days without progress
- `policies/control-loop-metrics.yaml` setpoints with blank targets
- Files in `src/` that violate golden principle file-size limits

## Ownership

Primary owner: `TODO: [HUMAN]`
Review cadence: weekly
Escalation: add to `docs/exec-plans/active/` if cleanup requires > 1 hour of work
