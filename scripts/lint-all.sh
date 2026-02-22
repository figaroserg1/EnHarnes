#!/usr/bin/env bash
set -euo pipefail

python3 scripts/custom_linter.py
python3 tools/linters/dependency_guard.py

echo "TODO: [AI] Добавить project-specific линтеры"
