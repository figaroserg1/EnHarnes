#!/usr/bin/env bash
set -euo pipefail

# Минимальная рабочая сборка/валидация шаблона.
# TODO: заменить на реальные команды проекта (make test, npm test, cargo test и т.д.)
# Owner: AI->HUMAN
# Status: TODO

echo "[build] Запуск scaffold checks..."
bash scripts/custom-linter.sh

echo "[build] TODO: подключить реальные шаги сборки."
echo "[build] OK"
