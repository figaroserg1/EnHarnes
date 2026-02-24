# Engineering Rules — Phase 1

## 1) Agent execution rules
- Агент выполняет только проверяемые изменения и фиксирует проверки.
- Агент не пропускает обновление документации, если меняется процесс.
- TODO: [HUMAN] Утвердить границы автономности для изменений среднего/высокого риска.

## 2) Change management rules
- Все значимые изменения проходят через commit + PR.
- Для сложных задач используется ExecPlan.
- TODO: [AI->HUMAN] Зафиксировать SLA на review и критерии эскалации.

## 3) Security and reliability rules
- Секреты не хранятся в репозитории.
- Изменения в security/reliability должны сопровождаться обновлением профильных документов.
- TODO: [HUMAN] Утвердить минимальные требования compliance.

## 4) Documentation rules
- Все неизвестные части будущего продукта оформляются как TODO с владельцем.
- TODO: [AI] Поддерживать консистентность между `README.md`, `METHOD.md`, `ARCHITECTURE.md`.

---

## 5) Engineering philosophy (judgment, not linter rules)

Prefer simple functions and explicit logic over abstractions.
Keep execution flow linear and readable.
Start monolith-first: single service, single repo, single DB.
Allow small duplication if it keeps code simple.

Introduce abstraction only when all three are true:
- 3+ real repeated cases exist now
- it reduces complexity now
- it improves readability now

Add a new architectural layer only for real boundaries:
- external integration
- async processing
- security boundary
- transaction scope

Before adding complexity: does this simplify the code today?
Is this solving a real current need? If any answer is NO — choose the simpler solution.
