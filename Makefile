.PHONY: smoke check structural test ci build tools todo-sync entropy review dev obs-up obs-down seed gardener

# Fast sanity: doc linter only (~5s)
smoke:
	python3 scripts/linters/custom_linter.py

# Static checks: harness lint script (doc linter + Python source guard)
check:
	bash scripts/linters/lint.sh

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
	bash scripts/generators/build_handbook.sh

tools:
	@echo "TODO: setup script not yet implemented"

todo-sync:
	python3 scripts/generators/sync_todo_registry.py

entropy:
	bash scripts/health/entropy-check.sh

review:
	bash scripts/health/agent_self_review.sh

dev:
	bash scripts/dev/dev-start.sh

obs-up:
	bash scripts/observability/obs-up.sh

obs-down:
	bash scripts/observability/obs-down.sh

seed:
	bash scripts/dev/seed-dev-data.sh

gardener:
	bash scripts/health/doc_gardener.sh
