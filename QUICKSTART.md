# QUICKSTART: запуск scaffold по Harness Engineering

## Шаг 0. Прочитать основу
- `METHOD.md`
- `approach.md`
- `AGENTS.md`

## Шаг 1. Зафиксировать цель и рамки
- Заполни `docs/system-spec.md`.
- Заполни `docs/rules.md`.

## Шаг 2. Зафиксировать архитектуру
- Заполни `docs/architecture.md`.
- Синхронизируй high-level карту в `ARCHITECTURE.md`.
- Добавляй решения в `docs/adr/`.

## Шаг 3. Настроить выполняемые команды для агента
- `scripts/dev-start.sh`
- `scripts/lint-all.sh`
- `scripts/test-all.sh`
- `scripts/seed-dev-data.sh`
- `scripts/obs-up.sh` / `scripts/obs-down.sh`

## Шаг 4. Подготовить docs как single source of truth
- Product: `docs/product-specs/`
- Design: `docs/design-docs/`
- Reliability/Security/Quality: `docs/RELIABILITY.md`, `docs/SECURITY.md`, `docs/QUALITY_SCORE.md`
- Планы: `docs/PLANS.md`, `docs/exec-plans/`

## Шаг 5. Прогнать проверки
```bash
make lint
make build
bash scripts/test-all.sh
```

## Шаг 6. Синхронизировать реестр TODO
- Обнови `docs/todo-registry.md`.
