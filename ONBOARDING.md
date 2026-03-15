# ONBOARDING — Project Bootstrap Guide

This guide walks you through setting up a new project for agent-driven development with EnHarnes. Follow the steps in order. Once complete, remove the onboarding reference from `AGENTS.md` (see last section).

---

## Step 1: Create the RFP

Start by writing `docs/RFP.md` — the Request for Proposal. This is the single source of truth that the agent will use to generate all other docs.

### RFP Sections

```markdown
# RFP: <Project Name>

## 1. Problem Statement
What problem does this solve? Who has it? Why now?

## 2. Goals & Non-Goals
- Goals: what success looks like (measurable)
- Non-goals: explicit scope boundaries

## 3. Target Users
Who uses this? What are their workflows?

## 4. Functional Requirements
Numbered list of features. Each: description, priority (P0/P1/P2), acceptance criteria.

## 5. Technical Constraints
Language, framework, infra, performance requirements, compatibility.

## 6. Architecture Overview
High-level layers, data flow, external integrations.
(Agent will expand this into ARCHITECTURE.md)

## 7. Security & Compliance
Auth model, data handling, regulatory requirements.

## 8. Observability Requirements
What to log, what to monitor, alert thresholds.

## 9. Quality Requirements
Test coverage targets, performance budgets, reliability SLOs.

## 10. Milestones
Phased delivery plan. Each milestone: scope, deliverables, verification criteria.

## 11. Open Questions
Unresolved decisions. Agent should flag these, not guess.
```

### Prompt to create RFP

Copy this into your agent session:

> Create `docs/RFP.md` for this project. Interview me section by section — ask 2-3 questions per section, then write the section based on my answers. Start with Problem Statement.

---

## Step 2: Generate Project Docs from RFP

Once the RFP is complete, the agent can generate all required docs from it.

### Prompt to generate docs

> Read `docs/RFP.md` and `AGENTS.md`. Generate these files based on the RFP:
>
> 1. `ARCHITECTURE.md` — layers, import rules, quality grades (use `policies/architecture.yaml` format from harness example)
> 2. `policies/architecture.yaml` — layer names, allowed imports, file size limits
> 3. `docs/PROJECT_DESIGN.md` — system design from RFP sections 1-6
> 4. `docs/PROJECT_SECURITY.md` — from RFP section 7
> 5. `docs/PROJECT_OBSERVABILITY.md` — from RFP section 8
> 6. `docs/PROJECT_QUALITY_SCORE.md` — from RFP section 9
> 7. `docs/PROJECT_RELIABILITY.md` — SLOs and failure modes
> 8. `docs/product-specs/index.md` — feature specs from RFP section 4
> 9. `docs/exec-plans/active/` — one ExecPlan per milestone from RFP section 10
>
> For each file: follow the existing templates in `docs/`. Mark unknowns as `TODO: [HUMAN]`. Run `make smoke` after each file.

---

## Step 3: Set Up Verification

Before writing any code, set up the project's verification tools.

### Prompt

> Based on `ARCHITECTURE.md` and `docs/RFP.md`:
>
> 1. Create `policies/architecture.yaml` with layers and import rules
> 2. Create `tests/` directory with a structural test for layer boundaries
> 3. Create `scripts/verify/` with a sanity check script
> 4. Run `make install-hooks` to enable pre-commit linting
> 5. Verify: `make smoke` and `make lint-structural` must pass
>
> Remember: every feature needs a deterministic verification strategy (see AGENTS.md → Verification-First Engineering).

---

## Step 4: First Feature

Pick the first P0 feature from the RFP and implement it using the harness workflow:

1. `/harness.plan` — create an ExecPlan (must include Verification section)
2. Implement in small steps, `make smoke` after each
3. `/harness.test` — full suite
4. `/harness.review` — pre-PR gate

---

## Step 5: Sync Generators

After initial docs are in place, run the generators to create derived files:

```bash
make gen-handbook    # project handbook
make sync-todos      # TODO registry from codebase
make sync-indexes    # doc index sync
```

---

## Onboarding Complete

Once all steps are done:

1. Remove the `> **New project? Start with [ONBOARDING.md](ONBOARDING.md)**` line from `AGENTS.md`
2. Optionally move this file to `docs/references/ONBOARDING.md` for future reference
3. The project is now ready for autonomous agent-driven development
