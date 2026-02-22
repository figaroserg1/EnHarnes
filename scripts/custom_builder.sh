#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$ROOT_DIR/dist"
OUT_FILE="$DIST_DIR/project-handbook.md"

mkdir -p "$DIST_DIR"

{
  echo "# Project handbook (generated)"
  echo
  echo "_Generated from scaffold core docs._"
  echo
  for f in \
    "$ROOT_DIR/README.md" \
    "$ROOT_DIR/METHOD.md" \
    "$ROOT_DIR/QUICKSTART.md" \
    "$ROOT_DIR/ARCHITECTURE.md" \
    "$ROOT_DIR/docs/system-spec.md" \
    "$ROOT_DIR/docs/rules.md" \
    "$ROOT_DIR/docs/architecture.md"; do
    echo "\n---\n"
    echo "## Source: ${f#$ROOT_DIR/}"
    echo
    cat "$f"
    echo
  done
} > "$OUT_FILE"

echo "Generated: $OUT_FILE"
