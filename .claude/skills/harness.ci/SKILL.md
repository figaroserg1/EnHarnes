---
name: harness-ci
description: CI orchestration, pre-PR gates, type checking, metrics, and worktree management. Ties linters and generators into CI pipelines.
---

# Harness CI

Orchestration scripts for CI pipelines, pre-PR quality gates, and developer workflow tools.

## Scripts

- `lint_runner.py` — Orchestrator: runs todo_linter + code_conventions in sequence
- `pre_pr_gate.py` — 4-check pre-PR self-review gate
- `typecheck.py` — Type checking wrapper
- `measure_metrics.py` — Harness health metrics collection
- `worktree_boot.py` — Git worktree bootstrap for isolated task branches

## Dependencies

- Requires **harness-linters** (lint_runner calls linter scripts)
- Requires **harness-core** (for policies/ and workflow rules)

## Makefile Targets

```makefile
lint:     lint-todos + lint-src + lint-structural (composite)
review:   pre_pr_gate.py
ci:       lint (alias)
```

## CI Workflow

Typical CI pipeline order:
1. `make lint` — All linters (TODO + source + structural)
2. `make review` — Pre-PR gate (4 checks)
