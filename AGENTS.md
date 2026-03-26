# AGENTS.md — Agent Control Panel

**Humans steer, agents execute.** You MUST read this fully at session start and follow every step.

> **New project? Start with [ONBOARDING.md](ONBOARDING.md)** — step-by-step bootstrap from RFP to ready-for-development. Remove this line once/if onboarding is complete.

## Permissions

You own the full repo. You may create, modify, and delete any file — code, scripts, linters, tests, docs, configs, instructions (including this file). Build deterministic tools for everything checkable mechanically. If it can be a linter rule or test — make it one.

## Autonomy

| Risk | Action |
|------|--------|
| **Low** (docs, tests, lint) | Execute full loop. Commit, PR. |
| **Medium** (scripts, refactors) | **MUST** create ExecPlan first → get approval → implement → PR. |
| **High** (architecture, security) | **MUST** create ExecPlan only. Do NOT implement. |

Unsure → treat as medium. Tiers defined in `policies/risk-policy.json`.

**HARD RULE:** For medium/high risk tasks, you MUST NOT write any implementation code until an ExecPlan exists in `docs/exec-plans/active/`. Skipping the plan is a harness violation.

### ExecPlan Minimum Content

Every ExecPlan MUST contain these sections (see `.claude/skills/harness.plan/SKILL.md` for full template):

1. **Goal** — what and why (1-2 sentences)
2. **Risk tier** — Low / Medium / High + justification
3. **Scope** — files to create/modify (list)
4. **Steps** — numbered implementation steps
5. **Verification** — concrete commands to prove it works (not "manual check")
6. **Decision log** — key choices with reasoning (append during work)
7. **Progress** — checklist updated as steps complete

## Task Loop

Every task MUST follow this loop. Steps marked 🚫 STOP are hard gates — do not proceed until the gate passes.

1. **Boot worktree** — `python scripts/harness/worktree_boot.py <task-name>`
2. **Validate** — `make lint-todos`. 🚫 STOP if fails.
3. **Log start** — append session entry to Activity Log (see below).
4. **Load context** — check `progress.txt` if resuming. Load docs from Reference Table.
5. **Classify risk** — determine Low/Medium/High per Autonomy table.
6. **Plan** (medium/high only) — create ExecPlan in `docs/exec-plans/active/`. 🚫 STOP — do NOT implement until plan exists and is acknowledged.
7. **Research** — for medium/high risk: launch subagent in researcher role (facts only, no opinions). Output → `docs/exec-plans/active/*-research.md`.
8. **Implement** — small steps. `make lint` after each change. Log each tool/command in Activity Log.
9. **Doc drift** — check `policies/risk-policy.json` → `docsDriftRules`. Update matching docs.
10. **Pre-PR** — `make review`. 🚫 STOP — fix all failures before proceeding.
11. **Agent review** — for medium/high risk: launch subagent in reviewer role (fresh context, no shared assumptions).
12. **Review loop** — respond to feedback until approved.
13. **Merge + teardown** — merge PR, remove worktree.
14. **Log end** — finalize Activity Log entry. Update `progress.txt`.

## What Runs Automatically (do NOT call these manually)

| Trigger | Script | What it does |
|---------|--------|-------------|
| Before every bash command | `validate-bash.py` (PreToolUse hook) | Blocks dangerous commands (rm -rf, force push, DROP) |
| Before every prompt | `prompt-validator.py` (UserPromptSubmit hook) | Blocks secrets in prompts |
| After every response | `post-response-sync.py` (Stop hook) | Auto-syncs doc indexes if .md files changed |
| Before every commit | `pre-commit` hook | Runs `make lint` — blocks commit on failure |
| On PR / push to main | `ci.yml` workflow | Lint + doc-drift check |
| Daily 03:00 UTC | `nightly-entropy.yml` | Entropy scan |
| Monday 06:00 UTC | `weekly-cleanup.yml` | Auto-fixes TODO owners, creates cleanup PR |

**You do NOT need to call any of these.** They fire automatically. The pre-commit hook also means `make lint` runs before every commit — you don't need to lint right before committing.

## Agent Commands (what YOU call)

| Command | When to use | Duration |
|---------|-------------|----------|
| `make lint-todos` | Task Loop step 2: validate before starting | ~5s |
| `make lint` | Step 8: after each change (composite: todos + src + structural) | ~10s |
| `make review` | Step 10: pre-PR gate (5 checks: lint + structural + doc-drift + watch-paths + entropy) | ~2min |
| `make check-entropy` | Cadenced: between tasks or weekly | ~1min |
| `make check-docs` | Cadenced: between tasks or weekly | ~1min |
| `make gen-handbook` | After significant doc changes | ~2min |
| `make sync-todos` / `sync-skills` / `sync-indexes` | After adding TODOs, skills, or docs (sync-indexes also auto-runs via hook) | ~30s |
| `make obs-up` / `obs-down` | When you need structured JSON logging | instant |
| `make install-hooks` | One-time: install pre-commit hook in a new worktree | instant |

