# Project handbook (generated)

_Generated from core Phase 1 docs._


---

## Source: README.md

# EnHarnes — Phase 1: AI Coding Agent Infrastructure

Репозиторий переведён в стартовую фазу проекта: мы строим инфраструктуру для инженерного цикла с AI coding-агентом по подходу Harness Engineering ("Humans steer, agents execute").

## Текущий фокус
- Описать рабочий контур агента, роли человека и гарантии безопасности.
- Подготовить минимально-исполняемую инфраструктуру для lint/build/test/doc-check циклов.
- Зафиксировать TODO по продуктовой специфике, которая будет определена позже.

## Карта репозитория
- `AGENTS.md` — краткие правила и навигация для агента.
- `ARCHITECTURE.md` — high-level устройство текущей фазы.
- `docs/` — живой source of truth (policy, design, reliability, security, execution plans).
- `scripts/` — линтеры, проверки здоровья, генераторы, dev-утилиты.
- `policies/` — machine-readable политики (risk-policy, setpoints, review config).

## Что пока неизвестно
- TODO: [HUMAN] Зафиксировать домен и продуктовую цель Phase 2.
- TODO: [HUMAN] Утвердить стек runtime и целевую платформу деплоя.
- TODO: [AI->HUMAN] Предложить стартовый backlog после discovery.

## Базовые команды
```bash
make smoke    # быстрая проверка (~5с)
make check    # статические проверки
make test     # полный набор тестов
```



---

## Source: METHOD.md

_File not found: METHOD.md_



---

## Source: QUICKSTART.md

_File not found: QUICKSTART.md_



---

## Source: ARCHITECTURE.md

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



---

## Source: docs/design-docs/system-spec.md

# System Specification — Phase 1

## 1) Mission for current phase
- Построить инфраструктуру инженерного цикла для AI coding-агента.
- Сохранить независимость от конкретного домена до завершения discovery.

## 2) Problem statement
- TODO: [HUMAN] Определить бизнес-проблему, которую решает продукт.
- TODO: [AI] Подготовить варианты problem framing после интервью со стейкхолдерами.

## 3) Stakeholders
- TODO: [HUMAN] Назначить владельца продукта и технического владельца.
- TODO: [AI->HUMAN] Уточнить список ролей, которые будут работать с агентом.

## 4) Scope boundaries
### In scope now
- CI/локальные проверки (lint/build/test).
- Документированный процесс внесения изменений агентом.

### Out of scope now
- Конкретная бизнес-логика продукта.
- Доменные интеграции и production rollout.

## 5) Quality goals
- TODO: [HUMAN] Утвердить критерии готовности Phase 1.
- TODO: [AI] Предложить измеримые метрики качества контуров разработки.



---

## Source: docs/design-docs/rules.md

_File not found: docs/design-docs/rules.md_



---

## Source: docs/design-docs/architecture.md

_File not found: docs/design-docs/architecture.md_

