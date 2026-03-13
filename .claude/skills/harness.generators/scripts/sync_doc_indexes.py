#!/usr/bin/env python3
"""sync_doc_indexes.py — Auto-generate index.md files for doc directories.

Reads config from policies/doc-indexes.yaml. For each configured directory,
finds all .md files (except index.md itself) and updates the registry table.

If index.md doesn't exist, creates it. If it exists, updates the table
while preserving any content after the table.

Usage:
    python scripts/harness/generators/sync_doc_indexes.py
    or: make sync-indexes
"""

import re
import subprocess
import sys
from pathlib import Path


def _find_root() -> Path:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            return Path(result.stdout.strip())
    except FileNotFoundError:
        pass
    return Path(__file__).resolve().parents[4]


ROOT = _find_root()


def _load_index_configs() -> list[tuple[str, str, list[str], dict[str, str]]]:
    """Load index configs from policies/doc-indexes.yaml (simple parser)."""
    yaml_path = ROOT / "policies" / "doc-indexes.yaml"
    if not yaml_path.exists():
        return []
    configs: list[tuple[str, str, list[str], dict[str, str]]] = []
    current: dict = {}
    in_defaults = False
    for line in yaml_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped == "indexes:":
            continue
        if stripped.startswith("- dir:"):
            if current.get("dir"):
                configs.append((
                    current["dir"], current.get("title", ""),
                    current.get("columns", []), current.get("defaults", {}),
                ))
            current = {"dir": stripped.split(":", 1)[1].strip()}
            in_defaults = False
            continue
        if stripped.startswith("title:"):
            current["title"] = stripped.split(":", 1)[1].strip()
            in_defaults = False
        elif stripped.startswith("columns:"):
            val = stripped.split(":", 1)[1].strip()
            if val.startswith("[") and val.endswith("]"):
                current["columns"] = [x.strip() for x in val[1:-1].split(",") if x.strip()]
            in_defaults = False
        elif stripped == "defaults:":
            current["defaults"] = {}
            in_defaults = True
        elif in_defaults and ":" in stripped:
            key, _, val = stripped.partition(":")
            val = val.strip().strip('"')
            current.setdefault("defaults", {})[key.strip()] = val
    if current.get("dir"):
        configs.append((
            current["dir"], current.get("title", ""),
            current.get("columns", []), current.get("defaults", {}),
        ))
    return configs


INDEX_CONFIGS = _load_index_configs()

TABLE_HEADER_RE = re.compile(r"^\|.*\|$")
TABLE_SEP_RE = re.compile(r"^\|[-| ]+\|$")


def find_docs(dir_path: Path) -> list[str]:
    """Find all .md files in dir except index.md, sorted."""
    if not dir_path.exists():
        return []
    return sorted(
        f.name for f in dir_path.glob("*.md")
        if f.name.lower() != "index.md"
    )


def parse_existing_table(text: str) -> dict[str, dict[str, str]]:
    """Parse existing table rows into {filename: {col: value}}."""
    rows: dict[str, dict[str, str]] = {}
    lines = text.splitlines()
    headers: list[str] = []
    for line in lines:
        stripped = line.strip()
        if TABLE_SEP_RE.match(stripped):
            continue
        if TABLE_HEADER_RE.match(stripped):
            if not headers:
                headers = [c.strip() for c in stripped.split("|")[1:-1]]
            else:
                cols = [c.strip() for c in stripped.split("|")[1:-1]]
                if cols and headers:
                    # First column is the doc name/link
                    first = cols[0]
                    # Extract filename from markdown link [name](file)
                    link_match = re.match(r"\[.*?\]\((.+?)\)", first)
                    key = link_match.group(1) if link_match else first
                    row = {}
                    for i, h in enumerate(headers):
                        row[h] = cols[i] if i < len(cols) else ""
                    rows[key] = row
    return rows


def build_table(columns: list[str], rows: list[dict[str, str]]) -> str:
    """Build a markdown table from columns and row dicts."""
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, sep]
    for row in rows:
        cells = [row.get(c, "—") for c in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def sync_index(dir_rel: str, title: str, columns: list[str], defaults: dict[str, str]) -> bool:
    """Sync one index.md. Returns True if changes were made."""
    dir_path = ROOT / dir_rel
    if not dir_path.exists():
        return False

    index_path = dir_path / "index.md"
    doc_files = find_docs(dir_path)

    if not doc_files and not index_path.exists():
        return False

    # Parse existing data to preserve user edits
    existing: dict[str, dict[str, str]] = {}
    after_table = ""
    if index_path.exists():
        text = index_path.read_text(encoding="utf-8")
        existing = parse_existing_table(text)
        # Preserve content after the table (sections like ## Verification Schedule)
        lines = text.splitlines()
        in_table = False
        after_idx = len(lines)
        for i, line in enumerate(lines):
            stripped = line.strip()
            if TABLE_HEADER_RE.match(stripped) or TABLE_SEP_RE.match(stripped):
                in_table = True
                continue
            if in_table and not TABLE_HEADER_RE.match(stripped):
                # First non-table line after table
                after_idx = i
                break
        # Find next section header after table
        for i in range(after_idx, len(lines)):
            if lines[i].strip().startswith("##"):
                after_table = "\n" + "\n".join(lines[i:])
                break

    # Build rows: merge existing data with new files
    rows = []
    first_col = columns[0]
    for doc in doc_files:
        if doc in existing:
            row = dict(existing[doc])
            # Ensure first column has link format
            row[first_col] = f"[{doc}]({doc})"
            rows.append(row)
        else:
            row = {first_col: f"[{doc}]({doc})"}
            for col in columns[1:]:
                row[col] = defaults.get(col, "—")
            rows.append(row)

    # Build file content
    table = build_table(columns, rows)
    content = f"# {title}\n\nRegistry of all documents in this directory.\n\n{table}\n"
    if after_table:
        content += after_table
    if not content.endswith("\n"):
        content += "\n"

    # Check if changed
    if index_path.exists():
        old = index_path.read_text(encoding="utf-8")
        if old == content:
            return False

    index_path.write_text(content, encoding="utf-8")
    print(f"  Updated: {dir_rel}/index.md ({len(doc_files)} docs)")
    return True


def main() -> int:
    print("=== Sync Doc Indexes ===")
    changes = 0
    for dir_rel, title, columns, defaults in INDEX_CONFIGS:
        if sync_index(dir_rel, title, columns, defaults):
            changes += 1

    if changes:
        print(f"\n{changes} index file(s) updated.")
    else:
        print("\nAll index files up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
