.PHONY: lint build tools todo-sync

lint:
	python3 scripts/custom_linter.py

build:
	bash scripts/custom_builder.sh

tools:
	bash tooling/setup-tools.sh

todo-sync:
	python3 scripts/sync_todo_registry.py
