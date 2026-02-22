# QUICKSTART: порядок работы с шаблоном

## Шаг 0. Прочитать метод
- Открой `METHOD.md`.
- Открой `approach.md` (источник идей и rationale).

## Шаг 1. Зафиксировать контекст продукта
Заполни `docs/system-spec.md` строго в порядке:
1. Project identity
2. Problem statement
3. Users & stakeholders
4. Scope
5. Functional requirements
6. Non-functional requirements
7. Risks / assumptions
8. Open questions

Если не хватает данных — ставь `TODO: [AI->HUMAN]` и список вопросов.

## Шаг 2. Зафиксировать правила
Заполни `docs/rules.md`:
1. Product rules
2. Engineering rules
3. AI agent rules
4. Documentation rules

## Шаг 3. Зафиксировать архитектуру
- Заполни `docs/architecture.md`.
- Сверь high-level карту в `ARCHITECTURE.md`.
- При решениях добавляй ADR в `docs/adr/`.

## Шаг 4. Настроить тулы агента
- Пройди `tooling/SETUP_TOOLS.md` (MCP + skills).
- При необходимости адаптируй `tooling/setup-tools.sh`.

## Шаг 5. Прогнать проверки
```bash
make lint
make build
```

## Шаг 6. Закрыть TODO реестр
- Обнови `docs/todo-registry.md`.
- Удали или замени `EXAMPLE (REPLACE ME)` по мере заполнения.
