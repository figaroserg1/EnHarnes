---
name: harness-linters
description: Static analysis and quality checks — architecture boundaries, code conventions, doc health, entropy detection. Reads config from policies/.
---

# Harness Linters

Static analysis scripts that enforce code quality, architecture boundaries, and documentation health.

## Scripts

### architecture/
- `test_layer_dependencies.py` — Layer DAG enforcement, cycle detection, cross-cutting imports (Golden Principles 1, 3, 12). Reads `policies/architecture.yaml`.

### code-quality/
- `code_conventions.py` — No bare print(), file size limits, kebab-case naming, layer directory validation (Golden Principles 4, 5). Reads `policies/architecture.yaml`.
- `validate_lint_rules.py` — Validates ast-grep rule YAML files in `policies/ast-grep/`.

### doc-health/
- `todo_linter.py` — TODO owner format, template marker checks. Universal, no config needed.
- `doc_health_check.py` — Stale docs, broken links, orphan files, index coverage. Uses autodiscovery.
- `check_doc_drift.py` — Detects doc/code drift per `policies/risk-policy.json` watch paths.

### entropy/
- `entropy_check.py` — Orphan scripts, blank setpoints detection.

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
```
