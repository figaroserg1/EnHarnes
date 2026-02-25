# AGENTS.md

You are an AI agent. This file is your map. Read it at session start, follow pointers.

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

## Workflow

1. Read this file → follow pointers to relevant docs.
2. `make smoke` to verify repo health.
3. Implement in minimal steps. `make check` after each.
4. `make review` before opening PR. Fix failures, re-run until clean.
5. Open PR. Resolve all review threads before merge.

Details: `docs/AGENT_RUNBOOK.md`

## After Every Change

1. `make check` — fix failures.
2. Read `risk-policy.json` `docsDriftRules` — if changed files match a `watch` path, verify and update listed docs.

## Autonomy

| Risk | Action |
|------|--------|
| **Low** (docs, tests, lint) | Execute, commit, PR. |
| **Medium** (scripts, refactors) | ExecPlan + PR. Wait for approval. |
| **High** (architecture, security) | ExecPlan only. Do not implement. |

Unsure → treat as medium. Details: `docs/AGENT_RUNBOOK.md`

## Core Rules

- Unidirectional layers: `Types→Config→Repo→Service→Runtime→UI`. Cross-cutting via `Providers` only → `ARCHITECTURE.md`
- Validate at boundaries. No YOLO-parsing inside layers.
- Reuse existing utilities. No duplicates.
- No secrets in repo.
- Docs that contradict code → fix immediately, same commit.

## Project Map

| What | Where |
|---|---|
| Agent runbook (full operational guide) | `docs/AGENT_RUNBOOK.md` |
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
