#!/usr/bin/env bash
set -euo pipefail

make lint
make build

echo "TODO: [AI] Добавить запуск unit/integration/e2e тестов по мере появления кода"
