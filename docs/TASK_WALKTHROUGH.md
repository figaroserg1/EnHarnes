# Task Walkthrough: Medium-Risk Feature (Example)

Пример полного цикла для medium-risk задачи — от промпта пользователя до мержа PR.
Показывает какие шаги делает агент, какие вещи срабатывают автоматически (хуки/CI), и в каком порядке.

---

## Контекст примера

**Промпт пользователя:** "Добавь новый skill `order-status` который позволяет проверить статус заказа по номеру через Trilogy API. Он должен вызывать существующий TrilogyClient."

**Классификация:** Medium risk (новый функционал, затрагивает Service слой)

---

## Полный поток

### Фаза 0: Промпт пользователя

```
User: "Добавь новый skill order-status..."
```

🔄 **AUTO: `prompt-validator.py`** (UserPromptSubmit hook) — проверяет что в промпте нет секретов. Если найдены API ключи → блокирует отправку.

---

### Фаза 1: Агент загружает контекст

**Агент делает (шаги 1-5 Task Loop):**

```
1. [AGENT] Читает AGENTS.md полностью
2. [AGENT] make smoke                         # Шаг 2: валидация (~5s)
3. [AGENT] Создаёт запись в docs/activity-log.md:
   ## 2026-03-25 14:00 — Add order-status skill
   - RISK: Medium
   - READ: AGENTS.md, ARCHITECTURE.md, policies/risk-policy.json
4. [AGENT] Читает ARCHITECTURE.md             # Шаг 4: загрузка контекста
5. [AGENT] Читает policies/risk-policy.json
6. [AGENT] Читает policies/architecture.yaml
7. [AGENT] Классифицирует: Medium risk        # Шаг 5
```

---

### Фаза 2: Планирование (🚫 STOP gate)

**Агент ОБЯЗАН создать ExecPlan до написания кода:**

```
8. [AGENT] Создаёт docs/exec-plans/active/2026-03-25-order-status-skill.md:

   # ExecPlan: order-status skill

   ## Goal
   Добавить skill для проверки статуса заказа через TrilogyClient.

   ## Risk tier
   Medium — новый функционал в Service слое, использует существующий клиент.

   ## Scope
   - CREATE: src/Service/order-status-skill.py
   - CREATE: tests/test_order_status_skill.py
   - MODIFY: src/Service/skill-registry.py (регистрация)
   - MODIFY: ARCHITECTURE.md (обновить quality grade)

   ## Steps
   1. Создать тип OrderStatusResult в Types/
   2. Создать order-status-skill.py в Service/
   3. Зарегистрировать в skill-registry.py
   4. Написать тесты
   5. Проверить layer dependencies
   6. Обновить документацию

   ## Verification
   - `make check` — lint проходит
   - `make structural` — layer deps не нарушены
   - `pytest tests/test_order_status_skill.py -v` — все тесты зелёные
   - `make review` — все 5 гейтов пройдены

   ## Decision log
   (будет обновляться по ходу работы)

   ## Progress
   - [ ] Step 1
   - [ ] Step 2
   - [ ] Step 3
   - [ ] Step 4
   - [ ] Step 5
   - [ ] Step 6
```

**🚫 STOP:** Агент показывает план пользователю и ждёт подтверждения.

```
User: "Ок, делай"
```

---

### Фаза 3: Реализация

**Агент делает (шаг 8 Task Loop):**

```
9.  [AGENT] Создаёт src/Types/order-status-types.py
10. [AGENT] make check                        # проверка после изменения
```

🔄 **Каждый `make check` вызывается агентом явно.** Внутри он запускает doc_linter.py + code_conventions.py — но агент вызывает только `make check`.

```
11. [AGENT] Создаёт src/Service/order-status-skill.py
12. [AGENT] make check                        # проверка после изменения
13. [AGENT] Модифицирует src/Service/skill-registry.py
14. [AGENT] make check
15. [AGENT] Создаёт tests/test_order_status_skill.py
16. [AGENT] pytest tests/test_order_status_skill.py -v
17. [AGENT] make structural                   # проверка layer deps
```

**Агент обновляет Activity Log и ExecPlan Progress:**

```
18. [AGENT] Обновляет docs/activity-log.md:
    - COMMANDS: make smoke, make check ×3, pytest, make structural
19. [AGENT] Обновляет ExecPlan Progress: ✅ Steps 1-5
```

---

### Фаза 4: Doc drift (шаг 9)

```
20. [AGENT] Читает policies/risk-policy.json → docsDriftRules
    # Видит: изменения в src/ → нужно проверить ARCHITECTURE.md, docs/generated/db-schema.md
21. [AGENT] Обновляет ARCHITECTURE.md (quality grade Service слоя)
22. [AGENT] Обновляет ExecPlan Progress: ✅ Step 6
```

