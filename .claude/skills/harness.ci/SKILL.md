---
name: harness-ci
description: CI orchestration, pre-PR gates, type checking, metrics, and worktree management. Ties linters and generators into CI pipelines.
---

# Harness CI

Orchestration scripts for CI pipelines, pre-PR quality gates, and developer workflow tools.

## Scripts

- `lint_runner.py` — Orchestrator: runs doc_linter + code_conventions in sequence
- `pre_pr_gate.py` — 5-check pre-PR self-review gate
- `typecheck.py` — Type checking wrapper
- `measure_metrics.py` — Harness health metrics collection
- `worktree_boot.py` — Git worktree bootstrap for isolated task branches

## Dependencies

- Requires **harness-linters** (lint_runner calls linter scripts)
- Requires **harness-core** (for policies/ and workflow rules)

## Makefile Targets

```makefile
lint:     lint_runner.py
review:   pre_pr_gate.py
ci:       make test (lint + structural)
```

## CI Workflow

Typical CI pipeline order:
1. `make lint-todos` — Doc linter only (~5s)
2. `make lint` — All static checks (lint runner)
3. `make structural` — Architecture boundary tests
4. `make review` — Pre-PR gate (5 checks)
