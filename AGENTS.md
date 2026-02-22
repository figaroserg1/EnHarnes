# AGENTS.md

Короткая карта для кодовых агентов.

## Mission
Поддерживать репозиторий как универсальный scaffold для agent-first разработки.

## Где что искать
- Старт для человека: `README.md`, `QUICKSTART.md`, `METHOD.md`
- High-level структура: `ARCHITECTURE.md`
- Policy и design: `docs/system-spec.md`, `docs/rules.md`, `docs/architecture.md`
- Reliability/security/quality: `docs/RELIABILITY.md`, `docs/SECURITY.md`, `docs/QUALITY_SCORE.md`
- Планы: `.agent/PLANS.md`, `docs/PLANS.md`, `docs/exec-plans/`
- Реестр незаполненного: `docs/todo-registry.md`
- Технические проверки: `scripts/custom_linter.py`, `scripts/custom_builder.sh`

## Working rules
1. Не удаляй TODO, пока нет фактического содержимого.
2. Любой пример помечай `EXAMPLE (REPLACE ME)`.
3. Для каждого TODO указывай owner: `[HUMAN]`, `[AI]`, `[AI->HUMAN]`.
4. Изменения структуры синхронизируй с `ARCHITECTURE.md` и `docs/todo-registry.md`.

## ExecPlans
Для сложных фич и рефакторингов используй ExecPlan по `.agent/PLANS.md`.
