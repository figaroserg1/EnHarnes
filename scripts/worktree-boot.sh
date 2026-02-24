#!/usr/bin/env bash
set -euo pipefail

# Worktree boot script: sets up a fresh worktree for an agent task.
#
# Usage:
#   ./scripts/worktree-boot.sh <task-name>
#
# This creates a worktree, installs dependencies, and runs smoke check.
# Each agent task gets an isolated copy of the repo with no shared state.

TASK_NAME="${1:?Usage: worktree-boot.sh <task-name>}"
WORKTREE_DIR="../worktree_${TASK_NAME}"
BRANCH_NAME="task/${TASK_NAME}"

echo "=== Worktree Boot: ${TASK_NAME} ==="

# 1. Create worktree
if [ -d "${WORKTREE_DIR}" ]; then
  echo "Worktree ${WORKTREE_DIR} already exists. Reusing."
else
  echo "Creating worktree at ${WORKTREE_DIR} on branch ${BRANCH_NAME}..."
  git worktree add "${WORKTREE_DIR}" -b "${BRANCH_NAME}"
fi

cd "${WORKTREE_DIR}"

# 2. Install dependencies (auto-detect runtime)
echo ""
echo "-- Installing dependencies --"
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt 2>/dev/null || pip install pytest
elif [ -f "package.json" ]; then
  if command -v bun &>/dev/null; then
    bun install
  elif command -v npm &>/dev/null; then
    npm install
  fi
elif [ -f "Cargo.toml" ]; then
  cargo build 2>/dev/null || true
else
  echo "No dependency file detected. Installing pytest for structural tests."
  pip install pytest 2>/dev/null || true
fi

# 3. Run smoke check
echo ""
echo "-- Running smoke check --"
if [ -f Makefile ] && make -n smoke &>/dev/null; then
  make smoke
else
  echo "No smoke target. Running basic checks..."
  make check 2>/dev/null || echo "[WARN] make check not available"
fi

echo ""
echo "=== Worktree ready at ${WORKTREE_DIR} (branch: ${BRANCH_NAME}) ==="
echo "To clean up: git worktree remove ${WORKTREE_DIR}"
