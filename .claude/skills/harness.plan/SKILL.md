---
allowed-tools: Read, Write, Edit, Grep, Glob, Agent
argument-hint: "[task-description]"
description: Create a self-contained ExecPlan for a task
---

Read `.claude/skills/harness.planner/SKILL.md` and follow the instructions there.

Do not write code. Output: plan file path, purpose summary, milestone count, risk tier.

Next: after plan is approved, suggest implementing step by step with `/harness.smoke` after each change.
