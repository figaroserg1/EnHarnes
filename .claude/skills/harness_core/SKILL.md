---
name: harness-core
description: Core harness methodology — principles, workflow rules, golden principles, architecture policy, and project templates. Foundation for all other harness skills.
---

# Harness Core

Foundation skill providing methodology docs, project templates, and policies.

## What's Included

### Docs
- `CORE_PRINCIPLES.md` — Harness methodology fundamentals
- `WORKFLOW_RULES.md` — Agent execution and change management rules
- `GOLDEN_PRINCIPLES.md` — Linter rules reference (what each rule checks and where)
- `WORKTREE_WORKFLOW.md` — Git worktree boot script usage
- `ENTROPY_PRINCIPLES.md` — Entropy management methodology
- `BROWSER_AUTOMATION.md` — UI testing guidance
- `baseline-template.md` — Baseline doc template
- `harness-checklist.md` — Full harness setup checklist

### Templates
- `AGENTS.md.template` — Agent control panel template for new projects
- `Makefile.inc` — Makefile include with all harness targets

### Example
- `example/` — Reference project with 7-layer architecture, filled `architecture.yaml`

## Installation

This skill is the foundation. Install it first, then add linters/generators/ci as needed.

After installing, the agent should:
1. Copy `templates/AGENTS.md.template` → `AGENTS.md` (customize for project)
2. Copy `policies/` templates from example if needed
3. Review `GOLDEN_PRINCIPLES.md` for available lint rules

## Policies (User-Customizable)

All project-specific config lives in `policies/` at the repo root:
- `architecture.yaml` — Layers, allowed imports, cross-cutting modules, file size limits
- `doc-indexes.yaml` — Doc index generation config
- `control-loop-metrics.yaml` — Health setpoints
- `risk-policy.json` — Risk tiers, doc drift rules
- `ast-grep/` — Custom lint rules (YAML)

See `example/architecture.yaml` for a filled-in reference.
