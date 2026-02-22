#!/usr/bin/env bash
set -euo pipefail

echo "Starting local observability stack..."

docker compose -f observability.yml up -d || true
