# ExecPlan: Structural dependency tests and layered Python stubs

## Purpose
После этого изменения репозиторий будет содержать исполняемые структурные тесты (в стиле ArchUnit для Python) для проверки однонаправленных зависимостей слоёв `Types → Config → Repo → Service → Runtime → UI` и отдельного слоя `Providers`. Пользователь сможет запустить один pytest-тест и увидеть, что запрещённые зависимости (включая циклы) детектируются автоматически.

## Progress
- [x] (2026-02-23 23:44Z) Зафиксирован план работ и целевые артефакты.
- [x] (2026-02-23 23:46Z) Создан каркас `src/app_settings` с папками слоёв и stub-файлами.
- [x] (2026-02-23 23:47Z) Добавлен структурный тест зависимостей в `tools/structural-tests/test_layer_dependencies.py`.
- [x] (2026-02-23 23:47Z) Искусственно создана циклическая зависимость (`Types -> Config -> Types`) и подтверждено падение pytest.
- [x] (2026-02-23 23:48Z) Цикл исправлен, тесты проходят повторно.
- [x] (2026-02-23 23:48Z) Подключён скрипт `scripts/structural-tests.sh` в `scripts/test-all.sh`.
- [x] (2026-02-23 23:49Z) Обновлены `tools/structural-tests/README.example.md` и `progress.txt`.

## Surprises & Discoveries
- Observation: В репозитории отсутствовал `src/`, поэтому архитектурный каркас создан с нуля.
  Evidence: `rg --files` до изменений не возвращал файлов в `src/`.
- Observation: Проверка циклов и проверка allowlist покрывают разные классы нарушений и полезны одновременно.
  Evidence: На искусственном примере первая проверка поймала `Types -> Config`, вторая — конкретный цикл `Types -> Config -> Types`.

## Decision Log
- Decision: Реализовать архитектурный тест на AST-анализе импортов, чтобы не зависеть от runtime-импорта модулей.
  Rationale: AST-анализ стабильно выявляет связи слоёв и циклы без побочных эффектов выполнения кода.
  Date/Author: 2026-02-23 / Codex
- Decision: Добавить отдельный скрипт `scripts/structural-tests.sh` и вызывать его из `scripts/test-all.sh`.
  Rationale: Это упрощает локальный запуск только структурных проверок и повторное использование в CI.
  Date/Author: 2026-02-23 / Codex

## Outcomes & Retrospective
Результат соответствует цели: теперь есть runnable структурные тесты архитектурных зависимостей, есть каркас слоёв по `ARCHITECTURE.md`, и показана практика test-first через временное внесение архитектурного дефекта (цикла) с последующим исправлением. Пробел: пока это только один домен `app_settings`; при появлении новых доменов тест можно обобщить на весь `src/`.

## Context and Orientation
- `ARCHITECTURE.md` задаёт обязательную однонаправленную цепочку зависимостей для доменного кода в `src/`.
- `scripts/test-all.sh` — единый вход для тестов.
- `tools/structural-tests/README.example.md` — документ для запуска структурных тестов.
- `tools/linters/dependency_guard.py` — простая legacy-проверка импортов, дополняется новым pytest-тестом.

Термины:
- **Structural test**: тест, который проверяет структуру кода (зависимости модулей), а не бизнес-логику.
- **Layer dependency graph**: ориентированный граф зависимостей между слоями.
- **Cycle**: путь, который возвращается в исходный слой через зависимости (запрещён в данной архитектуре).

## Plan of Work
1. Создать домен `src/app_settings` и подпапки слоёв `Types`, `Config`, `Repo`, `Service`, `Runtime`, `UI`, `Providers`.
2. В каждом слое добавить `__init__.py` и stub-модуль с минимальными импортами между соседними слоями.
3. Добавить `tools/structural-tests/test_layer_dependencies.py`, который:
   - собирает импорты по AST;
   - сопоставляет каждый файл слою;
   - проверяет, что зависимости соответствуют allowlist;
   - проверяет отсутствие циклов через DFS.
4. Сначала внести искусственную циклическую зависимость (`Types -> Config` + `Config -> Types`) и выполнить pytest, чтобы тест упал.
5. Удалить запрещённый импорт, повторно выполнить pytest до зелёного состояния.
6. Подключить запуск теста в `scripts/test-all.sh` и обновить `tools/structural-tests/README.example.md`.
7. Обновить `progress.txt` итогом сессии.

## Concrete Steps
Команды (из `/workspace/EnHarnes`):
1. `pytest tools/structural-tests/test_layer_dependencies.py` (с намеренно внесённым циклом) → ожидаемое падение подтверждено.
2. Исправление `src/app_settings/Types/models.py`.
3. `pytest tools/structural-tests/test_layer_dependencies.py` → pass.
4. `bash scripts/test-all.sh` → pass.

Фрагмент фактического падения на шаге 1:

    E   AssertionError: Forbidden dependency: Types -> Config
    E   AssertionError: Detected cycle in layers: Types -> Config -> Types

## Validation and Acceptance
- Acceptance 1: тест зависимостей падает при наличии цикла и запрещённого направления. ✅
- Acceptance 2: после исправления цикла тест проходит. ✅
- Acceptance 3: `scripts/test-all.sh` запускает структурный тест и завершается успешно. ✅

## Idempotence and Recovery
- Все шаги идемпотентны: повторный запуск перезаписывает только рабочие файлы.
- Если тест не запускается из-за отсутствия pytest, установить его: `python3 -m pip install pytest`.
- Откат: `git checkout -- <file>` для конкретного файла.

## Artifacts and Notes
- Red-state pytest: детектированы `Forbidden dependency: Types -> Config` и цикл `Types -> Config -> Types`.
- Green-state pytest: `2 passed`.
- Full suite: `bash scripts/test-all.sh` завершился с `OK: base test suite completed (including structural dependency checks)`.

## Interfaces and Dependencies
- Python runtime: `python3`.
- Test runner: `pytest`.
- Новые интерфейсы:
  - `tools/structural-tests/test_layer_dependencies.py::test_layer_dependencies_follow_architecture()`
  - `tools/structural-tests/test_layer_dependencies.py::test_no_cycles_in_layer_graph()`

---
Revision note (2026-02-23): План обновлён по фактическому выполнению — добавлены результаты red/green прогона, новые скрипты и финальные выводы.
