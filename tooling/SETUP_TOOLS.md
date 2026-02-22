# Tools setup (MCP + Skills)

Этот файл специально вынесен отдельно, чтобы каждый мог подправить команды под свою среду.

## 1) Проверка базовых зависимостей
```bash
python3 --version
node --version
npm --version
```

## 2) Пример установки MCP tooling
> TODO: [HUMAN] Подставить актуальный MCP-клиент под вашу экосистему.

```bash
# EXAMPLE (REPLACE ME): установка условного MCP CLI
npm install -g @modelcontextprotocol/cli

# EXAMPLE (REPLACE ME): инициализация конфигурации
mcp init
```

## 3) Пример подключения MCP серверов
> TODO: [AI->HUMAN] Спросить у команды список нужных MCP серверов и доступов.

```bash
# EXAMPLE (REPLACE ME): файловый MCP
mcp server add filesystem -- npx -y @modelcontextprotocol/server-filesystem .

# EXAMPLE (REPLACE ME): git MCP
mcp server add git -- npx -y @modelcontextprotocol/server-git .
```

## 4) Пример установки skills для агента
> TODO: [HUMAN] Заменить путь/репозиторий навыков на ваш.

```bash
# EXAMPLE (REPLACE ME): создать локальную папку skills
mkdir -p "$HOME/.codex/skills"

# EXAMPLE (REPLACE ME): склонировать набор skills
git clone https://github.com/<org>/<skills-repo>.git "$HOME/.codex/skills/<skills-repo>"
```

## 5) Проверка, что всё поднялось
```bash
# EXAMPLE (REPLACE ME)
mcp server list

# EXAMPLE (REPLACE ME)
ls "$HOME/.codex/skills"
```
