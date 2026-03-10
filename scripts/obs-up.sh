#!/usr/bin/env bash
# =============================================================================
# obs-up.sh — Запуск локального observability-стека
# =============================================================================
#
# ЧТО ДЕЛАЕТ:
#   Заглушка (placeholder). В будущем будет поднимать контейнеры для
#   сбора логов, метрик и трейсов — например,
#   docker compose -f observability.compose.yml up -d.
#
# ЗАЧЕМ НУЖЕН:
#   Observability — ключевая часть agent-first workflow. Агенты и люди
#   должны видеть что происходит в системе в реальном времени. На Phase 1
#   используется obs.py (файловый JSON), но на Phase 2/3 появятся
#   полноценные Vector → Loki → Grafana.
#
# СТАТУС: placeholder — требует реализации (Phase 2/3 obs).
# =============================================================================
set -euo pipefail

echo "TODO: [AI] Поднять локальный observability stack (logs/metrics/traces)"
echo "EXAMPLE (REPLACE ME): docker compose -f observability.compose.yml up -d"
