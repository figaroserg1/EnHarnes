#!/usr/bin/env bash
set -euo pipefail

echo "== EnHarnes tools setup helper =="

echo "[1/4] Versions"
python3 --version
git --version
if command -v gh >/dev/null 2>&1; then gh --version | head -n 1; else echo "TODO: [HUMAN] install gh"; fi
if command -v node >/dev/null 2>&1; then node --version; else echo "TODO: [HUMAN] install node"; fi
if command -v npm >/dev/null 2>&1; then npm --version; else echo "TODO: [HUMAN] install npm"; fi

echo "[2/4] MCP commands (EXAMPLE REPLACE ME)"
cat <<'CMDS'
npm install -g @modelcontextprotocol/cli
mcp init
mcp server add filesystem -- npx -y @modelcontextprotocol/server-filesystem .
mcp server add git -- npx -y @modelcontextprotocol/server-git .
CMDS

echo "[3/4] Skills installer commands"
cat <<'CMDS'
python3 /opt/codex/skills/.system/skill-installer/scripts/list-curated-skills.py
python3 /opt/codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo openai/skills --path skills/.curated/<skill-name>
python3 /opt/codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill>
CMDS

echo "[4/4] TODO: [HUMAN] Uncomment and adapt commands in this script for your team."
