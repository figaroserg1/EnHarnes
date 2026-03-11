# Harness Planner — ExecPlan Creation Skill

**Planning is pure. No code modifications during planning.**

## When to Use

Use `/plan <task-description>` when:
- A task spans multiple files or layers
- Risk is medium or high (per `policies/risk-policy.json`)
- The task involves architecture changes, new features, or complex refactors

## Workflow

### Phase 1: Research (read-only)

1. **Read `OPENAI_PLANS.md`** (this skill directory) — the canonical ExecPlan format. Follow it to the letter. It defines all required sections, the skeleton, formatting rules, and non-negotiable requirements.
2. Read `AGENTS.md` — check autonomy tier for this task type
3. Read `ARCHITECTURE.md` — understand layers, boundaries, quality grades
4. Read `docs/GOLDEN_PRINCIPLES.md` — mechanical invariants the plan must respect
5. Read `policies/risk-policy.json` — identify doc-drift rules for affected paths
6. Scan affected source files — understand current state before proposing changes

### Phase 2: Author

Create the plan at `docs/exec-plans/active/YYYY-MM-DD-<slug>.md`.

Use the skeleton from `OPENAI_PLANS.md` verbatim. Every section listed there is mandatory.

Size guidelines:

| Complexity | Milestones | Tasks per Milestone |
|---|---|---|
| Small (1-3 files) | 1-2 | 2-4 |
| Medium (4-10 files) | 2-3 | 3-6 |
| Large (10+ files) | 3-5 | 4-8 |

### Phase 3: Validate

Before presenting:
- [ ] Self-contained: a novice with only the plan + repo can succeed
- [ ] Every file referenced by full repo-relative path
- [ ] Acceptance criteria are observable behaviors, not code attributes
- [ ] Risk-policy watch paths identified, affected docs listed
- [ ] `make smoke` passes

### After Approval

1. Execute milestone by milestone
2. Atomic commits per task: `T<NNN>: <summary>`
3. Quality gates after each task: `make check`, `make structural`
4. Update the plan as a living document during execution
5. On completion: fill Outcomes & Retrospective, move to `docs/exec-plans/done/`
