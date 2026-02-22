# Setup tools (MCP + Skills)

## 1) Базовые проверки окружения
```bash
python3 --version
git --version
gh --version
```

## 2) Минимальный runtime/toolchain проекта
- TODO: [HUMAN] Зафиксировать обязательный runtime (Node/Python/Go/...).
- TODO: [HUMAN] Зафиксировать единый package manager/build tool.

## 3) MCP: базовая установка (пример)
> TODO: [HUMAN] Подставить ваш MCP-клиент и поддерживаемые серверы.

```bash
# EXAMPLE (REPLACE ME)
npm install -g @modelcontextprotocol/cli
mcp init

# EXAMPLE (REPLACE ME)
mcp server add filesystem -- npx -y @modelcontextprotocol/server-filesystem .
mcp server add git -- npx -y @modelcontextprotocol/server-git .
```

## 4) Skills
- TODO: [AI->HUMAN] Уточнить обязательный список skills и зафиксировать в `tools/agent-skills/README.md`.

## 5) Проверка runnable-команд для агента
```bash
bash scripts/dev-start.sh
bash scripts/lint-all.sh
bash scripts/test-all.sh
bash scripts/obs-up.sh
bash scripts/obs-down.sh
```
