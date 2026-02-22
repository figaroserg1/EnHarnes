# Rules & Policies Template

> ⚠️ Это шаблон. Все пункты с `TODO` и `REPLACE ME` обязательно заменить.

## 1. Security Rules
- TODO: Политика секретов (где хранить токены/ключи).
- Owner: HUMAN
- Priority: P0
- Status: TODO
- Example (REPLACE ME): "Секреты только через Vault/Secrets Manager".

- TODO: Правила доступа к production.
- Owner: HUMAN
- Priority: P0
- Status: TODO
- Example (REPLACE ME): "Доступ только через SSO + MFA + approve workflow".

## 2. Data Governance
- TODO: Классы данных и правила хранения.
- Owner: AI->HUMAN
- Priority: P0
- Status: TODO
- Example (REPLACE ME): "PII хранится в зашифрованном виде, retention 180 дней".

## 3. Engineering Rules
- TODO: Code review policy (кто и как ревьюит).
- Owner: AI
- Priority: P1
- Status: TODO
- Example (REPLACE ME): "Минимум 1 approve, запрет self-merge в main".

- TODO: Branching strategy.
- Owner: AI->HUMAN
- Priority: P1
- Status: TODO
- Example (REPLACE ME): "trunk-based + короткоживущие feature-ветки".

## 4. Release & Incident
- TODO: Release cadence и критерии готовности.
- Owner: AI->HUMAN
- Priority: P1
- Status: TODO
- Example (REPLACE ME): "Релизы 2 раза в неделю, обязательны smoke tests".

- TODO: Incident response baseline.
- Owner: HUMAN
- Priority: P1
- Status: TODO
- Example (REPLACE ME): "S1 инцидент: ack до 15 минут".
