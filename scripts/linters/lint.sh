#!/usr/bin/env bash
# =============================================================================
# harness/lint.sh — Универсальный линтер с автоопределением типа проекта
# =============================================================================
#
# ЧТО ДЕЛАЕТ:
#   Автоматически определяет тип проекта и запускает подходящий линтер:
#     - Rust (Cargo.toml)    → cargo clippy с -D warnings
#     - Node.js (package.json) → npm run lint (если скрипт lint есть)
#     - Python (pyproject.toml/requirements.txt) → custom_linter.py +
#       dependency_guard.py
#   Можно переопределить через переменную HARNESS_LINT_CMD.
#
# ЗАЧЕМ НУЖЕН:
#   EnHarnes — мета-фреймворк, который может работать с проектами на
#   разных языках. Этот скрипт абстрагирует конкретный линтер за единым
#   интерфейсом: `make check` всегда работает, независимо от стека.
#   Это позволяет агентам и CI использовать одну и ту же команду.
#
# ИСПОЛЬЗОВАНИЕ:
#   bash scripts/harness/lint.sh
#   или: make check
#   или: HARNESS_LINT_CMD="flake8 src/" make check
# =============================================================================
set -euo pipefail

root_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)

if [ -n "${HARNESS_LINT_CMD:-}" ]; then
  cd "$root_dir"
  eval "$HARNESS_LINT_CMD"
  exit 0
fi

if [ -f "$root_dir/Cargo.toml" ] && command -v cargo >/dev/null 2>&1; then
  cd "$root_dir"
  cargo clippy --all-targets --all-features -- -D warnings
  exit 0
fi

if [ -f "$root_dir/package.json" ] && command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
  cd "$root_dir"
  if node -e 'const p=require("./package.json"); process.exit(p.scripts&&p.scripts.lint?0:1)' >/dev/null 2>&1; then
    npm run -s lint
    exit 0
  fi
fi

if [ -f "$root_dir/pyproject.toml" ] || [ -f "$root_dir/requirements.txt" ]; then
  cd "$root_dir"
  python3 scripts/linters/custom_linter.py
  python3 scripts/linters/dependency_guard.py
  exit 0
fi

echo "No default lint command detected."
echo "Set HARNESS_LINT_CMD or customize scripts/harness/lint.sh."
exit 1
