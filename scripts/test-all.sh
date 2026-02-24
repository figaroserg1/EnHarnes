#!/usr/bin/env bash
set -euo pipefail

make lint
make build
bash scripts/structural-tests.sh

echo "OK: base test suite completed (including structural dependency checks)"
