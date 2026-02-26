# Scripts Reference

Описание всех скриптов проекта. Для человека — что делает, зачем нужен, как запускать.

---

## worktree-boot.sh

Создаёт изолированный worktree для задачи агента. Автоматически определяет runtime (Python/Node/Rust), ставит зависимости, запускает smoke-проверку. Каждая задача — отдельный worktree, без shared state.

```bash
./scripts/worktree-boot.sh feature-login
# Создаёт ../worktree_feature-login на ветке task/feature-login
```

---

## agent_self_review.sh

Предварительная проверка перед PR — 5 шагов: статический анализ (`make check`), структурные тесты (`make structural`), проверка doc-drift, проверка watch-path из `risk-policy.json`, быстрый entropy spot-check. Если хоть один шаг упал — exit 1, PR открывать нельзя.

```bash
bash scripts/agent_self_review.sh
# или через Makefile:
make review
```

---

## check_doc_drift.py

Читает `risk-policy.json`, проверяет что все документы из `docsDriftRules` реально существуют. Если файлы в PR затрагивают watch-path — выводит предупреждения о документах, которые нужно обновить. Запускается в CI и в self-review.

```bash
python3 scripts/check_doc_drift.py
```

Код возврата 1 = есть ссылки на несуществующие документы.

---

## custom_linter.py

Линтер для markdown и соглашений об именовании:
- Каждый `TODO:` должен иметь маркер владельца `[HUMAN]`, `[AI]` или `[AI->HUMAN]`
- Каждый `EXAMPLE` должен содержать `(REPLACE ME)`
- Файлы в `src/` должны быть в kebab-case
- Директории слоёв в `src/` должны совпадать с ARCHITECTURE.md (Types, Config, Repo, Service, Runtime, UI, Providers)

```bash
python3 scripts/custom_linter.py
```

Ошибки блокируют (exit 1), предупреждения — нет.

---

## doc_gardener.sh

Комплексное обслуживание документации — 5 проверок:
1. Устаревшие заголовки верификации (старше 30 дней)
2. Битые внутренние ссылки в markdown
3. Файлы-индексы, которые всё ещё заглушки (< 5 строк)
4. Doc lint (вызывает `custom_linter.py`)
5. Doc drift (вызывает `check_doc_drift.py`)

```bash
bash scripts/doc_gardener.sh
# или:
make gardener
```

---

## entropy-check.sh

Сканирование «энтропии» проекта — нарастающего беспорядка:
1. Незаменённые `REPLACE ME` плейсхолдеры в docs/
2. Скрипты-сироты, не упомянутые в Makefile или CI
3. Пустые target-значения в `evals/control-loop-metrics.yaml`
4. Python-файлы длиннее 500 строк (soft limit)
5. Битые ссылки на документы в `risk-policy.json`

```bash
bash scripts/entropy-check.sh
# или:
make entropy
```

---

## measure_metrics.py

Измеряет 5 метрик контроля через GitHub API (`gh` CLI):

| Метрика | Что измеряет |
|---------|-------------|
| `pr_pass_at_1` | % PR где CI прошёл с первого коммита |
| `merge_cycle_time_hours` | Медиана часов от открытия PR до merge |
| `revert_rate` | % замерженных PR, которые потом реверт |
| `human_intervention_rate` | % PR с комментариями от людей (не ботов) |
| `time_to_actionable_failure_minutes` | Медиана минут от push до провала CI |

Сравнивает с setpoints из `evals/control-loop-metrics.yaml`. Exit 1 при алертах.

```bash
python3 scripts/measure_metrics.py --owner figaroserg1 --repo EnHarnes --days 30
```

Требует: `gh auth login`.

---

## obs.py

Модуль наблюдаемости без инфраструктуры. Пишет структурированные JSON-логи и метрики в JSONL-файлы (`.claude/observability/`). Имеет API для записи и чтения.

```python
import obs
obs.log("info", "task started", component="ci", task_id="abc")
obs.metric("startup_time_ms", 1230, component="api")

errors = obs.query_logs(level="error", since_minutes=5)
print(obs.summary())
```

Phase 1 (текущая) — файлы. Phase 2 — Vector sink. Phase 3 — Grafana + Loki.

---

## structural-tests.sh

Запускает структурные тесты: проверяет что зависимости между слоями соответствуют архитектуре (UI не импортирует Repo напрямую и т.д.).

```bash
bash scripts/structural-tests.sh
# или:
make structural
```

Внутри: `pytest tools/structural-tests/test_layer_dependencies.py`.

---

## custom_builder.sh

Генерирует единый `dist/project-handbook.md` из ключевых документов проекта (README, METHOD, QUICKSTART, ARCHITECTURE, system-spec, rules). Полезен для передачи контекста человеку или агенту одним файлом.

```bash
bash scripts/custom_builder.sh
# Результат: dist/project-handbook.md
```

---

## sync_todo_registry.py

Считает все `TODO:` маркеры по markdown-файлам и группирует по владельцу (HUMAN / AI / AI->HUMAN). Даёт быструю сводку кто за что отвечает.

```bash
python3 scripts/sync_todo_registry.py
# TODO owners summary:
# - HUMAN: 3
# - AI: 5
# - AI->HUMAN: 1
```

---

## harness/lint.sh

Автоопределяет тип проекта и запускает правильный линтер:
- Rust → `cargo clippy`
- Node.js → `npm run lint`
- Python → `custom_linter.py` + `dependency_guard.py`

Можно переопределить через переменную `HARNESS_LINT_CMD`.

```bash
bash scripts/harness/lint.sh
```

---

## harness/typecheck.sh

Автоопределяет тип проекта и запускает тайпчекер:
- Rust → `cargo check`
- Node.js → `npm run typecheck`
- Python → `pyright` или `mypy`

Можно переопределить через `HARNESS_TYPECHECK_CMD`.

```bash
bash scripts/harness/typecheck.sh
```

---

## dev-start.sh

Заглушка для запуска приложения в dev-режиме. Нужно заменить на реальную команду (например, `docker compose up`).

---

## obs-up.sh / obs-down.sh

Заглушки для поднятия/остановки observability стека (docker compose). Будут актуальны при переходе на Phase 2/3 (Vector, Grafana, Loki).

---

## seed-dev-data.sh

Заглушка для загрузки dev-данных (фикстуры, сиды). Нужно заменить на реальную реализацию.
