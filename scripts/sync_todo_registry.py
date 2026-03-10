#!/usr/bin/env python3
"""Подсчёт и классификация TODO-маркеров по владельцам.

ЧТО ДЕЛАЕТ:
  Сканирует все *.md файлы проекта и считает TODO-маркеры по владельцам:
    - HUMAN — задачи, которые должен выполнить человек
    - AI — задачи, которые должен выполнить агент
    - AI->HUMAN — задачи, начатые агентом, но требующие валидации человеком

  Выводит суммарную таблицу: сколько TODO каждого типа осталось в проекте.

ЗАЧЕМ НУЖЕН:
  Позволяет быстро оценить объём открытых задач и понять, кто за что
  отвечает. Если TODO: [AI] растёт — агент не справляется. Если TODO:
  [HUMAN] растёт — человек стал узким местом. Это инструмент для
  управления backlog-ом на уровне документации.

ИСПОЛЬЗОВАНИЕ:
  python3 scripts/sync_todo_registry.py
"""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
owner_re = re.compile(r"TODO:\s*\[(HUMAN|AI|AI->HUMAN)\]")

counts = {"HUMAN": 0, "AI": 0, "AI->HUMAN": 0}
for p in root.rglob("*.md"):
    for line in p.read_text(encoding="utf-8").splitlines():
        m = owner_re.search(line)
        if m:
            counts[m.group(1)] += 1

print("TODO owners summary:")
for k, v in counts.items():
    print(f"- {k}: {v}")
