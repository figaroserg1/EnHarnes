.PHONY: lint-todos lint-src lint-structural lint-yaml lint-ast lint ci check-docs check-entropy review gen-handbook sync-todos sync-skills sync-indexes worktree obs-up obs-down install-hooks

# Python interpreter. Auto-detects python3 then python; override: make lint PYTHON=/path/to/python
PYTHON ?= $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null || echo python3)
S = .claude/skills

# === Linters (CI-blocking) ===

# TODO ownership & placeholder checks (~5s) + misfiled-plan check
lint-todos:
	$(PYTHON) $(S)/harness.linters/scripts/doc-health/todo_linter.py
	$(PYTHON) $(S)/harness.linters/scripts/doc-health/misfiled_plans.py

# Code conventions: bare print, kebab-case, file size + hook-registration check
lint-src:
	$(PYTHON) $(S)/harness.linters/scripts/code-health/code_conventions.py
	$(PYTHON) $(S)/harness.linters/scripts/code-health/hooks_registered.py

# Architecture boundary tests (pytest)
lint-structural:
	pytest $(S)/harness.linters/scripts/architecture-health/test_layer_dependencies.py

# Validate ast-grep rule YAML files
lint-yaml:
	$(PYTHON) $(S)/harness.linters/scripts/code-health/validate_lint_rules.py policies/ast-grep/

# Run ast-grep scan on src/
lint-ast:
	ast-grep scan --rule policies/ast-grep/ src/

# Composite: all CI-blocking linters
lint: lint-todos lint-src lint-structural

# CI alias
ci: lint

# === Health checks (periodic) ===

# Doc health: stale headers, broken links
check-docs:
	$(PYTHON) $(S)/harness.linters/scripts/doc-health/doc_health_check.py

# Entropy: orphan scripts, blank setpoints
check-entropy:
	$(PYTHON) $(S)/harness.linters/scripts/entropy/entropy_check.py

# === Pre-PR gate ===

# Pre-PR self-review (4 gates)
review:
	$(PYTHON) $(S)/harness.linters/scripts/pre_pr_gate.py

# === Generators ===

gen-handbook:
	$(PYTHON) $(S)/harness.generators/scripts/build_handbook.py

sync-todos:
	$(PYTHON) $(S)/harness.generators/scripts/sync_todo_registry.py

sync-skills:
	$(PYTHON) $(S)/harness.generators/scripts/sync_skills_to_agents.py

sync-indexes:
	$(PYTHON) $(S)/harness.generators/scripts/sync_doc_indexes.py

# === Dev tools ===

# Install hooks: git pre-commit (runs make lint) + Claude Code hooks
# (registers validate-bash / prompt-validator / post-response-sync / log-agent-usage
#  into the operator-local .claude/settings.json; idempotent).
install-hooks:
	cp scripts/harness/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit
	@echo "Pre-commit (git) hook installed."
	$(PYTHON) $(S)/harness.generators/scripts/install_claude_hooks.py

# Worktree bootstrap
worktree:
	$(PYTHON) scripts/harness/worktree_boot.py $(TASK)

# Observability
obs-up:
	$(PYTHON) $(S)/harness.generators/scripts/observability/structured_log.py up

obs-down:
	$(PYTHON) $(S)/harness.generators/scripts/observability/structured_log.py down
