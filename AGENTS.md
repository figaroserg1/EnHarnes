# AGENTS.md

Короткая карта для кодовых агентов.

## Mission
Поддерживать репозиторий как универсальный scaffold для agent-first разработки.

## Где что искать
- Старт для человека: `README.md`, `QUICKSTART.md`, `METHOD.md`
- Основные шаблоны: `docs/system-spec.md`, `docs/rules.md`, `docs/architecture.md`
- Реестр незаполненного: `docs/todo-registry.md`
- Референсы: `docs/references.md`
- Сетап тулов: `tooling/SETUP_TOOLS.md`
- Технические проверки: `scripts/custom_linter.py`, `scripts/custom_builder.sh`

## Working rules
1. Не удаляй TODO, пока нет фактического содержимого.
2. Любой пример помечай `EXAMPLE (REPLACE ME)`.
3. Для каждого TODO указывай owner: `[HUMAN]`, `[AI]`, `[AI->HUMAN]`.
4. Изменения, затрагивающие структуру, синхронизируй с `ARCHITECTURE.md` и `docs/todo-registry.md`.
