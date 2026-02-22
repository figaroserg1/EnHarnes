# ARCHITECTURE (high-level map)

## Repository modules
- `docs/` — шаблоны проектной документации и референсы.
- `scripts/` — минимально полезные утилиты (линтер scaffold, сборка handbook, TODO sync).
- `tooling/` — установка и адаптация MCP + skills.
- `examples/` — примеры заполненных артефактов, которые нужно заменить под свой проект.

## Architecture principles (inspired by matklad `ARCHITECTURE.md`)
1. **Архитектура = управляемые зависимости**, а не диаграммы ради диаграмм.
2. **Слои направлены внутрь**: high-level policy не зависит от low-level implementation.
3. **API first между модулями**: границы фиксируются контрактами, а не «дружбой» через внутренности.
4. **Локальная простота важнее глобальной магии**: сложность должна быть изолирована внутри компонента.
5. **Изменения должны быть дешёвыми**: структура репозитория помогает безопасно менять код по частям.
6. **Тестируемость как свойство дизайна**: unit/integration границы соответствуют архитектурным границам.

## Target decomposition for this scaffold
- **Policy layer**: `docs/system-spec.md`, `docs/rules.md` (что и зачем строим).
- **Design layer**: `docs/architecture.md`, `docs/adr/` (как разрезаем систему и почему).
- **Execution layer**: `scripts/`, `tooling/` (как обеспечиваем повторяемый delivery).
- **Examples layer**: `examples/` (EXAMPLE (REPLACE ME) артефакты для ускорения старта).

## Dependency rules
- `examples/` не являются source-of-truth для policy и не должны переопределять `docs/`.
- `scripts/` могут читать документы из `docs/`, но не менять их семантику автоматически.
- `tooling/` поддерживает процессы, но не определяет продуктовые решения.
- Архитектурные решения фиксируются в `docs/adr/` и отражаются в `docs/architecture.md`.

## TODO
- TODO: [AI] Добавить в `docs/architecture.md` явную карту зависимостей между Policy/Design/Execution слоями.
- TODO: [AI->HUMAN] Зафиксировать в `docs/adr/` первый ADR с правилами направленности зависимостей.
- TODO: [HUMAN] Уточнить доменную архитектуру конкретного продукта и bounded contexts.
- TODO: [AI] Добавить checklist «architecture fitness checks» в `scripts/custom_linter.py`.

## EXAMPLE (REPLACE ME)
- Monorepo: `apps/web`, `apps/api`, `packages/common`, `infra/`.
