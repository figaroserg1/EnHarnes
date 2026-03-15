---
name: harness-linters
description: Static analysis, quality checks, pre-PR gates, type checking — architecture boundaries, code conventions, doc health, entropy detection. Reads config from policies/.
---

# Harness Linters

Static analysis scripts that enforce code quality, architecture boundaries, documentation health, and pre-PR quality gates.

## Scripts

### architecture-health/
- `test_layer_dependencies.py` — Layer DAG enforcement, cycle detection, cross-cutting imports (Golden Principles 1, 3, 12). Reads `policies/architecture.yaml`.

### code-health/
- `code_conventions.py` — No bare print(), file size limits, kebab-case naming, layer directory validation (Golden Principles 4, 5). Reads `policies/architecture.yaml`.
- `validate_lint_rules.py` — Validates ast-grep rule YAML files in `policies/ast-grep/`.

### doc-health/
- `todo_linter.py` — TODO owner format, template marker checks. Universal, no config needed.
- `doc_health_check.py` — Stale docs, broken links, orphan files, index coverage. Uses autodiscovery.
- `check_doc_drift.py` — Detects doc/code drift per `policies/risk-policy.json` watch paths.

### entropy/
- `entropy_check.py` — Orphan scripts, blank setpoints detection.

### Top-level
- `lint_runner.py` — Orchestrator: runs todo_linter + code_conventions in sequence. Auto-detects project type.
- `typecheck.py` — Universal type checker with auto-detection (Rust/Node/Python).
- `pre_pr_gate.py` — 4-check pre-PR self-review gate (lint + doc-drift + watch-paths + entropy).

## Dependencies

- Requires **harness-core** (for policies/ and docs references)
- All scripts read from `policies/` — no hardcoded project knowledge

## Makefile Targets

```makefile
lint-todos:      todo_linter.py
lint-src:        code_conventions.py
lint-structural: pytest test_layer_dependencies.py
lint-yaml:       validate_lint_rules.py
lint-ast:        ast-grep scan
check-entropy:   entropy_check.py
check-docs:      doc_health_check.py
review:          pre_pr_gate.py
```