**Simplified mental model:** `make lint` after changes → `make review` before PR → done. Everything else is cadenced or situational.

## Cadenced Ops

- **Weekly / between tasks:** `make check-entropy`, `make check-docs`
- **Monthly / when drift:** `python .claude/skills/harness.ci/scripts/measure_metrics.py`

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
| Onboarding guide | `ONBOARDING.md` | New project bootstrap (RFP → docs → code) |
| Architecture + quality grades | `ARCHITECTURE.md` | Architecture decisions |
| Architecture checklist | `.claude/skills/harness.core/docs/ARCHITECTURE_CHECKLIST.md` | Writing or validating ARCHITECTURE.md |
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
| Doc drift policy | `policies/risk-policy.json` | After any code change (step 8) |
| Architecture policy | `policies/architecture.yaml` | Setting up layers for a new project |
| Example project | `.claude/skills/harness.core/example/` | Reference for `src/` layout + `architecture.yaml` |
| Anti-overengineering | `.claude/skills/harness.anti-overengineering/SKILL.md` | Startup-style pragmatic rules |
| Linters | `.claude/skills/harness.linters/SKILL.md` | Architecture, code health, doc health, pre-PR gates |
| Generators | `.claude/skills/harness.generators/SKILL.md` | Handbook, doc index, TODO sync |
| CI observability | `.claude/skills/harness.ci/SKILL.md` | Health metrics via GitHub API |
| Task walkthrough (example) | `docs/TASK_WALKTHROUGH.md` | Understanding the full task flow, auto vs manual |

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

- **rule:** Agent must create ExecPlan before implementing medium/high risk tasks.
  **context:** In teamsBotTest project, agent skipped plan creation and went straight to implementation for Phase 1 MVP.
  **fix:** Added HARD RULE with 🚫 STOP gate in Task Loop step 6. Added ExecPlan Minimum Content section.
  **enforcement:** Task Loop gate — plan file must exist in `docs/exec-plans/active/` before step 8.

- **rule:** Agent must log all tool invocations in Activity Log.
  **context:** In teamsBotTest project, agent did not maintain activity log during Phase 1. No audit trail.
  **fix:** Made Activity Log MANDATORY with MUST language. Logging is now Task Loop steps 3, 8, and 14.
  **enforcement:** Activity Log section with compliance language. Session without log entry = non-compliant.

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/harness.smoke` | Run `make lint-todos`. Report result. If passed → suggest `/harness.lint` or `/harness.review`. |
| `/harness.lint` | Run `make lint`. Report results. If all passed → suggest `/harness.review`. |
| `/harness.review` | Run `make review`. Fix failures, re-run. Summarize: lint / doc-drift / entropy. If all pass → "Ready for PR". |
| `/harness.entropy` | Run `make check-entropy` + `make check-docs`. Summarize findings (issue, file, severity, fix). Ask: fix now or log to `docs/exec-plans/tech-debt-tracker.md`? |

## Activity Log — MANDATORY

You MUST maintain an activity log at `docs/activity-log.md`. This is NOT optional — it is a core compliance artifact.

**Start of every session:** append a new entry header immediately after loading AGENTS.md.
**During work:** log every tool/command execution and every document read.
**End of session:** finalize the entry with outcome.

Format:
```
## YYYY-MM-DD HH:MM — <task summary>
- RISK: Low/Medium/High
- PLAN: <path to ExecPlan> or "N/A (low risk)"
- READ: AGENTS.md, ARCHITECTURE.md, policies/risk-policy.json, ...
- COMMANDS: make smoke, make lint, pytest tests/, ...
- DECISIONS: chose X over Y because Z
- OUTCOME: PR #N merged / plan created / blocked on X
```

Rules:
- One entry per session or major task — start it FIRST, complete it LAST
- List EVERY .md file you read and EVERY script/command you ran
- Include the risk classification and plan reference
- If you cannot point to an Activity Log entry for your session, the session is non-compliant
- Purpose: audit trail proving agent followed the harness workflow

## Verification-First Engineering

**Every feature and every plan MUST include a deterministic, executable verification strategy.** The agent should always think: "how do I verify this works without a human?"

Verification tools are a first-class part of the project. Build them alongside features, not after.

| Verification type | Tool | When to use |
|-------------------|------|-------------|
| Code structure | `make lint`, `make lint-structural` | After every change |
| Runtime behavior | pytest, integration tests | After feature completion |
| Web UI / frontend | Playwright MCP, agentic-browser | Web app features |
| API endpoints | curl/httpx scripts, contract tests | API changes |
| Data pipelines | Snapshot tests, deterministic fixtures | Data processing |

Principles:
- If you can't verify it without a human, design it differently
- Verification scripts live in `tests/` or `scripts/verify/`
- Every ExecPlan must have a "Verification" section with concrete commands
- Prefer executable checks over manual inspection — automate judgment out of the loop

## Self-Improvement

- Update this file, docs, and scripts as needed. Your convenience is priority.
- On failure → add ledger entry + update docs. If automatable → write a linter/test instead.
