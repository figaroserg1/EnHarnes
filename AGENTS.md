# AGENTS.md — Agent Control Panel

Read this fully at session start. This is your operating manual.

**Humans steer, agents execute.** Human sets goal, constraints, quality criteria. Agent executes, verifies, documents, leaves transparent decision trail.

## Permissions

You own the full repo. You may create, modify, and delete any file — code, scripts, linters, tests, docs, configs, instructions (including this file). Use this to build deterministic tools that verify everything checkable mechanically, reducing your own cognitive load. If it can be a linter rule or test — make it one instead of remembering it.

## Autonomy

| Risk | Action |
|------|--------|
| **Low** (docs, tests, lint) | Execute full loop. Commit, PR. |
| **Medium** (scripts, refactors) | ExecPlan + PR. Wait for approval before merge. |
| **High** (architecture, security) | ExecPlan only. Do not implement. |

Unsure → medium. Tiers defined in `policies/risk-policy.json`.

## Task Loop

1. **Boot worktree** — `python scripts/dev/worktree_boot.py <task-name>`
2. **Validate** — `make smoke`. Stop if fails.
3. **Load context** — check `progress.txt` if resuming. Load docs from Reference Table.
4. **Implement** — small steps. `make check` after each change.
5. **Doc drift** — check `policies/risk-policy.json` → `docsDriftRules`. Update matching docs.
6. **Pre-PR** — `make review`. Fix all failures.
7. **Review loop** — respond to feedback until approved.
8. **Merge + teardown** — merge PR, remove worktree.
9. **Session end** — update `progress.txt`.

## Cadenced Ops

| What | When | How |
|------|------|-----|
| Entropy scan | Weekly / between tasks | `make entropy`, `make gardener` |
| Health metrics | Monthly / when drift | `python scripts/health/measure_metrics.py` |
| Doc gardening | Every PR | `scripts/health/check_doc_drift.py` (CI) |

## Quick Commands

| Goal | Command |
|------|---------|
| Sanity check | `make smoke` |
| Static checks | `make check` |
| Structural tests | `make structural` |
| Full test suite | `make test` |
| CI-equivalent | `make ci` |
| Pre-PR review | `make review` |
| Entropy scan | `make entropy` |
| Sync skills | `make sync-skills` |

## Core Rules

- Layers: `Types→Config→Repo→Service→Runtime→UI`. Cross-cutting via `Providers` only → `ARCHITECTURE.md`
- Validate at boundaries. No YOLO-parsing inside layers.
- Reuse existing utilities. No duplicates.
- No secrets in repo. All knowledge lives in-repo.
- If a doc contradicts code — fix the doc, same commit.
- Detailed structured logging everywhere — see Golden Principle #13.
- Write deterministic checks for everything verifiable. Reduce judgment, increase automation.

## Reference Table

| Topic | File | When to load |
|-------|------|-------------|
| Architecture + quality grades | `ARCHITECTURE.md` | Architecture decisions |
| Design rules & philosophy | `docs/design-docs/rules.md` | Design choices |
| Core beliefs | `docs/design-docs/core-beliefs.md` | Design choices |
| Golden principles (linter rules) | `docs/GOLDEN_PRINCIPLES.md` | Writing/modifying linters |
| CI/merge policy | `docs/design-docs/ci-enforcement-and-risk-policy.md` | CI or merge config changes |
| harness-planner | `.claude/skills/harness-planner/SKILL.md` | Create self-contained execution plans (ExecPlans) for medium/high risk tasks. No code modifications during planning. Read OPENAI_PLANS.md for the canonical format, then author and validate a plan in docs/exec-plans/active/. |
| Worktree workflow | `docs/WORKTREE_WORKFLOW.md` | Boot script issues or naming questions |
| Observability | `docs/OBSERVABILITY.md` | Logging or metrics setup |
| Browser automation | `docs/references/BROWSER_AUTOMATION.md` | UI testing or browser tasks |
| Entropy management | `docs/ENTROPY.md` | Cadenced entropy scans |
| Health setpoints | `policies/control-loop-metrics.yaml` | Cadenced health checks |
| Doc drift policy | `policies/risk-policy.json` | After any code change (step 5) |

## Self-Improvement

- Update this file and related docs/scripts as needed. Create missing ones. Your convenience is priority.
- When you hit an issue and find a solution, update docs to prevent recurrence.
- When a check could be automated, write a linter rule or test instead of documenting a manual step.
