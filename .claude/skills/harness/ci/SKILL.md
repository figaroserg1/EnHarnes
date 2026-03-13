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
check:    lint_runner.py
review:   pre_pr_gate.py
ci:       make test (check + structural)
```

## CI Workflow

Typical CI pipeline order:
1. `make smoke` — Fast sanity (doc linter only)
2. `make check` — Static checks (lint runner)
3. `make structural` — Architecture boundary tests
4. `make review` — Pre-PR gate (5 checks)
