#!/usr/bin/env bash
set -euo pipefail

# Минимально рабочий кастомный линтер для scaffold-репозитория.
# Расширьте проверками проекта.

echo "[lint] Проверка TODO owner-меток..."

missing_owner=0
while IFS= read -r file; do
  # Если есть TODO, должен быть хотя бы один Owner в файле.
  if rg -n "TODO:" "$file" >/dev/null && ! rg -n "Owner:" "$file" >/dev/null; then
    echo "[lint][error] В файле $file есть TODO без Owner-меток"
    missing_owner=1
  fi
done < <(rg --files docs README.md METHOD.md)

if [[ "$missing_owner" -ne 0 ]]; then
  echo "[lint] FAIL"
  exit 1
fi

echo "[lint] Проверка REPLACE ME маркеров..."
rg -n "REPLACE ME" docs README.md METHOD.md || true

echo "[lint] OK"
