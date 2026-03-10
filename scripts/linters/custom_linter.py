#!/usr/bin/env python3
"""Markdown and naming convention linter.

ЧТО ДЕЛАЕТ:
  Проверяет соблюдение соглашений проекта по четырём направлениям:
    1. TODO-маркеры — каждый «TODO:» в markdown-файлах обязан содержать
       владельца: [HUMAN], [AI] или [AI->HUMAN]. Без этого непонятно,
       кто отвечает за выполнение задачи.
    2. EXAMPLE-плейсхолдеры — каждый блок «EXAMPLE» должен содержать
       «(REPLACE ME)», чтобы было очевидно, что это шаблон, а не рабочий код.
    3. Именование файлов — файлы в src/ должны быть в kebab-case
       (например, user-service.py), что обеспечивает единообразие в проекте.
    4. Имена директорий-слоёв — поддиректории в src/ должны соответствовать
       слоям из ARCHITECTURE.md (Types, Config, Repo, Service, Runtime, UI,
       Providers).

ЗАЧЕМ НУЖЕН:
  Этот линтер — часть CI-пайплайна (make check). Он ловит нарушения
  соглашений до код-ревью, экономя время людей и агентов. Без него
  TODO теряют владельцев, плейсхолдеры попадают в прод, а файловая
  структура постепенно деградирует.

ИСПОЛЬЗОВАНИЕ:
  python3 scripts/custom_linter.py

КОД ВОЗВРАТА:
  0 — нет blocking-ошибок (warnings допустимы)
  1 — есть ошибки, которые нужно исправить
"""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
OWNER_RE = re.compile(r"TODO:\s*\[(HUMAN|AI|AI->HUMAN)\]")
KEBAB_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*\.[a-z]+$")
LAYER_DIRS = {"Types", "Config", "Repo", "Service", "Runtime", "UI", "Providers"}

errors: list[str] = []
warnings: list[str] = []

# --- Markdown checks ---
for file_path in ROOT.rglob("*.md"):
    if ".git/" in str(file_path):
        continue

    for idx, line in enumerate(file_path.read_text(encoding="utf-8").splitlines(), start=1):
        if "TODO:" in line and not OWNER_RE.search(line):
            rel = file_path.relative_to(ROOT)
            errors.append(
                f"{rel}:{idx}: TODO without owner marker. "
                f"Fix: add [HUMAN], [AI], or [AI->HUMAN] after 'TODO:'. "
                f"Example: TODO: [AI] Implement feature X"
            )
        if "EXAMPLE" in line and "REPLACE ME" not in line:
            rel = file_path.relative_to(ROOT)
            errors.append(
                f"{rel}:{idx}: EXAMPLE without '(REPLACE ME)'. "
                f"Fix: add '(REPLACE ME)' to indicate this is a template placeholder."
            )

# --- Naming convention checks (src/ only) ---
src_dir = ROOT / "src"
if src_dir.is_dir():
    for file_path in src_dir.rglob("*"):
        if ".git/" in str(file_path) or file_path.is_dir():
            continue
        name = file_path.name
        if name.startswith("__"):
            continue

        if not KEBAB_RE.match(name):
            rel = file_path.relative_to(ROOT)
            warnings.append(
                f"{rel}: filename '{name}' is not kebab-case. "
                f"Fix: rename to kebab-case (e.g., 'user-service.py'). "
                f"Convention: files=kebab-case, types=PascalCase, functions=camelCase."
            )

    # Check layer directory names
    for child in src_dir.iterdir():
        if child.is_dir() and not child.name.startswith("."):
            for subdir in child.iterdir():
                if (subdir.is_dir()
                        and subdir.name not in LAYER_DIRS
                        and not subdir.name.startswith(".")
                        and not subdir.name.startswith("__")):
                    warnings.append(
                        f"{subdir.relative_to(ROOT)}: directory '{subdir.name}' is not a recognized layer. "
                        f"Expected: {', '.join(sorted(LAYER_DIRS))}. "
                        f"Fix: use standard layer names or update ARCHITECTURE.md."
                    )

# --- Output ---
for w in warnings:
    print(f"  [WARN] {w}")

if errors:
    print("Documentation lint errors:")
    for err in errors:
        print(f"  [ERROR] {err}")
    sys.exit(1)

if warnings:
    print(f"OK: {len(warnings)} warning(s), no blocking errors.")
else:
    print("OK: all lint checks passed.")
