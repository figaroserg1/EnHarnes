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
make lint-todos  # быстрая проверка TODO (~5с)
make lint        # все линтеры (lint-todos + lint-src + lint-structural)
make ci          # CI алиас для lint
```
