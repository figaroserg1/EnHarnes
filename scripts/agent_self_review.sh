#!/usr/bin/env bash
set -euo pipefail

echo "Running agent self review..."

bash scripts/lint-all.sh
bash scripts/test-all.sh

echo "TODO: [AI] Добавить observability checks в self-review pipeline"
