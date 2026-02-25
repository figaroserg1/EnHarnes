# Agent Runbook

Full operational guide for autonomous agent work. `AGENTS.md` points here.

---

## Session Lifecycle

### Start
1. Read `AGENTS.md` (map + commands).
2. Read `docs/exec-plans/active/` — pick up assigned plan if any.
3. If resuming: read `progress.txt` for prior context.
4. `make smoke`.

### During Work
- After every file change: `make check` + verify `risk-policy.json` drift rules.
- If you created/resolved a TODO: run `python scripts/sync_todo_registry.py`.

### Before PR
```bash
make review
```
Fix all failures. Re-run until clean. Then open PR with:
- What changed and why.
- Which docs were updated (from risk-policy.json watch-path matches).

### End
1. Update `progress.txt`: what done, what's left, blockers.
2. Commit any uncommitted work.
3. Address open review comments on PRs.

---

## Autonomy Rules

| Risk | You do | You ask human |
|------|--------|---------------|
| **Low** — docs, tests, lint fixes, typos | Execute fully. Commit, open PR. | Nothing. |
| **Medium** — new scripts, refactors, config changes | Write ExecPlan + implement + PR. | Wait for approval before merge. |
| **High** — architecture, security, Providers, infra | Write ExecPlan only. Stop. | Human approves before implementation. |

- Unsure about risk → treat as medium.
- `risk-policy.json` defines tiers and watch paths.

---

## Doc Update Triggers

When you change files, docs must follow. These are not optional.

| Trigger | Action |
|---------|--------|
| Changed files match `risk-policy.json` watch path | Verify and update each listed doc |
| Changed a script | Check if `AGENTS.md` Quick Commands needs update |
| Added new tool/script | Add to `tools/skills_registry.json` + `AGENTS.md` Project Map |
| Changed architecture | Update `ARCHITECTURE.md` (layers, grades) |
| Resolved a TODO | Remove from source file. Run `sync_todo_registry.py` |
| Found doc that contradicts code | Fix doc immediately, same commit |
| Created new design doc | Add to `docs/design-docs/index.md` with verified date |

---

## Maintenance Schedule

Perform proactively. Do not wait for human to ask.

### Every PR
- Doc-drift verified automatically via `make review`.
- If you spot stale docs while working → fix them in same PR.

### Weekly (or on prompt: "maintain" / "housekeeping")
- `make entropy` → fix flagged issues.
- `make gardener` → fix stale verification headers, broken links.
- Review `docs/exec-plans/active/` → update progress on open plans.
- Review `docs/exec-plans/tech-debt-tracker.md` → pick up small items.

### Monthly (or on prompt: "health check")
- `python scripts/measure_metrics.py --owner figaroserg1 --repo EnHarnes --days 30`
- Compare to `evals/control-loop-metrics.yaml`. If ALERT → create ExecPlan for root cause.
- Update quality grades in `ARCHITECTURE.md`.
- Verify all docs in `docs/design-docs/index.md` → update `Verified` dates.

---

## Decision Making

When facing a choice with no clear answer:

1. `docs/design-docs/rules.md` — existing guidance?
2. `docs/design-docs/core-beliefs.md` — belief that points to answer?
3. `docs/GOLDEN_PRINCIPLES.md` — mechanical rule?
4. None apply → choose simpler option, document decision in `docs/design-docs/`, add to index.

---

## ExecPlan Protocol

Complex tasks (multi-file, architecture, new features) need an ExecPlan.

1. Create in `docs/exec-plans/active/<name>.md` using template from `docs/PLANS.md`.
2. Low risk → start immediately. Medium/high → wait for human approval.
3. Update Progress section as you work.
4. On completion → move to `docs/exec-plans/completed/`, write Outcomes.
