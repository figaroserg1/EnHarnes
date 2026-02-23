# ARCHITECTURE: high-level карта Phase 1

## Основные зоны
- `docs/` — политики, дизайн-ориентиры, планы исполнения.
- `scripts/` — исполняемый слой локальных проверок и операционных команд.
- `tools/` — статические проверки структуры и зависимостей.
- `tooling/` — установка и настройка локальных инструментов.

## Логика слоёв
1. **Policy layer**: `docs/design-docs/system-spec.md`, `docs/design-docs/rules.md`.
2. **Design layer**: `docs/design-docs/architecture.md`, `docs/DESIGN.md`.
3. **Execution layer**: `scripts/`, `Makefile`.
4. **Reliability & Security layer**: `docs/RELIABILITY.md`, `docs/SECURITY.md`, `docs/OBSERVABILITY.md`.
5. **Planning layer**: `docs/PLANS.md`, `docs/exec-plans/`.

## Ограничения текущей фазы
- TODO: [HUMAN] Зафиксировать границы доступа агента к прод-средам.
- TODO: [AI] Добавить диаграмму потока "задача → изменение → проверка → отчёт".
