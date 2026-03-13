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

1. **Boot worktree** — `python scripts/harness/worktree_boot.py <task-name>`
2. **Validate** — `make lint-todos`. Stop if fails.
3. **Load context** — check `progress.txt` if resuming. Load docs from Reference Table.
4. **Research** — for medium/high risk: launch subagent in researcher role (facts only, no opinions). Output → `docs/exec-plans/active/*-research.md`.
5. **Implement** — small steps. `make lint` after each change.
6. **Doc drift** — check `policies/risk-policy.json` → `docsDriftRules`. Update matching docs.
7. **Pre-PR** — `make review`. Fix all failures.
8. **Agent review** — for medium/high risk: launch subagent in reviewer role (fresh context, no shared assumptions).
9. **Review loop** — respond to feedback until approved.
10. **Merge + teardown** — merge PR, remove worktree.
11. **Session end** — update `progress.txt`.

## Cadenced Ops

- **Weekly / between tasks:** `make check-entropy`, `make check-docs`
- **Monthly / when drift:** `python .claude/skills/harness.ci/scripts/measure_metrics.py`
- **Every PR (CI):** `python .claude/skills/harness.linters/scripts/doc-health/check_doc_drift.py`

## Available Tools

| Command | Purpose |
|---------|---------|
| `make lint-todos` | TODO ownership & placeholder checks (~5s) |
| `make lint-src` | Code conventions (bare print, kebab-case, file size) |
| `make lint-structural` | Architecture boundary tests (pytest) |
| `make lint` | Composite: lint-todos + lint-src + lint-structural |
| `make ci` | CI alias for `lint` |
| `make review` | Pre-PR self-review (4 gates) |
| `make check-entropy` | Entropy scan (orphans, blank setpoints) |
| `make check-docs` | Doc health (stale headers, broken links) |
| `make gen-handbook` | Generate project handbook |
| `make sync-skills` / `sync-indexes` / `sync-todos` | Sync generators |
| `make obs-up` / `obs-down` | Observability stack |

### DO NOT USE

- `rm -rf` on directories → use git clean or targeted removal
- Direct DB queries in prod → use Repo layer
- `curl` to external APIs → use Providers layer ApiClient
- `git push --force` to main → regular push or `--force-with-lease`
- `pip install` in global env → use venv
- Bare `print()` in prod code → use logging (Golden Principle #13)

## Core Rules

- Layer imports flow downward only. Cross-cutting via `Providers` only → `ARCHITECTURE.md`, `policies/architecture.yaml`
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
| Core skill (docs, templates, examples) | `.claude/skills/harness.core/SKILL.md` | Setting up harness in a new project |
| Workflow rules | `.claude/skills/harness.core/docs/WORKFLOW_RULES.md` | Agent execution, change mgmt |
| Core principles | `.claude/skills/harness.core/docs/CORE_PRINCIPLES.md` | Harness methodology |
| Golden principles (linter rules) | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` | Writing/modifying linters |
| CI/merge policy | `docs/design-docs/ci-enforcement.md` | CI or merge config changes |
| Execution plans | `.claude/skills/harness.plan/SKILL.md` | ExecPlans for medium/high risk |
| Worktree workflow | `.claude/skills/harness.core/docs/WORKTREE_WORKFLOW.md` | Boot script issues |
| Observability | `docs/PROJECT_OBSERVABILITY.md` | Logging or metrics |
| Browser automation | `.claude/skills/harness.core/docs/BROWSER_AUTOMATION.md` | UI testing |
| Entropy management | `.claude/skills/harness.core/docs/ENTROPY_PRINCIPLES.md` | Entropy scans |
| Health setpoints | `policies/control-loop-metrics.yaml` | Health checks |
| Doc drift policy | `policies/risk-policy.json` | After any code change (step 5) |
| Architecture policy | `policies/architecture.yaml` | Setting up layers for a new project |
| Example project | `.claude/skills/harness.core/example/` | Reference for `src/` layout + `architecture.yaml` |
| Anti-overengineering | `.claude/skills/harness.anti-overengineering/SKILL.md` | Startup-style pragmatic rules |
| Linters | `.claude/skills/harness.linters/SKILL.md` | Architecture, code quality, doc health checks |
| Generators | `.claude/skills/harness.generators/SKILL.md` | Handbook, doc index, TODO sync |
| CI scripts | `.claude/skills/harness.ci/SKILL.md` | CI orchestration, pre-PR gates |
## Subagent Roles

Launch subagents by role name. If `.claude/agents/harness/<role>.md` exists, it will be used. Otherwise Claude creates a universal agent with that role — both work fine.

| Role | Purpose |
|------|---------|
| researcher | Pre-planning codebase research. Facts only, no opinions. |
| reviewer | Independent pre-PR review. Fresh context, read-only. |
| codebase-analyzer | Analyze HOW code works — trace data flow. |
| codebase-locator | Find WHERE code lives — file search by topic. |
| security-orchestrator | Multi-phase security investigation. |
| code-synthesis-analyzer | Analyze recent changes for issues. |
| code-clarity-refactorer | Apply refactoring rules. Proactive. |
| bug-issue-creator | Investigate bug + create GitHub issue. |

## Failure Ledger

When an agent breaks something, **fix the harness, not the agent**. Add entries: `rule:`, `context:`, `fix:`, `enforcement:`. Prefer linter/test over documentation. Rewrite "should" as "must".

<!-- Add failure ledger entries below this line -->

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/harness.smoke` | Run `make lint-todos`. Report result. If passed → suggest `/harness.lint` or `/harness.review`. |
| `/harness.lint` | Run `make lint`. Report results. If all passed → suggest `/harness.review`. |
| `/harness.review` | Run `make review`. Fix failures, re-run. Summarize: lint / doc-drift / entropy. If all pass → "Ready for PR". |
| `/harness.entropy` | Run `make check-entropy` + `make check-docs`. Summarize findings (issue, file, severity, fix). Ask: fix now or log to `docs/exec-plans/tech-debt-tracker.md`? |

## Self-Improvement

- Update this file, docs, and scripts as needed. Your convenience is priority.
- On failure → add ledger entry + update docs. If automatable → write a linter/test instead.
