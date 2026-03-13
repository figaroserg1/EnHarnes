# Harness Makefile include — add to your project Makefile:
#   include .claude/skills/harness.core/templates/Makefile.inc

.PHONY: smoke check structural ast-rules ast-scan test ci build todo-sync sync-skills sync-indexes entropy review gardener obs-up obs-down

PYTHON ?= python3
S ?= .claude/skills

# Fast sanity: doc linter only (~5s)
smoke:
	$(PYTHON) $(S)/harness.linters/scripts/doc-health/doc_linter.py

# Static checks: doc lint + code conventions
check:
	$(PYTHON) $(S)/harness.ci/scripts/lint_runner.py

# Validate lint rule YAML files
ast-rules:
	$(PYTHON) $(S)/harness.linters/scripts/code-quality/validate_lint_rules.py policies/ast-grep/

# Run ast-grep scan on src/
ast-scan:
	ast-grep scan --rule policies/ast-grep/ src/

# Structural architecture tests only
structural:
	pytest $(S)/harness.linters/scripts/architecture/test_layer_dependencies.py

# Full test suite: check + structural
test:
	make check
	make structural

# CI-equivalent local run
ci:
	make test

# Generators
build:
	$(PYTHON) $(S)/harness.generators/scripts/build_handbook.py

todo-sync:
	$(PYTHON) $(S)/harness.generators/scripts/sync_todo_registry.py

sync-skills:
	$(PYTHON) $(S)/harness.generators/scripts/sync_skills_to_agents.py

sync-indexes:
	$(PYTHON) $(S)/harness.generators/scripts/sync_doc_indexes.py

# Health
entropy:
	$(PYTHON) $(S)/harness.linters/scripts/entropy/entropy_check.py

review:
	$(PYTHON) $(S)/harness.ci/scripts/pre_pr_gate.py

gardener:
	$(PYTHON) $(S)/harness.linters/scripts/doc-health/doc_health_check.py

# Observability
obs-up:
	$(PYTHON) $(S)/harness.generators/scripts/observability/structured_log.py up

obs-down:
	$(PYTHON) $(S)/harness.generators/scripts/observability/structured_log.py down
