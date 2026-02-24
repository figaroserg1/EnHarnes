# AGENTS.md

Navigation map for agents. Single source of truth is `docs/`. Do not invent outside it.

## Quick Commands

| Goal | Command |
|---|---|
| Fast sanity check | `make smoke` |
| Static checks (lint + imports) | `make check` |
| Structural / architecture tests | `make structural` |
| Full test suite | `make test` |
| CI-equivalent local run | `make ci` |
| Self-review before PR | `make review` |
| Weekly entropy scan | `make entropy` |

## Core Rules

- Follow unidirectional layer architecture → `ARCHITECTURE.md`
- Never write code without an approved ExecPlan → `docs/PLANS.md`
- Validate data at layer boundaries. No YOLO-parsing inside layers.
- Use existing utilities. Do not create duplicates.
- Update `progress.txt` before ending a session.
- When code changes, check `risk-policy.json` to see which docs need updating.
- Для задач по документации и описанию структуры репозитория используй `printdirtree` (когда уместно) вместо ручного перечисления дерева.

## Project Map

| What | Where |
|---|---|
| Architecture | `ARCHITECTURE.md` |
| Design rules & philosophy | `docs/design-docs/rules.md` |
| Core beliefs (agent-facing) | `docs/design-docs/core-beliefs.md` |
| Mechanical invariants (linter rules) | `docs/GOLDEN_PRINCIPLES.md` |
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
| Harness checklist | `docs/CHECKLIST.md` |
| Deep research backlog | `docs/DEEP_RESEARCH.md` |
| Metrics evaluation harness | `scripts/measure_metrics.py` |
| Observability module | `scripts/obs.py` |
| Scripts | `scripts/` |
| Linters + structural tests | `tools/` |

## Development Workflow

1. Receive task via prompt.
2. Read this file, then follow pointers to relevant docs.
3. Check constraints in `docs/design-docs/rules.md` and `risk-policy.json`.
4. For complex tasks, create an ExecPlan in `docs/exec-plans/active/` (see `docs/PLANS.md`).
5. Implement changes in minimal steps. Run `make check` after each step.
6. Run `make test` to verify all gates pass.
7. Run `make review` (agent self-review) before opening PR.
8. Open PR with concise summary. Resolve all review threads before merge.

## ExecPlans

Any complex task or refactor requires an ExecPlan (see `docs/PLANS.md`).
Code is only written after the plan appears in `docs/exec-plans/active/`.
