# Core beliefs

- TODO: [HUMAN] Утвердить продуктовые и инженерные убеждения команды.
- TODO: [AI] Переложить убеждения в проверяемые engineering rules.

## AI Draft: baseline core beliefs (best practices)

> Черновой набор для старта. Команда может адаптировать формулировки под контекст домена.

### Product beliefs

1. **Value over output**
   - Меряем успех не количеством фич, а влиянием на пользовательский результат и бизнес-метрики.
2. **Problem-first discovery**
   - Сначала подтверждаем проблему и сегмент пользователей, потом выбираем реализацию.
3. **Fast feedback loops**
   - Предпочитаем короткие циклы релиза и раннюю проверку гипотез на реальных пользователях.
4. **Reliability is a feature**
   - Отказоустойчивость и предсказуемость UX являются частью ценности продукта.

### Engineering beliefs

1. **Design for change**
   - Архитектура должна упрощать эволюцию системы, а не только решать текущий кейс.
2. **Quality is built-in, not inspected-in**
   - Качество закладывается через архитектуру, тесты и автоматические проверки, а не только через ручной review.
3. **Security and privacy by default**
   - Любое решение проходит базовую проверку на риски безопасности и защиты данных.
4. **Operational excellence is part of development**
   - Код считается «готовым» только при наличии мониторинга, алертов и понятной диагностики.

## AI Draft: beliefs → engineering rules

| Belief | Проверяемое правило |
| --- | --- |
| Value over output | Для каждой фичи в PR/спеке фиксируется целевая метрика и expected impact. |
| Fast feedback loops | Default rollout: feature flag + staged rollout + post-release check. |
| Quality is built-in | Merge-blocking CI: lint + unit/integration tests + docs consistency checks. |
| Security by default | Обязательный security checklist для изменений auth/data/permissions. |
| Operational excellence | Для каждого нового критичного workflow: logs + metrics + alert + runbook link. |
