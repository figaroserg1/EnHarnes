# GOLDEN PRINCIPLES

Это не советы. Это инварианты.

- TODO: [HUMAN] Определить и зафиксировать ключевые архитектурные принципы.
- TODO: [AI] Использовать этот документ как источник правил для автоматических линтеров.

EXAMPLE (REPLACE ME):
- structured logging only;
- no business logic in UI layer;
- max file size 5k lines.

## AI Draft: baseline best practices

> Этот блок можно использовать как стартовую точку до утверждения финальных принципов.

1. **Single source of truth for business rules**
   - Доменная логика живёт в одном слое (domain/service), а не дублируется между UI, API и jobs.
2. **Fail fast на границах системы**
   - Валидация входа на boundary (API, queue consumer, CLI), внутри системы — работа с уже валидными моделями.
3. **Observability-by-default**
   - Каждая важная операция имеет структурированный лог, метрики latency/error rate и trace-id.
4. **Secure-by-default**
   - Принцип минимальных привилегий, безопасные значения по умолчанию, секреты только через secret manager.
5. **Idempotency for side effects**
   - Любые повторяемые вызовы (webhook, job retry, payment callback) проектируются идемпотентными.
6. **Backward compatibility first**
   - Контракты (API/events/schema) меняются через versioning + deprecation window.
7. **Small, reversible changes**
   - Изменения дробятся на небольшие PR с feature flags и понятным rollback-путём.
8. **Automation over tribal knowledge**
   - Обязательные проверки (lint/tests/docs checks/security scan) автоматизированы в CI, а не зависят от памяти команды.

## AI Draft: mapping принципов в проверяемые правила

- Для `structured logging only`:
  - запрет неструктурированных `print`/`console.log` в production-коде;
  - обязательные поля `service`, `env`, `trace_id`, `operation`, `result`.
- Для `no business logic in UI layer`:
  - архитектурное правило линтера: UI-модули не импортируют domain repositories напрямую;
  - проверка PR: бизнес-ветвления и расчёты выносятся в use-case/service.
- Для `max file size 5k lines`:
  - soft-limit предупреждение с 800 строк;
  - hard-limit блокировка merge >1500 строк для application-кода (кроме generated).
