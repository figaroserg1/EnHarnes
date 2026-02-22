# EnHarnes — universal agent-first repo scaffold

Публичный шаблон, который помогает быстро стартовать проект, даже если на старте ещё неизвестны точные system spec, rules, архитектура и процессы.

## Главная идея
Если данных не хватает, **не выдумывать**. Оставляем явный placeholder:

- `TODO: [HUMAN]` — заполняет человек.
- `TODO: [AI]` — ИИ может заполнить сам.
- `TODO: [AI->HUMAN]` — ИИ обязан сначала опросить человека и только потом заполнить.

Для примеров используем только метку:
- `EXAMPLE (REPLACE ME)` — пример обязателен к замене.

## Что уже есть в шаблоне
- Пошаговый старт: `QUICKSTART.md`
- Краткая памятка метода: `METHOD.md`
- Карта работы для агента: `AGENTS.md`
- Базовые шаблоны документов: `docs/`
- Заготовки полезных скриптов: `scripts/`
- Отдельный сетап тулов (MCP + skills): `tooling/SETUP_TOOLS.md`
- Полуавтоматическая проверка TODO/примеров: `scripts/custom_linter.py`

## Как начать
1. Пройти `QUICKSTART.md`.
2. Заполнить `docs/system-spec.md`.
3. Заполнить `docs/rules.md`.
4. Уточнить `docs/architecture.md` + `ARCHITECTURE.md`.
5. Настроить инструменты по `tooling/SETUP_TOOLS.md`.
6. Запустить:

```bash
make lint
make build
```

## Внешние референсы
Ссылки на хорошие внешние гайды собраны в `docs/references.md`.
