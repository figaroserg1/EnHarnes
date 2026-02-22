# EnHarnes — Universal Project Scaffold

Готовый публичный шаблон репозитория для запуска проектов, когда на старте ещё неясны точные правила, система или процессы.

> Важный принцип: если что-то неизвестно — **оставляем явный placeholder формата `TODO: [HUMAN|AI|AI->HUMAN]`** с пометкой **кто заполняет**:
> - `[HUMAN]` — заполняет человек.
> - `[AI]` — заполняет ИИ без доп. вопросов.
> - `[AI->HUMAN]` — ИИ обязан сначала опросить человека, потом заполнить.

## Что внутри
- Пошаговый запуск работы с шаблоном: `QUICKSTART.md`
- Краткая метод-напоминалка: `METHOD.md`
- Шаблоны системного описания/правил/архитектуры: `docs/`
- Заготовки кастомного линтера и сборщика: `scripts/`
- Отдельный сетап тулов (MCP + skills): `tooling/SETUP_TOOLS.md` и `tooling/setup-tools.sh`

## Рекомендуемый порядок
1. Открой `QUICKSTART.md`.
2. Заполни критичные `TODO` из `docs/system-spec.md`.
3. Уточни правила в `docs/rules.md`.
4. Зафиксируй целевую архитектуру в `docs/architecture.md`.
5. Настрой инструменты через `tooling/SETUP_TOOLS.md`.
6. Прогони `scripts/custom_linter.py` и `scripts/custom_builder.sh`.

## Быстрые команды
```bash
python3 scripts/custom_linter.py
bash scripts/custom_builder.sh
```

## Полезные внешние гайды
Смотри `docs/references.md` — туда уже добавлены стартовые ссылки по architecture docs, ADR и style guides.
