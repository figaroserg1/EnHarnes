# ARCHITECTURE: high-level карта Phase 1

## Основные зоны
- `docs/` — политики, дизайн-ориентиры, планы исполнения.
- `scripts/` — исполняемый слой: линтеры, проверки здоровья, генераторы, dev-утилиты.
- `policies/` — machine-readable политики (risk-policy, setpoints, review config).

## Логика слоёв
1. **Policy layer**: `docs/design-docs/system-spec.md`, `.claude/skills/harness.core/docs/WORKFLOW_RULES.md`.
2. **Design layer**: `docs/design-docs/`, `docs/PROJECT_DESIGN.md`.
3. **Execution layer**: `scripts/`, `Makefile`.
4. **Reliability & Security layer**: `docs/PROJECT_RELIABILITY.md`, `docs/PROJECT_SECURITY.md`, `docs/PROJECT_OBSERVABILITY.md`.
5. **Planning layer**: `.claude/skills/harness.plan/OPENAI_PLANS.md`, `docs/exec-plans/`.


**Архитектура исходного кода (`src/`):**

> **NOTE:** The layers below are an EXAMPLE for this project (EnHarnes). When bootstrapping a new project, define your own layers in `policies/architecture.yaml` based on your RFP — do NOT copy these verbatim.

Каждый бизнес-домен продукта имеет строго фиксированную структуру папок. Зависимости могут идти **только в одном направлении** по цепочке, определённой в `policies/architecture.yaml`. Агент обязан парсить данные на границах этих слоев.

Пример слоёв (для типичного full-stack приложения):
*   **`Types/`** — типы и схемы данных.
*   **`Config/`** — конфигурация домена.
*   **`Repo/`** — логика базы данных.
*   **`Service/`** — бизнес-логика.
*   **`Runtime/`** — исполняемый слой.
*   **`UI/`** — пользовательский интерфейс.
*   **`Providers/`** — единственная точка входа для всех сквозных функций.

## Quality Grades

| Zone | Description | Grade |
|------|-------------|-------|
| docs/ | Policies, design, plans — well-structured | A |
| scripts/ | Linters, health checks, generators, dev utils | B |
| policies/ | Machine-readable policies (risk, setpoints, review) | A |
| src/ | Product code — not yet started (Phase 1) | — |

Grade scale: **A** = well-tested, documented, stable. **B** = functional, room for improvement. **C** = works but needs attention. **D** = tech debt, needs refactoring.

## Ограничения текущей фазы
- TODO: [HUMAN] Зафиксировать границы доступа агента к прод-средам.
- TODO: [AI] Добавить диаграмму потока "задача → изменение → проверка → отчёт".
