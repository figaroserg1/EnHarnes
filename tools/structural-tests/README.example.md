# Structural tests (ArchUnit style for Python)

Эта директория хранит структурные тесты зависимостей (подход аналогичен ArchUnit, для Python-проектов можно использовать pytest + pytest-archon).

## Что проверяется
- Разрешённые направления зависимостей слоёв `Types → Config → Repo → Service → Runtime → UI`.
- Отсутствие циклических зависимостей между слоями.

## Запуск
```bash
pytest tools/structural-tests/test_layer_dependencies.py
```
