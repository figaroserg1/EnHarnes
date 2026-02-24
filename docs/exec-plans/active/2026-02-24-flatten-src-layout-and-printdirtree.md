# ExecPlan: Flatten src layout and standardize printdirtree usage

## Purpose
Исправить структуру исходников с `src/app_settings/...` на прямую раскладку `src/<Layer>/...`, добавить зависимость `printdirtree` и зафиксировать правило её использования в `AGENTS.md` при обновлении документации.

## Progress
- [x] (2026-02-24) Подготовлен план и список затрагиваемых файлов.
- [x] (2026-02-24) Перемещены слои из `src/app_settings/` в `src/`.
- [x] (2026-02-24) Обновлены импорты и структурный тест зависимостей.
- [x] (2026-02-24) Добавлен `printdirtree` в зависимости и setup-скрипт.
- [x] (2026-02-24) Обновлён `AGENTS.md` и `progress.txt`.

## Plan of Work
1. Переместить директории `Types/Config/Repo/Service/Runtime/UI/Providers` в корень `src/`.
2. Исправить импорты в Python-файлах согласно новой структуре.
3. Адаптировать `tools/structural-tests/test_layer_dependencies.py` к пути `src/`.
4. Добавить зависимость `printdirtree` и команду установки в setup-утилиты.
5. Обновить агентские инструкции и журнал прогресса.

## Validation and Acceptance
- `pytest tools/structural-tests/test_layer_dependencies.py` проходит.
- `bash scripts/test-all.sh` проходит.
- В `AGENTS.md` есть явное правило про `printdirtree`.
