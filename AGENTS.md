# AGENTS.md

You are an AI agent. This is your entry point. Read fully at session start.

## Quick Commands

| Goal | Command |
|---|---|
| Sanity check | `make smoke` |
| Static checks | `make check` |
| Structural tests | `make structural` |
| Full test suite | `make test` |
| CI-equivalent | `make ci` |
| Pre-PR review | `make review` |
| Entropy scan | `make entropy` |

## Autonomy

| Risk | Action |
|------|--------|
| **Low** (docs, tests, lint) | Execute, commit, PR. |
| **Medium** (scripts, refactors) | ExecPlan + PR. Wait for approval. |
| **High** (architecture, security) | ExecPlan only. Do not implement. |

Unsure → medium. Risk tiers defined in `risk-policy.json`.

## After Every Change

1. `make check` — fix failures before continuing.
2. Open `risk-policy.json` → `docsDriftRules`. If changed files match a `watch` path, verify and update every listed doc in that rule.
3. If you notice a doc contradicts code — fix the doc, same commit.

## Before Every PR

`make review` — must pass clean. Fixes all failures first. Then open PR.

## When to Load Additional Docs

| Situation | Load |
|-----------|------|
| Starting complex/multi-file task | `docs/PLANS.md` → create ExecPlan in `docs/exec-plans/active/` |
| Resuming prior work | `progress.txt` |
| Making architecture decisions | `ARCHITECTURE.md`, `docs/design-docs/rules.md` |
| Facing a design choice | `docs/design-docs/core-beliefs.md` then `docs/design-docs/rules.md` |
| Writing/modifying linter rules | `docs/GOLDEN_PRINCIPLES.md` |
| Working with CI or merge config | `docs/design-docs/ci-enforcement-and-risk-policy.md` |
| Setting up observability/logging | `docs/OBSERVABILITY.md` |
| Need browser/UI automation | `docs/BROWSER_AUTOMATION.md` |
| Working in parallel worktrees | `docs/WORKTREE_WORKFLOW.md` |
| Prompted "maintain"/"housekeeping" | `docs/ENTROPY.md` → then `make entropy`, `make gardener` |
| Prompted "health check" | `evals/control-loop-metrics.yaml` → then `python scripts/measure_metrics.py` |
| Adding new tool/script | `tools/skills_registry.json` — register it; update Project Map below |

## Session End

Update `progress.txt`: what done, what's left, blockers.

## Core Rules

- Layers flow one way: `Types→Config→Repo→Service→Runtime→UI`. Cross-cutting via `Providers` only → `ARCHITECTURE.md`
- Validate at boundaries. No YOLO-parsing inside layers.
- Reuse existing utilities. No duplicates.
- No secrets in repo.
- All knowledge lives in-repo. If it's not here, it doesn't exist.

## Project Map

| What | Where |
|---|---|
| Architecture + quality grades | `ARCHITECTURE.md` |
| Design rules & philosophy | `docs/design-docs/rules.md` |
| Core beliefs | `docs/design-docs/core-beliefs.md` |
| Golden principles (linter rules) | `docs/GOLDEN_PRINCIPLES.md` |
| CI/merge policy | `docs/design-docs/ci-enforcement-and-risk-policy.md` |
| Execution plans | `docs/exec-plans/active/` → spec: `docs/PLANS.md` |
| Observability | `docs/OBSERVABILITY.md` |
| Entropy management | `docs/ENTROPY.md` |
| Health setpoints | `evals/control-loop-metrics.yaml` |
| Doc drift policy | `risk-policy.json` |
| Browser automation | `docs/BROWSER_AUTOMATION.md` |
| Worktree workflow | `docs/WORKTREE_WORKFLOW.md` |
| Checklist + scores | `docs/CHECKLIST.md` |
| Research backlog | `docs/DEEP_RESEARCH.md` |
| Scripts | `scripts/` |
| Linters + structural tests | `tools/` |
