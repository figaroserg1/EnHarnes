# Setup tools (MCP + Skills)

Отдельный файл, который легко кастомизировать под команду.

## 1) Базовые проверки
```bash
python3 --version
git --version
gh --version
node --version
npm --version
```

## 2) MCP: базовая установка (пример)
> TODO: [HUMAN] Подставить ваш MCP-клиент и поддерживаемые серверы.

```bash
# EXAMPLE (REPLACE ME)
npm install -g @modelcontextprotocol/cli
mcp init

# EXAMPLE (REPLACE ME)
mcp server add filesystem -- npx -y @modelcontextprotocol/server-filesystem .
mcp server add git -- npx -y @modelcontextprotocol/server-git .
```

## 3) Skills: прямые команды для Codex агента

### 3.1 Установить curated skill из openai/skills
```bash
python3 /opt/codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo openai/skills \
  --path skills/.curated/<skill-name>
```

### 3.2 Установить skill из произвольного GitHub репозитория
```bash
python3 /opt/codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --repo <owner>/<repo> \
  --path <path/to/skill>
```

### 3.3 Установить skill по URL
```bash
python3 /opt/codex/skills/.system/skill-installer/scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/<repo>/tree/<ref>/<path-to-skill>
```

### 3.4 Посмотреть curated список навыков
```bash
python3 /opt/codex/skills/.system/skill-installer/scripts/list-curated-skills.py
```

> TODO: [AI->HUMAN] Уточнить, какие именно skills нужны команде и зафиксировать ниже:
- TODO: [HUMAN] Список обязательных skills.
- TODO: [HUMAN] Список optional skills.

## 4) Проверка после установки
```bash
# EXAMPLE (REPLACE ME)
mcp server list

# EXAMPLE (REPLACE ME)
ls "$HOME/.codex/skills"
```
