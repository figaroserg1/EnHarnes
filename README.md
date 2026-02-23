# EnHarnes — universal agent-first repo scaffold

Шаблон репозитория, выровненный под подход Harness Engineering: **Humans steer, agents execute**.

## Что внутри (каркас agent-first)
- `AGENTS.md` — короткая карта для агента (не энциклопедия).
- `ARCHITECTURE.md` — high-level границы и dependency rules.
- `docs/` — единый versioned источник знаний (specs, design, reliability, security, quality).
- `scripts/` — воспроизводимые команды запуска, проверок, observability и данных.
- `tools/` — custom linters, structural tests, agent skills.
- `.github/workflows/ci.yml` — базовый CI для code+docs проверок.

## Быстрый старт
1. Прочитать `QUICKSTART.md`.
2. Заполнить policy-слой: `docs/design-docs/system-spec.md`, `docs/design-docs/rules.md`.
3. Заполнить design-слой: `docs/design-docs/architecture.md`, `docs/adr/`.
4. Настроить tooling по `tooling/SETUP_TOOLS.md`.
5. Запустить проверки:

```bash
make lint
make build
```

## Правила заполнения шаблона
- TODO только с owner: `[HUMAN]`, `[AI]`, `[AI->HUMAN]`.
- Любой пример помечать как `EXAMPLE (REPLACE ME)`.
- Структурные изменения синхронизировать с `ARCHITECTURE.md` и `docs/todo-registry.md`.
