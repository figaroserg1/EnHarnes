# AGENTS.md

Короткая карта для кодовых агентов, которые используют этот репозиторий как шаблон.

## Mission
Поддерживать репозиторий как универсальный scaffold для agent-first разработки.

## Эталонная структура
- `AGENTS.md`
- `ARCHITECTURE.md`
- `docs/design-docs/` — design и policy-документы (`index.md`, `core-beliefs.md`, `system-spec.md`, `rules.md`, `architecture.md`)
- `docs/exec-plans/` — `active/`, `completed/`, `tech-debt-tracker.md`
- `docs/generated/` — generated-артефакты (например `db-schema.md`)
- `docs/product-specs/` — продуктовые спеки (`index.md` и feature-документы)
- `docs/references/` — справочные материалы для LLM/инженеров (`index.md` и `.txt` reference-файлы)
- `docs/` root — `DESIGN.md`, `FRONTEND.md`, `PLANS.md`, `PRODUCT_SENSE.md`, `QUALITY_SCORE.md`, `RELIABILITY.md`, `SECURITY.md`

## Где что искать
- Старт для человека: `README.md`, `QUICKSTART.md`, `METHOD.md`
- High-level структура: `ARCHITECTURE.md`
- Базовые policy/design документы: `docs/design-docs/system-spec.md`, `docs/design-docs/rules.md`, `docs/design-docs/architecture.md`
- Reliability/security/quality: `docs/RELIABILITY.md`, `docs/SECURITY.md`, `docs/QUALITY_SCORE.md`
- Наблюдаемость и принципы: `docs/OBSERVABILITY.md`, `docs/GOLDEN_PRINCIPLES.md`, `docs/observability/queries.md`
- Worktree процесс: `docs/WORKTREE_WORKFLOW.md`
- Возможности агента в этом шаблоне: `docs/AGENT_CAPABILITIES.md`
- Планы: `.agent/PLANS.md`, `docs/PLANS.md`, `docs/exec-plans/`
- Реестр незаполненного: `docs/todo-registry.md`
- Технические проверки: `scripts/custom_linter.py`, `scripts/custom_builder.sh`

## Когда читать отдельные инструкции по разработке шаблона
Если задача изменяет сам scaffold (структуру репозитория, правила шаблона, базовые скрипты/документы для будущих проектов), сначала открой `docs/TEMPLATE_MAINTENANCE.md` и следуй ему.

# ExecPlans
When writing complex features or significant refactors, use an ExecPlan (as described in docs/PLANS.md) from design to implementation.
