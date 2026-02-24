#!/usr/bin/env bash
set -euo pipefail

pytest tools/structural-tests/test_layer_dependencies.py
