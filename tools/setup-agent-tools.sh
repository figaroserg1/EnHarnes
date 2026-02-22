#!/usr/bin/env bash
set -euo pipefail

# Setup tools for AI agents (skills + MCP)
# Этот файл можно запускать частями. Команды ниже — прямые шаблоны.
# Обязательно адаптировать под ваш runtime.

echo "[setup] Skills / MCP setup template"

echo "\n# 1) Skills: установить curated skill (пример, REPLACE ME)"
echo "codex skills install skill-creator"
echo "codex skills install skill-installer"

echo "\n# 2) Skills: установить из GitHub (пример, REPLACE ME)"
echo "codex skills install github.com/<org>/<repo>/path/to/skill"

echo "\n# 3) MCP: добавить сервер (пример, REPLACE ME)"
echo "codex mcp add docs --command \"npx -y @modelcontextprotocol/server-filesystem /path/to/docs\""
echo "codex mcp add github --command \"npx -y @modelcontextprotocol/server-github\""

echo "\n# 4) MCP: проверить подключение"
echo "codex mcp list"

echo "\n# TODO checklist"
echo "- TODO: Указать точные skill-репозитории вашей команды. (Owner: HUMAN)"
echo "- TODO: Указать рабочие MCP команды под вашу ОС/CI. (Owner: AI->HUMAN)"
echo "- TODO: Добавить аутентификацию (tokens/secrets) через безопасный менеджер. (Owner: HUMAN)"
