# AGENTS.md — Agent Control Panel

**Humans steer, agents execute.** Read this fully at session start.

## Permissions

You own the full repo. You may create, modify, and delete any file — code, scripts, linters, tests, docs, configs, instructions (including this file). Build deterministic tools for everything checkable mechanically. If it can be a linter rule or test — make it one.

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
4. **Research** — for medium/high risk: launch `researcher` subagent. Output → `docs/exec-plans/active/*-research.md`.
5. **Implement** — small steps. `make check` after each change.
6. **Doc drift** — check `policies/risk-policy.json` → `docsDriftRules`. Update matching docs.
7. **Pre-PR** — `make review`. Fix all failures.
8. **Agent review** — for medium/high risk: launch `reviewer` subagent (fresh context, no shared assumptions).
9. **Review loop** — respond to feedback until approved.
10. **Merge + teardown** — merge PR, remove worktree.
11. **Session end** — update `progress.txt`.

## Cadenced Ops

- **Weekly / between tasks:** `make entropy`, `make gardener`
- **Monthly / when drift:** `python scripts/health/measure_metrics.py`
- **Every PR (CI):** `scripts/health/check_doc_drift.py`

## Available Tools

| Command | Purpose |
|---------|---------|
| `make smoke` | Fast sanity check (~5s) |
| `make check` | Static checks (lint + source guard) |
| `make structural` | Architecture boundary tests |
| `make test` | Full test suite |
| `make ci` | CI-equivalent local run |
| `make review` | Pre-PR self-review (5 checks) |
| `make entropy` | Entropy scan |
| `make gardener` | Doc gardening check |
| `make build` | Generate handbook |
| `make sync-skills` / `sync-indexes` / `todo-sync` | Sync generators |
| `python scripts/dev/worktree_boot.py <name>` | Create isolated worktree |
| `python scripts/health/measure_metrics.py` | GitHub health metrics |
| `python scripts/observability/obs.py up\|down` | Observability stack |

### DO NOT USE

- `rm -rf` on directories → use git clean or targeted removal
- Direct DB queries in prod → use Repo layer
- `curl` to external APIs → use Providers layer ApiClient
- `git push --force` to main → regular push or `--force-with-lease`
- `pip install` in global env → use venv
- Bare `print()` in prod code → use logging (Golden Principle #13)

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
| harness-planner (skill) | `.claude/skills/harness-planner/SKILL.md` | ExecPlans for medium/high risk. No code during planning. |
| researcher (agent) | `.claude/agents/researcher.md` | Pre-planning codebase research. Facts only, no opinions. |
| reviewer (agent) | `.claude/agents/reviewer.md` | Independent pre-PR review. Fresh context, read-only. |
| codebase-analyzer (agent) | `.claude/agents/codebase-analyzer.md` | Analyze HOW code works — trace data flow. |
| codebase-locator (agent) | `.claude/agents/codebase-locator.md` | Find WHERE code lives — file search by topic. |
| security-orchestrator (agent) | `.claude/agents/security-orchestrator.md` | Multi-phase security investigation. |
| code-synthesis-analyzer (agent) | `.claude/agents/code-synthesis-analyzer.md` | Analyze recent changes for issues. |
| code-clarity-refactorer (agent) | `.claude/agents/code-clarity-refactorer.md` | Apply 10 refactoring rules. Proactive. |
| bug-issue-creator (agent) | `.claude/agents/bug-issue-creator.md` | Investigate bug + create GitHub issue. |
| Worktree workflow | `docs/WORKTREE_WORKFLOW.md` | Boot script issues |
| Observability | `docs/OBSERVABILITY.md` | Logging or metrics |
| Browser automation | `docs/references/BROWSER_AUTOMATION.md` | UI testing |
| Entropy management | `docs/ENTROPY.md` | Entropy scans |
| Health setpoints | `policies/control-loop-metrics.yaml` | Health checks |
| Doc drift policy | `policies/risk-policy.json` | After any code change (step 5) |

## Failure Ledger

When an agent breaks something, **fix the harness, not the agent**. Add entries: `rule:`, `context:`, `fix:`, `enforcement:`. Prefer linter/test over documentation. Rewrite "should" as "must".

<!-- Add failure ledger entries below this line -->

## Self-Improvement

- Update this file, docs, and scripts as needed. Your convenience is priority.
- On failure → add ledger entry + update docs. If automatable → write a linter/test instead.
