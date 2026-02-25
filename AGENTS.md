# AGENTS.md

You are an AI agent working in this repository. This file is your entry point.
Read it fully at session start, then follow pointers.

---

## Quick Commands

| Goal | Command |
|---|---|
| Fast sanity check | `make smoke` |
| Static checks (lint + imports) | `make check` |
| Structural / architecture tests | `make structural` |
| Full test suite | `make test` |
| CI-equivalent local run | `make ci` |
| Self-review before PR | `make review` |
| Doc gardener (stale docs/links) | `make gardener` |
| Entropy scan | `make entropy` |
| Measure health metrics | `python scripts/measure_metrics.py --owner figaroserg1 --repo EnHarnes` |

---

## Autonomy Levels

You operate at different levels depending on risk. Check `risk-policy.json` for tier definitions.

| Risk | You do | You ask human |
|------|--------|---------------|
| **Low** (docs, tests, lint fixes) | Execute fully. Commit, open PR. | Nothing — proceed. |
| **Medium** (new scripts, refactors, config) | Draft change + ExecPlan. Open PR. | Wait for approval before merge. |
| **High** (architecture, security, Providers, infra) | Write ExecPlan only. Do not implement. | Human approves plan first. |

When unsure about risk level → treat as medium.

---

## On Every Code Change

After any modification to files, do these steps **automatically**:

1. **Run `make check`** — fix any failures before continuing.
2. **Check `risk-policy.json`** — read `docsDriftRules`. If your changed files match a `watch` path, open and verify each listed doc. Update docs if they no longer reflect reality.
3. **Update TODO registry** — if you created, resolved, or changed a TODO, run `python scripts/sync_todo_registry.py`.
4. **Log the change** — `python -c "import scripts.obs as obs; obs.log('info', 'changed X', component='Y')"` (when obs.py is on PYTHONPATH).

---

## On Every PR (Before Opening)

Run the full self-review. Do not skip steps.

```bash
make review
```

This runs: static checks → structural tests → doc-drift → watch-path reminders → entropy spot-check.

If `make review` passes:
1. Open PR with concise summary (what changed, why, which docs updated).
2. If `risk-policy.json` flagged docs to verify, list them in PR description.

If `make review` fails:
1. Fix every failure.
2. Re-run until clean.
3. Then open PR.

---

## On Session Start

1. Read this file.
2. Read `docs/exec-plans/active/` — check if there's an active plan assigned to you.
3. If resuming prior work, read `progress.txt` for context.
4. Run `make smoke` to verify repo is healthy.

## On Session End

1. Update `progress.txt` with: what was done, what's left, any blockers.
2. If changes are uncommitted, commit with descriptive message.
3. If a PR is open, check for review comments and address them.

---

## Maintenance Tasks (Do Proactively)

You are responsible for repo health. Perform these without being asked:

### Every PR
- Verify doc-drift (automatic via `make review`).
- If you notice stale docs while working, fix them in the same PR.

### Weekly (or when prompted "maintain" / "housekeeping")
- Run `make entropy` — fix anything flagged.
- Run `make gardener` — fix stale verification headers, broken links.
- Check `docs/exec-plans/active/` — update progress on open plans.
- Check `docs/exec-plans/tech-debt-tracker.md` — pick up small debt items.

### Monthly (or when prompted "health check")
- Run `python scripts/measure_metrics.py --owner figaroserg1 --repo EnHarnes --days 30`.
- Compare results to `evals/control-loop-metrics.yaml` setpoints.
- If any metric is in ALERT: create an ExecPlan to fix the root cause.
- Update quality grades in `ARCHITECTURE.md` if they changed.
- Verify all docs in `docs/design-docs/index.md` — update `Verified` dates.

---

## Doc Update Rules

Docs are your responsibility. Follow these rules strictly:

1. **When you change code** → check `risk-policy.json` and update listed docs.
2. **When you change a script** → update Quick Commands table above if needed.
3. **When you add a new tool/script** → add it to `tools/skills_registry.json` and Project Map below.
4. **When you change architecture** → update `ARCHITECTURE.md` (layers, grades, diagram).
5. **When you resolve a TODO** → remove it from the source file. Run `python scripts/sync_todo_registry.py`.
6. **When you find a doc that contradicts code** → fix the doc immediately, same commit.
7. **When you create a new doc** → add it to `docs/design-docs/index.md` with verification date.

---

## Decision Making

When facing a design choice:

1. Check `docs/design-docs/rules.md` — does it already have guidance?
2. Check `docs/design-docs/core-beliefs.md` — does a belief point to an answer?
3. Check `docs/GOLDEN_PRINCIPLES.md` — is there a mechanical rule?
4. If none apply: choose the simpler option, document the decision in `docs/design-docs/`, add entry to `docs/design-docs/index.md`.

---

## Core Rules

- Follow unidirectional layer architecture → `ARCHITECTURE.md`
- Validate data at layer boundaries. No YOLO-parsing inside layers.
- Use existing utilities (`src/utils/`, shared packages). Do not create duplicates.
- For task documentation and repo structure descriptions, use `printdirtree` when appropriate.
- No secrets in repo. No hardcoded credentials.

---

## Project Map

| What | Where |
|---|---|
| Architecture + quality grades | `ARCHITECTURE.md` |
| Design rules & philosophy | `docs/design-docs/rules.md` |
| Core beliefs (agent-facing) | `docs/design-docs/core-beliefs.md` |
| Mechanical invariants (linter rules) | `docs/GOLDEN_PRINCIPLES.md` |
| CI/merge policy + rationale | `docs/design-docs/ci-enforcement-and-risk-policy.md` |
| Execution plans | `docs/exec-plans/active/` |
| Planning spec | `docs/PLANS.md` |
| Observability | `docs/OBSERVABILITY.md` |
| Entropy management | `docs/ENTROPY.md` |
| Agent health setpoints | `evals/control-loop-metrics.yaml` |
| Doc drift policy | `risk-policy.json` |
| Reliability / Security | `docs/RELIABILITY.md`, `docs/SECURITY.md` |
| Product specs | `docs/product-specs/` |
| DB schema (auto-updated) | `docs/generated/db-schema.md` |
| Browser automation guide | `docs/BROWSER_AUTOMATION.md` |
| Worktree workflow | `docs/WORKTREE_WORKFLOW.md` |
| Harness checklist + scores | `docs/CHECKLIST.md` |
| Deep research backlog | `docs/DEEP_RESEARCH.md` |
| Metrics evaluation harness | `scripts/measure_metrics.py` |
| Observability module | `scripts/obs.py` |
| Doc-drift checker | `scripts/check_doc_drift.py` |
| All scripts | `scripts/` |
| Linters + structural tests | `tools/` |

---

## ExecPlans

Complex tasks (multi-file, architecture changes, new features) require an ExecPlan.

1. Create plan in `docs/exec-plans/active/<name>.md` using template from `docs/PLANS.md`.
2. For **low risk**: start implementing immediately after writing the plan.
3. For **medium/high risk**: wait for human approval before implementing.
4. Update plan's Progress section as you work.
5. When complete, move to `docs/exec-plans/completed/` and write Outcomes section.
