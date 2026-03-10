# AGENTS.md

You are an AI agent. Read this fully at session start. This is your operating manual.

## Task Loop (every task follows this sequence)

1. **Boot worktree** — `./scripts/dev/worktree-boot.sh <task-name>`. Every task runs in isolation.
2. **Validate state** — `make smoke`. Do not proceed if it fails.
3. **Load context** — check `progress.txt` if resuming. Load docs from the table below as needed.
4. **Implement** — small, verifiable steps. `make check` after each change.
5. **Doc drift** — open `policies/risk-policy.json` → `docsDriftRules`. If changed files match a `watch` path, update every listed doc.
6. **Pre-PR** — `make review`. Fix all failures. Then open PR.
7. **Review loop** — respond to feedback, iterate until reviewers approve.
8. **Merge + teardown** — merge PR, `git worktree remove <path>`.
9. **Session end** — update `progress.txt`: done, remaining, blockers.

## Autonomy

| Risk | Action |
|------|--------|
| **Low** (docs, tests, lint) | Execute full loop. Commit, PR. |
| **Medium** (scripts, refactors) | ExecPlan + PR. Wait for approval before merge. |
| **High** (architecture, security) | ExecPlan only. Do not implement. |

Unsure → medium. Tiers defined in `policies/risk-policy.json`.

## Cadenced Operations

| What | Cadence | How |
|------|---------|-----|
| Entropy scan | Weekly (or between tasks) | `make entropy`, `make gardener` → `docs/ENTROPY.md` |
| Health metrics | Monthly (or when metrics drift) | `python scripts/health/measure_metrics.py` → `policies/control-loop-metrics.yaml` |
| Doc gardening | With every PR | `scripts/health/check_doc_drift.py` runs in CI automatically |

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

## Agent Capabilities

- filesystem
- git
- browser automation
- observability queries
- TODO: [AI] Update when adding MCP servers or local tools.
- TODO: [AI->HUMAN] Clarify staging environment access.

## Core Rules

- Layers flow one way: `Types→Config→Repo→Service→Runtime→UI`. Cross-cutting via `Providers` only → `ARCHITECTURE.md`
- Validate at boundaries. No YOLO-parsing inside layers.
- Reuse existing utilities. No duplicates.
- No secrets in repo.
- All knowledge lives in-repo. If it's not here, it doesn't exist.
- If a doc contradicts code — fix the doc, same commit.

## Reference Table

| Topic | File | When to load |
|-------|------|-------------|
| Architecture + quality grades | `ARCHITECTURE.md` | Architecture decisions |
| Design rules & philosophy | `docs/design-docs/rules.md` | Design choices |
| Core beliefs | `docs/design-docs/core-beliefs.md` | Design choices |
| Golden principles (linter rules) | `docs/GOLDEN_PRINCIPLES.md` | Writing/modifying linters |
| CI/merge policy | `docs/design-docs/ci-enforcement-and-risk-policy.md` | CI or merge config changes |
| Execution plans | `docs/PLANS.md` | Complex/multi-file tasks → create plan in `docs/exec-plans/active/` |
| Worktree workflow | `docs/WORKTREE_WORKFLOW.md` | Boot script issues or naming questions |
| Observability | `docs/OBSERVABILITY.md` | Logging or metrics setup |
| Browser automation | `docs/references/BROWSER_AUTOMATION.md` | UI testing or browser tasks |
| Entropy management | `docs/ENTROPY.md` | Cadenced entropy scans |
| Health setpoints | `policies/control-loop-metrics.yaml` | Cadenced health checks |
| Doc drift policy | `policies/risk-policy.json` | After any code change (step 5 of loop) |
| Scripts | `scripts/` | — |
| Linters + structural tests | `scripts/linters/`, `scripts/structural-tests/` | — |

## Self improvement
- You suppoed to update the Agents.md and related docs and scripts, create missing ones for yourself. Your convenience is proority. 
- Any time you run into an issue and found solution, update docs accordinly to awoid the issue in the future