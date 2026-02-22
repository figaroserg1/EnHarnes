# Architecture Template

> Используйте этот файл как стартовую точку.
> Блоки с `REPLACE ME` — демонстрационные и должны быть заменены.

## 1. Context Diagram
- TODO: Описать основные компоненты и внешние системы.
- Owner: AI->HUMAN
- Priority: P0
- Status: TODO
- Example (REPLACE ME):
  - Web App -> API -> DB
  - API -> Message Broker -> Worker

## 2. Key Technical Decisions (ADR-lite)

### Decision 1
- TODO: Название решения.
- Owner: AI->HUMAN
- Status: TODO
- Example (REPLACE ME): "Выбор Postgres как основной БД".
- Options considered (REPLACE ME): Postgres / MySQL / DynamoDB.
- Trade-offs (REPLACE ME): консистентность vs операционная сложность.

## 3. Non-Functional Requirements
- TODO: Performance target.
- Owner: AI->HUMAN
- Priority: P1
- Example (REPLACE ME): p95 latency < 300ms.

- TODO: Reliability target.
- Owner: HUMAN
- Priority: P1
- Example (REPLACE ME): SLO 99.9% uptime.

- TODO: Observability baseline.
- Owner: AI
- Priority: P1
- Example (REPLACE ME): structured logs + metrics + traces.

## 4. Risks
- TODO: Ключевые архитектурные риски + план снижения.
- Owner: AI->HUMAN
- Priority: P1
- Status: TODO
- Example (REPLACE ME): "Риск vendor lock-in, mitigation: абстракции и контрактные тесты".

## 5. External References (обязательно обновить)
См. `docs/references.md` — добавьте ссылки на релевантные примеры и гайды.
