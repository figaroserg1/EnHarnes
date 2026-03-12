.PHONY: smoke check structural ast-rules test ci build tools todo-sync sync-skills sync-indexes entropy review dev obs-up obs-down seed gardener

# Python interpreter — override on Windows: make check PYTHON=python
PYTHON ?= python3

# Fast sanity: doc linter only (~5s)
smoke:
	$(PYTHON) scripts/linters/custom_linter.py

# Static checks: harness lint script (doc linter + Python source guard)
check:
	$(PYTHON) scripts/linters/lint.py

# Validate ast-grep rule YAML files
ast-rules:
	$(PYTHON) scripts/linters/validate-ast-rules.py rules/ast-grep/

# Run ast-grep scan on src/ (requires: pip install ast-grep-cli or cargo install ast-grep)
ast-scan:
	ast-grep scan --rule rules/ast-grep/ src/

# Structural architecture tests only
structural:
	pytest scripts/structural-tests/test_layer_dependencies.py

# Full test suite: check + structural
test:
	make check
	make structural

# CI-equivalent local run — same as make test
ci:
	make test

# Supporting targets
build:
	$(PYTHON) scripts/generators/build_handbook.py

tools:
	@echo "TODO: setup script not yet implemented"

todo-sync:
	$(PYTHON) scripts/generators/sync_todo_registry.py

# Sync skill AGENTS.md entries into AGENTS.md Reference Table
sync-skills:
	$(PYTHON) scripts/generators/sync_skills_to_agents.py

# Regenerate index.md files in doc directories
sync-indexes:
	$(PYTHON) scripts/generators/sync_doc_indexes.py

entropy:
	$(PYTHON) scripts/health/entropy_check.py

review:
	$(PYTHON) scripts/health/agent_self_review.py

dev:
	bash scripts/dev/dev-start.sh

obs-up:
	bash scripts/observability/obs-up.sh

obs-down:
	bash scripts/observability/obs-down.sh

seed:
	bash scripts/dev/seed-dev-data.sh

gardener:
	$(PYTHON) scripts/health/doc_gardener.py
