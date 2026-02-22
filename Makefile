.PHONY: lint build tools

lint:
	python3 scripts/custom_linter.py

build:
	bash scripts/custom_builder.sh

tools:
	bash tooling/setup-tools.sh