---

### Фаза 5: Pre-PR (🚫 STOP gate)

```
23. [AGENT] make review                       # Шаг 10: pre-PR gate
```

**`make review` внутри запускает 5 проверок (агент вызывает ОДНУ команду):**
1. `make check` — static lint
2. `make structural` — architecture tests
3. `check_doc_drift.py` — risk-policy compliance
4. Watch-path reminders — какие доки проверить
5. Entropy spot-check — мусор, пустые setpoints

```
    Результат: PASS: all self-review checks passed. Ready for PR.
```

🚫 **Если FAIL** — агент исправляет и перезапускает `make review`.

---

### Фаза 6: Agent review (шаг 11)

```
24. [AGENT] Запускает субагента в роли reviewer:
    "Review the changes in this branch. Focus on: layer violations,
     missing tests, doc drift. Read AGENTS.md first."
25. [REVIEWER SUBAGENT] Проверяет, даёт feedback
26. [AGENT] Исправляет замечания если есть
27. [AGENT] make check                        # после исправлений
```

---

### Фаза 7: Commit + PR

```
28. [AGENT] git add <specific files>
29. [AGENT] git commit -m "feat: add order-status skill for Trilogy API"
```

🔄 **AUTO: pre-commit hook** — запускает `make lint` перед коммитом. Если lint fails → коммит блокируется, агент исправляет.

```
30. [AGENT] git push
31. [AGENT] gh pr create --title "feat: add order-status skill" --body "..."
```

🔄 **AUTO: ci.yml** — GitHub Actions запускает lint + doc-drift на PR. Агент не вызывает это.

🔄 **AUTO: post-response-sync.py** (Stop hook) — после ответа агента автоматически синхронизируются doc indexes если были изменены .md файлы.

---

### Фаза 8: Завершение

```
32. [AGENT] Финализирует docs/activity-log.md:
    - OUTCOME: PR #42 created, all checks pass
33. [AGENT] Обновляет progress.txt
34. [AGENT] Перемещает ExecPlan в docs/exec-plans/completed/
```

---

## Сводная таблица: кто что вызывает

| Шаг | Кто | Что | Тип |
|-----|-----|-----|-----|
| Проверка промпта | `prompt-validator.py` | Блок секретов | 🔄 AUTO (hook) |
| `make smoke` | Агент | Валидация на старте | 🤖 MANUAL |
| Activity Log entry | Агент | Запись в docs/activity-log.md | 🤖 MANUAL |
| ExecPlan создание | Агент | Файл в docs/exec-plans/active/ | 🤖 MANUAL |
| `make check` | Агент | Lint после каждого изменения | 🤖 MANUAL |
| `make structural` | Агент | Layer dependency tests | 🤖 MANUAL |
| `pytest tests/...` | Агент | Unit/integration тесты | 🤖 MANUAL |
| Doc drift проверка | Агент | Читает risk-policy.json, обновляет docs | 🤖 MANUAL |
| `make review` | Агент | Pre-PR 5-gate check | 🤖 MANUAL |
| Субагент review | Агент | Запуск reviewer субагента | 🤖 MANUAL |
| `pre-commit` hook | Git | `make lint` перед коммитом | 🔄 AUTO (hook) |
| Bash validation | `validate-bash.py` | Блок опасных команд | 🔄 AUTO (hook) |
| Doc index sync | `post-response-sync.py` | Синхронизация индексов | 🔄 AUTO (hook) |
| CI pipeline | GitHub Actions | Lint + doc-drift на PR | 🔄 AUTO (CI) |
| Nightly entropy | GitHub Actions | Entropy scan в 03:00 | 🔄 AUTO (CI) |
| Weekly cleanup | GitHub Actions | Auto-fix + PR в понедельник | 🔄 AUTO (CI) |

---

## Чего агент НЕ должен вызывать

| Скрипт | Почему не нужно |
|--------|----------------|
| `doc_linter.py` напрямую | Вызывается внутри `make check` |
| `code_conventions.py` напрямую | Вызывается внутри `make check` |
| `test_layer_dependencies.py` напрямую | Вызывается через `make structural` |
| `check_doc_drift.py` напрямую | Вызывается внутри `make review` |
| `entropy_check.py` напрямую | Вызывается внутри `make review` и `make check-entropy` |
| `sync_doc_indexes.py` вручную | Автоматически вызывается post-response hook |
| `validate-bash.py` | Автоматический hook |
| `prompt-validator.py` | Автоматический hook |
| `post-response-sync.py` | Автоматический hook |

**Правило: агент вызывает только `make` таргеты, никогда не вызывает `.py` скрипты напрямую** (кроме `pytest` и `python scripts/harness/worktree_boot.py`).
