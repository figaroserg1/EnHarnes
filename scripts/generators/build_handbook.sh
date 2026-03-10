#!/usr/bin/env bash
# =============================================================================
# custom_builder.sh — Сборка единого project-handbook.md из ключевых документов
# =============================================================================
#
# ЧТО ДЕЛАЕТ:
#   Конкатенирует основные документы проекта (README, METHOD, QUICKSTART,
#   ARCHITECTURE, system-spec, rules, architecture) в один файл
#   dist/project-handbook.md с разделителями и указанием источника каждой секции.
#
# ЗАЧЕМ НУЖЕН:
#   Единый файл-справочник удобен для передачи в LLM-контекст или для чтения
#   целиком, когда нужно быстро понять весь проект. Вместо того чтобы открывать
#   7 файлов по отдельности, агент или человек читает один handbook.
#
# ИСПОЛЬЗОВАНИЕ:
#   bash scripts/custom_builder.sh
#
# ВЫХОДНОЙ ФАЙЛ:
#   dist/project-handbook.md
# =============================================================================
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
OUT_FILE="$DIST_DIR/project-handbook.md"

mkdir -p "$DIST_DIR"

{
  echo "# Project handbook (generated)"
  echo
  echo "_Generated from core Phase 1 docs._"
  echo
  for f in \
    "$ROOT_DIR/README.md" \
    "$ROOT_DIR/METHOD.md" \
    "$ROOT_DIR/QUICKSTART.md" \
    "$ROOT_DIR/ARCHITECTURE.md" \
    "$ROOT_DIR/docs/design-docs/system-spec.md" \
    "$ROOT_DIR/docs/design-docs/rules.md" \
    "$ROOT_DIR/docs/design-docs/architecture.md"; do
    echo "\n---\n"
    echo "## Source: ${f#$ROOT_DIR/}"
    echo
    cat "$f"
    echo
  done
} > "$OUT_FILE"

echo "Generated: $OUT_FILE"
