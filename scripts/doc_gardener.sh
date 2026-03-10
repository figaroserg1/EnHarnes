#!/usr/bin/env bash
# =============================================================================
# doc_gardener.sh — Комплексная проверка здоровья документации
# =============================================================================
#
# ЧТО ДЕЛАЕТ:
#   Выполняет 5 проверок качества документации:
#     1. Stale verification headers — находит docs/*.md с заголовками
#        «Verified: YYYY-MM-DD» старше 30 дней. Это значит, что документ
#        давно не верифицировался и может быть устаревшим.
#     2. Broken internal links — находит ссылки [text](path) в markdown,
#        где path не ведёт на существующий файл.
#     3. Sparse index files — проверяет, что index.md файлы в docs/
#        содержат хотя бы 5 строк (иначе это placeholder, а не индекс).
#     4. Doc lint — запускает custom_linter.py (TODO-маркеры, EXAMPLE-
#        плейсхолдеры, именование файлов).
#     5. Doc drift — запускает check_doc_drift.py (ссылки из
#        risk-policy.json ведут на реальные файлы).
#
# ЗАЧЕМ НУЖЕН:
#   Документация деградирует быстрее кода: ссылки ломаются, файлы не
#   обновляются, индексы остаются пустыми. Этот скрипт автоматизирует
#   «прополку» — регулярный аудит здоровья документации. Рекомендуется
#   запускать периодически или перед крупными релизами.
#
# ИСПОЛЬЗОВАНИЕ:
#   bash scripts/doc_gardener.sh
#
# КОД ВОЗВРАТА:
#   0 — документация в порядке
#   1 — найдены проблемы, требующие внимания
# =============================================================================
set -euo pipefail

echo "=== Doc Gardener ==="
ISSUES=0

# 1. Find stale verification headers (older than 30 days)
echo ""
echo "-- Stale verification headers --"
THIRTY_DAYS_AGO=$(date -d "30 days ago" +%Y-%m-%d 2>/dev/null || date -v-30d +%Y-%m-%d 2>/dev/null || echo "")
if [ -n "$THIRTY_DAYS_AGO" ]; then
  while IFS= read -r file; do
    DATE=$(grep -oP '(?<=Verified: )\d{4}-\d{2}-\d{2}' "$file" 2>/dev/null | head -1)
    if [ -n "$DATE" ] && [[ "$DATE" < "$THIRTY_DAYS_AGO" ]]; then
      echo "  STALE ($DATE): $file"
      ISSUES=$((ISSUES + 1))
    fi
  done < <(find docs/ -name "*.md" 2>/dev/null)
else
  echo "  [SKIP] date calculation not available on this platform"
fi

# 2. Find broken internal links in markdown docs
echo ""
echo "-- Broken internal references --"
while IFS= read -r file; do
  grep -oP '\[.*?\]\((?!http)([^)]+)\)' "$file" 2>/dev/null | grep -oP '\(([^)]+)\)' | tr -d '()' | while read -r ref; do
    ref_path="${ref%%#*}"
    if [ -n "$ref_path" ] && [ ! -f "$ref_path" ] && [ ! -f "$(dirname "$file")/$ref_path" ]; then
      echo "  BROKEN: $file -> $ref_path"
      ISSUES=$((ISSUES + 1))
    fi
  done
done < <(find docs/ -name "*.md" 2>/dev/null)

# 3. Find indexes that are sparse (likely still placeholders)
echo ""
echo "-- Sparse index files --"
for idx_file in docs/design-docs/index.md docs/product-specs/index.md docs/references/index.md; do
  if [ -f "$idx_file" ]; then
    LINES=$(wc -l < "$idx_file")
    if [ "$LINES" -lt 5 ]; then
      echo "  SPARSE: $idx_file ($LINES lines)"
      ISSUES=$((ISSUES + 1))
    fi
  fi
done

# 4. Run the doc linter (TODO ownership, EXAMPLE markers)
echo ""
echo "-- Doc lint --"
python3 scripts/custom_linter.py || ISSUES=$((ISSUES + 1))

# 5. Check risk-policy.json doc references
echo ""
echo "-- Doc drift references --"
python3 scripts/check_doc_drift.py || ISSUES=$((ISSUES + 1))

echo ""
if [ "$ISSUES" -gt 0 ]; then
  echo "Doc gardener found $ISSUES area(s) needing attention."
  exit 1
else
  echo "OK: docs are healthy."
fi
