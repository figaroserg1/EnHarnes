---
allowed-tools: Read, Write, Edit, Grep, Glob
argument-hint: "[task-description]"
description: Create an execution plan for a task in docs/exec-plans/active/
---

Create a structured execution plan for the given task.

## Steps

1. Read `docs/PLANS.md` to understand the ExecPlan format.
2. Read `AGENTS.md` to check autonomy tier for this task.
3. Read `ARCHITECTURE.md` and relevant design docs for context.
4. Create a new plan file at `docs/exec-plans/active/YYYY-MM-DD-<slug>.md` with:
   - **Goal**: what we're achieving
   - **Scope**: files/layers affected
   - **Steps**: ordered implementation steps, each with acceptance criteria
   - **Risks**: what could go wrong
   - **Rollback**: how to undo if needed
   - **Evidence**: how to verify success (commands, tests)
5. Print the plan path and summary.
