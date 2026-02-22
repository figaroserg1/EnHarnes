#!/usr/bin/env bash
set -euo pipefail

# This script is intentionally conservative and mostly prints commands.
# TODO: [HUMAN] Replace placeholder commands with your real toolchain setup.

echo "== EnHarnes tooling setup =="

echo "[1/3] Checking local dependencies..."
python3 --version
if command -v node >/dev/null 2>&1; then node --version; else echo "TODO: [HUMAN] install node"; fi
if command -v npm >/dev/null 2>&1; then npm --version; else echo "TODO: [HUMAN] install npm"; fi

echo "[2/3] Suggested MCP setup commands (REPLACE ME):"
cat <<'CMDS'
npm install -g @modelcontextprotocol/cli
mcp init
mcp server add filesystem -- npx -y @modelcontextprotocol/server-filesystem .
mcp server add git -- npx -y @modelcontextprotocol/server-git .
CMDS

echo "[3/3] Suggested skills setup commands (REPLACE ME):"
cat <<'CMDS'
mkdir -p "$HOME/.codex/skills"
git clone https://github.com/<org>/<skills-repo>.git "$HOME/.codex/skills/<skills-repo>"
CMDS

echo "Done. Edit tooling/SETUP_TOOLS.md and this script for your environment."
