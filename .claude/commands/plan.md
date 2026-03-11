---
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
argument-hint: "[task-description]"
description: Create a self-contained ExecPlan following OpenAI Harness Engineering methodology
---

Create an execution plan for the given task. **No code modifications during planning.**

## Phase 1: Research (mandatory, read-only)

Read these files in order. Do not skip any:

1. `.claude/skills/harness-planner/OPENAI_PLANS.md` — the canonical ExecPlan format. Follow it to the letter.
2. `AGENTS.md` — check autonomy tier for this task (low/medium/high).
3. `ARCHITECTURE.md` — understand layers, boundaries, quality grades.
4. `docs/GOLDEN_PRINCIPLES.md` — mechanical invariants the plan must respect.
5. `policies/risk-policy.json` — identify doc-drift watch paths for affected areas.

Then scan the affected source files to understand current state.

## Phase 2: Author the Plan

Create `docs/exec-plans/active/YYYY-MM-DD-<slug>.md`.

The plan MUST include ALL of these sections (from `OPENAI_PLANS.md` skeleton):

### Required sections
- **Purpose / Big Picture** — what someone gains after this change, how to see it working
- **Progress** — `- [ ]` checkbox list with timestamps, updated at every stopping point
- **Context and Orientation** — current repo state, key file paths (full repo-relative), define all jargon
- **Plan of Work** — prose: sequence of edits, file + location + what to change
- **Concrete Steps** — exact commands, working directories, expected output transcripts
- **Validation and Acceptance** — observable behaviors (not code attributes). "Run X, expect Y."
- **Idempotence and Recovery** — safe retries, rollback path
- **Interfaces and Dependencies** — libraries, types, function signatures
- **Decision Log** — every design decision with rationale
- **Surprises & Discoveries** — unexpected findings during research
- **Outcomes & Retrospective** — filled after execution completes

### Size guidelines
- Small (1-3 files): 1-2 milestones, 2-4 tasks each
- Medium (4-10 files): 2-3 milestones, 3-6 tasks each
- Large (10+ files): 3-5 milestones, 4-8 tasks per milestone

## Phase 3: Validate the Plan

Before presenting:
- [ ] Self-contained: a novice with only the plan + repo can succeed
- [ ] No undefined jargon
- [ ] Every file referenced by full repo-relative path
- [ ] Acceptance criteria are behaviors, not code attributes
- [ ] Each milestone independently verifiable
- [ ] Watch paths from risk-policy.json identified, affected docs listed
- [ ] Golden Principles compliance verified for proposed changes

## Anti-patterns (DO NOT)
- Write code during planning
- Use vague descriptions ("improve performance", "add caching")
- Assume prior context — repeat every assumption
- Point to external docs — embed needed knowledge
- Create tasks a junior developer couldn't start immediately
- Skip the Decision Log

## Output

Print: plan file path, purpose summary, milestone count, risk tier, affected layers.
