.PHONY: smoke check structural test ci build tools todo-sync entropy review dev obs-up obs-down seed gardener

# Fast sanity: doc linter only (~5s)
smoke:
	python3 scripts/custom_linter.py

# Static checks: harness lint script (doc linter + Python source guard)
check:
	bash scripts/harness/lint.sh

# Structural architecture tests only
structural:
	bash scripts/structural-tests.sh

# Full test suite: check + structural
test:
	make check
	make structural

# CI-equivalent local run — same as make test
ci:
	make test

# Supporting targets
build:
	bash scripts/custom_builder.sh

tools:
	bash tooling/setup-tools.sh

todo-sync:
	python3 scripts/sync_todo_registry.py

entropy:
	bash scripts/entropy-check.sh

review:
	bash scripts/agent_self_review.sh

dev:
	bash scripts/dev-start.sh

obs-up:
	bash scripts/obs-up.sh

obs-down:
	bash scripts/obs-down.sh

seed:
	bash scripts/seed-dev-data.sh

gardener:
	bash scripts/doc_gardener.sh
