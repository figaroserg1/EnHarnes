#!/usr/bin/env bash
# =============================================================================
# harness/typecheck.sh — Универсальная проверка типов с автоопределением стека
# =============================================================================
#
# ЧТО ДЕЛАЕТ:
#   Автоматически определяет тип проекта и запускает подходящий type checker:
#     - Rust (Cargo.toml)    → cargo check
#     - Node.js (package.json) → npm run typecheck (если скрипт есть)
#     - Python (pyproject.toml/requirements.txt) → pyright или mypy
#       (что установлено)
#   Можно переопределить через переменную HARNESS_TYPECHECK_CMD.
#
# ЗАЧЕМ НУЖЕН:
#   Аналогично lint.sh — единый интерфейс для проверки типов независимо
#   от языка проекта. Type checking ловит целый класс ошибок на этапе
#   статического анализа, до запуска кода. Особенно важен для агентов,
#   которые генерируют код: type checker верифицирует корректность
#   сгенерированных типов и интерфейсов.
#
# ИСПОЛЬЗОВАНИЕ:
#   bash scripts/harness/typecheck.sh
#   или: make typecheck
#   или: HARNESS_TYPECHECK_CMD="mypy src/" make typecheck
# =============================================================================
set -euo pipefail

#root is 2 levels above
root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)

if [ -n "${HARNESS_TYPECHECK_CMD:-}" ]; then
  cd "$root_dir"
  eval "$HARNESS_TYPECHECK_CMD"
  exit 0
fi

#Rust
if [ -f "$root_dir/Cargo.toml" ] && command -v cargo >/dev/null 2>&1; then
  cd "$root_dir"
  cargo check --quiet
  exit 0
fi

#TypeScript/JS
if [ -f "$root_dir/package.json" ] && command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
  cd "$root_dir"
  if node -e 'const p=require("./package.json"); process.exit(p.scripts&&p.scripts.typecheck?0:1)' >/dev/null 2>&1; then
    npm run -s typecheck
    exit 0
  fi
fi

#Python
if [ -f "$root_dir/pyproject.toml" ] || [ -f "$root_dir/requirements.txt" ]; then
  cd "$root_dir"
  if command -v pyright >/dev/null 2>&1; then
    pyright
    exit 0
  fi
  if command -v mypy >/dev/null 2>&1; then
    mypy src/
    exit 0
  fi
  echo "[typecheck] No type checker found (pyright/mypy). Skipping — install one to enable."
  exit 0
fi

echo "No default typecheck command detected."
echo "Set HARNESS_TYPECHECK_CMD or customize scripts/harness/typecheck.sh."
exit 1
