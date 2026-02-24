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
| Scripts | `scripts/` |
| Linters + structural tests | `tools/` |

## ExecPlans

Any complex task or refactor requires an ExecPlan (see `docs/PLANS.md`).
Code is only written after the plan appears in `docs/exec-plans/active/`.
