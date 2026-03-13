.PHONY: smoke check structural ast-rules ast-scan test ci build tools todo-sync sync-skills sync-indexes entropy review gardener obs-up obs-down

# Python interpreter — override on Windows: make check PYTHON=python
PYTHON ?= python3
H = scripts/harness

# Fast sanity: doc linter only (~5s)
smoke:
	$(PYTHON) $(H)/doc-health/doc_linter.py

# Static checks: doc lint + code conventions
check:
	$(PYTHON) $(H)/lint_runner.py

# Validate lint rule YAML files
ast-rules:
	$(PYTHON) $(H)/code-quality/validate_lint_rules.py policies/ast-grep/

# Run ast-grep scan on src/
ast-scan:
	ast-grep scan --rule policies/ast-grep/ src/

# Structural architecture tests only
structural:
	pytest $(H)/architecture/test_layer_dependencies.py

# Full test suite: check + structural
test:
	make check
	make structural

# CI-equivalent local run — same as make test
ci:
	make test

# Generators
build:
	$(PYTHON) $(H)/generators/build_handbook.py

todo-sync:
	$(PYTHON) $(H)/generators/sync_todo_registry.py

sync-skills:
	$(PYTHON) $(H)/generators/sync_skills_to_agents.py

sync-indexes:
	$(PYTHON) $(H)/generators/sync_doc_indexes.py

# Health
entropy:
	$(PYTHON) $(H)/entropy/entropy_check.py

review:
	$(PYTHON) $(H)/pre_pr_gate.py

gardener:
	$(PYTHON) $(H)/doc-health/doc_health_check.py

# Observability
obs-up:
	$(PYTHON) $(H)/observability/structured_log.py up

obs-down:
	$(PYTHON) $(H)/observability/structured_log.py down
