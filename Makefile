.PHONY: lint-todos lint structural ast-rules ast-scan test ci handbook todo-sync sync-skills sync-indexes entropy review doc-health worktree obs-up obs-down

# Python interpreter — override: make lint PYTHON=python3
PYTHON ?= python
S = .claude/skills

# TODO & placeholder linter (~5s)
lint-todos:
	$(PYTHON) $(S)/harness.linters/scripts/doc-health/doc_linter.py

# All static checks: doc lint + code conventions
lint:
	$(PYTHON) $(S)/harness.ci/scripts/lint_runner.py

# Validate ast-grep rule YAML files
ast-rules:
	$(PYTHON) $(S)/harness.linters/scripts/code-quality/validate_lint_rules.py policies/ast-grep/

# Run ast-grep scan on src/
ast-scan:
	ast-grep scan --rule policies/ast-grep/ src/

# Structural architecture tests (pytest)
structural:
	pytest $(S)/harness.linters/scripts/architecture/test_layer_dependencies.py

# Full test suite: lint + structural
test:
	make lint
	make structural

# CI-equivalent local run
ci:
	make test

# Generate project handbook
handbook:
	$(PYTHON) $(S)/harness.generators/scripts/build_handbook.py

# Sync generators
todo-sync:
	$(PYTHON) $(S)/harness.generators/scripts/sync_todo_registry.py

sync-skills:
	$(PYTHON) $(S)/harness.generators/scripts/sync_skills_to_agents.py

sync-indexes:
	$(PYTHON) $(S)/harness.generators/scripts/sync_doc_indexes.py

# Health checks
entropy:
	$(PYTHON) $(S)/harness.linters/scripts/entropy/entropy_check.py

doc-health:
	$(PYTHON) $(S)/harness.linters/scripts/doc-health/doc_health_check.py

# Pre-PR self-review (5 gates)
review:
	$(PYTHON) $(S)/harness.ci/scripts/pre_pr_gate.py

# Worktree bootstrap
worktree:
	$(PYTHON) scripts/harness/worktree_boot.py $(TASK)

# Observability
obs-up:
	$(PYTHON) $(S)/harness.generators/scripts/observability/structured_log.py up

obs-down:
	$(PYTHON) $(S)/harness.generators/scripts/observability/structured_log.py down
