#!/usr/bin/env bash
set -euo pipefail

echo "Stopping observability stack..."

docker compose -f observability.yml down || true
