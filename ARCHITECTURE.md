# ARCHITECTURE: high-level карта Phase 1

## Основные зоны
- `docs/` — политики, дизайн-ориентиры, планы исполнения.
- `scripts/` — исполняемый слой: линтеры, проверки здоровья, генераторы, dev-утилиты.
- `policies/` — machine-readable политики (risk-policy, setpoints, review config).

## Логика слоёв
1. **Policy layer**: `docs/design-docs/system-spec.md`, `docs/design-docs/rules.md`.
2. **Design layer**: `docs/design-docs/`, `docs/DESIGN.md`.
3. **Execution layer**: `scripts/`, `Makefile`.
4. **Reliability & Security layer**: `docs/RELIABILITY.md`, `docs/SECURITY.md`, `docs/OBSERVABILITY.md`.
5. **Planning layer**: `.claude/skills/harness-planner/OPENAI_PLANS.md`, `docs/exec-plans/`.


**Архитектура исходного кода (`src/`):**
Каждый бизнес-домен продукта (например, настройки приложения) имеет строго фиксированную структуру папок. Зависимости могут идти **только в одном направлении** по цепочке: `Types → Config → Repo → Service → Runtime → UI`. Агент обязан парсить данные на границах этих слоев (например, через Zod) [12-15].
*   **`Types/`** — типы и схемы данных.
*   **`Config/`** — конфигурация домена.
*   **`Repo/`** — логика базы данных.
*   **`Service/`** — бизнес-логика.
*   **`Runtime/`** — исполняемый слой.
*   **`UI/`** — пользовательский интерфейс.
*   **`Providers/`** — единственная точка входа для всех сквозных функций (авторизация, коннекторы, телеметрия, фиче-флаги). Прямые вызовы этих функций из других слоев запрещены [13, 15].

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
