# ExecPlan: Перенос слоёв из `src/app_settings` в `src/`

## Цель
Привести структуру к виду `src/<Layer>` без промежуточного `app_settings`, обновить структурные тесты и документацию/правила агента.

## Шаги
1. Переместить директории слоёв (`Types`, `Config`, `Repo`, `Service`, `Runtime`, `UI`, `Providers`) из `src/app_settings` в `src/`.
2. Обновить импорты в файлах слоёв и структурный тест `tools/structural-tests/test_layer_dependencies.py`.
3. Добавить зависимость `printdirtree` в dependency-файл проекта.
4. Зафиксировать правило в `AGENTS.md`: использовать `printdirtree` при обновлении документации структуры, когда это уместно.
5. Обновить `progress.txt` и прогнать `pytest tools/structural-tests/test_layer_dependencies.py`.

## Критерии готовности
- В `src/` находятся только папки слоёв без `src/app_settings`.
- Структурный тест проходит.
- `requirements.txt` содержит `printdirtree`.
- `AGENTS.md` содержит явное правило про `printdirtree`.
