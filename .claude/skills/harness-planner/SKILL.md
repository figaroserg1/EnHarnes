# Harness Planner — ExecPlan Creation Skill

This skill guides AI agents through creating self-contained execution plans (ExecPlans) following the OpenAI Harness Engineering methodology.

## When to Use

Use `/plan <task-description>` when:
- A task spans multiple files or layers
- Risk is medium or high (per risk-policy.json)
- The task involves architecture changes, new features, or complex refactors
- You need a plan that any novice agent can pick up and execute

## Core Principle

**Planning is pure. No code modifications during planning.**

An ExecPlan is a living document that contains ALL knowledge needed to implement a feature. A complete novice — with only the repo and the plan — must be able to succeed.

## Workflow

### Phase 1: Research (read-only)

1. Read `.claude/skills/harness-planner/OPENAI_PLANS.md` — the canonical ExecPlan format specification
2. Read `AGENTS.md` — check autonomy tier for this task type
3. Read `ARCHITECTURE.md` — understand layers, boundaries, quality grades
4. Read `docs/GOLDEN_PRINCIPLES.md` — mechanical invariants the plan must respect
5. Read `policies/risk-policy.json` — identify doc-drift rules for affected paths
6. Scan affected source files — understand current state before proposing changes

### Phase 2: Plan Authoring

Create the plan at `docs/exec-plans/active/YYYY-MM-DD-<slug>.md`.

The plan MUST follow the skeleton from `.claude/skills/harness-planner/OPENAI_PLANS.md` and include:

#### Required Sections
- **Purpose / Big Picture** — what someone gains after this change, how to see it working
- **Progress** — checkbox list, timestamps, updated at every stopping point
- **Context and Orientation** — current repo state relevant to the task, key file paths
- **Plan of Work** — prose description of edits, file paths, what to insert/change
- **Concrete Steps** — exact commands, working directories, expected outputs
- **Validation and Acceptance** — how to prove the change works (behavior, not attributes)
- **Idempotence and Recovery** — safe retries, rollback paths
- **Interfaces and Dependencies** — libraries, types, function signatures
- **Decision Log** — every decision with rationale and date
- **Surprises & Discoveries** — unexpected findings during research
- **Outcomes & Retrospective** — filled after completion

#### Quality Gates for the Plan
- [ ] Self-contained: novice can execute with only the plan + repo
- [ ] No jargon without definition
- [ ] Every file referenced by full repo-relative path
- [ ] Acceptance criteria are observable behaviors, not code attributes
- [ ] Milestones are independently verifiable
- [ ] Risk-policy watch paths identified, affected docs listed
- [ ] Golden Principles compliance checked for proposed changes

### Phase 3: Plan Validation

Before presenting the plan:
1. Verify all referenced files exist
2. Verify proposed changes don't violate layer dependencies
3. Verify risk tier matches autonomy level in AGENTS.md
4. Run `make smoke` to confirm repo is clean before planning

## Plan Size Guidelines

| Task Complexity | Milestones | Tasks per Milestone |
|---|---|---|
| Small (1-3 files) | 1-2 | 2-4 |
| Medium (4-10 files) | 2-3 | 3-6 |
| Large (10+ files) | 3-5 | 4-8 per milestone |

## Anti-Patterns (DO NOT)

- Do not write code during planning
- Do not use vague task descriptions ("implement caching", "fix performance")
- Do not assume prior context — repeat every assumption
- Do not point to external docs — embed knowledge in the plan
- Do not create tasks that a junior developer couldn't start immediately
- Do not skip the Decision Log — every choice needs rationale

## Integration with Harness

After plan is created:
1. Agent or human reviews the plan
2. If approved → execute milestone by milestone
3. Each task gets an atomic commit with `T<NNN>: <summary>`
4. Quality gates run after each task: `make check`, `make structural`
5. Plan is updated as a living document during execution
6. On completion → fill Outcomes & Retrospective, move to `docs/exec-plans/done/`

## Reference Files

| File | Purpose |
|---|---|
| `.claude/skills/harness-planner/OPENAI_PLANS.md` | Canonical ExecPlan format (read first, follow to the letter) |
| `AGENTS.md` | Autonomy tiers, task loop, core rules |
| `ARCHITECTURE.md` | Layer structure, quality grades |
| `docs/GOLDEN_PRINCIPLES.md` | Mechanical invariants |
| `policies/risk-policy.json` | Doc-drift rules, risk tiers |
| `docs/exec-plans/active/` | Where new plans go |
| `docs/exec-plans/done/` | Completed plans archive |
