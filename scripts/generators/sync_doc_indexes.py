#!/usr/bin/env python3
"""sync_doc_indexes.py — Auto-generate index.md files for doc directories.

Scans configured doc directories, finds all .md files (except index.md itself),
and updates the registry table in each index.md.

Directories scanned:
  - docs/design-docs/  (Document | Status | Last Verified | Owner)
  - docs/product-specs/ (Spec | Status | Priority | Owner)
  - docs/references/    (Reference | Description)

If index.md doesn't exist, creates it. If it exists, updates the table
while preserving any content after the table.

Usage:
    python scripts/generators/sync_doc_indexes.py
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
    return Path(__file__).resolve().parents[2]


ROOT = _find_root()

# Each entry: (dir_path, title, columns, column_defaults)
INDEX_CONFIGS = [
    (
        "docs/design-docs",
        "Design Documents Index",
        ["Document", "Status", "Last Verified", "Owner"],
        {"Status": "Draft", "Last Verified": "—", "Owner": "TODO: [HUMAN]"},
    ),
    (
        "docs/product-specs",
        "Product Specifications Index",
        ["Spec", "Status", "Priority", "Owner"],
        {"Status": "Draft", "Priority": "—", "Owner": "TODO: [HUMAN]"},
    ),
    (
        "docs/references",
        "References Index",
        ["Reference", "Description"],
        {"Description": "TODO: [AI] Add description"},
    ),
]

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
