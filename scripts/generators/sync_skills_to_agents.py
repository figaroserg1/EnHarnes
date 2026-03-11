#!/usr/bin/env python3
"""sync_skills_to_agents.py — Sync installed skill entries into AGENTS.md.

Reads every .claude/skills/*/SKILL.md, extracts the '## AGENTS.md Entry'
section (expected to contain a markdown table row), and ensures each entry
exists in the '## Reference Table' of AGENTS.md.

Convention: each SKILL.md may contain a section like:

    ## AGENTS.md Entry
    | Topic | `path/to/file` | When to load |

The script parses table rows from that section and inserts any missing
rows into the Reference Table in AGENTS.md. Existing rows (matched by
the file path in column 2) are updated in place.

Usage:
    python scripts/generators/sync_skills_to_agents.py
    or: make sync-skills

Exit code:
    0 — AGENTS.md is up to date (or was updated)
    1 — error (AGENTS.md or skills not found)
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENTS_MD = ROOT / "AGENTS.md"
SKILLS_DIR = ROOT / ".claude" / "skills"

# Markers in AGENTS.md
REF_TABLE_HEADER = "## Reference Table"
# We look for the table between the header and the next ## section
SECTION_RE = re.compile(r"^## ", re.MULTILINE)
# Match a table row: | col1 | col2 | col3 |
TABLE_ROW_RE = re.compile(r"^\|[^|]+\|[^|]+\|[^|]+\|$")
# Skill-injected rows are marked with a comment in the SKILL.md
SKILL_ENTRY_MARKER = "## AGENTS.md Entry"


def extract_skill_rows(skill_md: Path) -> list[str]:
    """Extract table rows from the AGENTS.md Entry section of a SKILL.md."""
    text = skill_md.read_text(encoding="utf-8")
    idx = text.find(SKILL_ENTRY_MARKER)
    if idx == -1:
        return []

    # Find the section content (until next ## or end of file)
    after = text[idx + len(SKILL_ENTRY_MARKER):]
    next_section = SECTION_RE.search(after)
    section_text = after[:next_section.start()] if next_section else after

    rows = []
    for line in section_text.strip().splitlines():
        line = line.strip()
        # Skip header rows and separator rows
        if TABLE_ROW_RE.match(line) and "---" not in line and "Topic" not in line:
            rows.append(line)
    return rows


def extract_file_path(row: str) -> str:
    """Extract the file path (column 2) from a table row for matching."""
    cols = [c.strip() for c in row.split("|")]
    # cols[0] is empty (before first |), cols[1] is topic, cols[2] is file
    if len(cols) >= 3:
        return cols[2]
    return ""


def sync() -> bool:
    """Sync skill entries into AGENTS.md. Returns True if changes were made."""
    if not AGENTS_MD.exists():
        print(f"ERROR: {AGENTS_MD} not found")
        return False

    if not SKILLS_DIR.exists():
        print("No .claude/skills/ directory found. Nothing to sync.")
        return False

    # Collect all skill entries
    skill_rows: list[str] = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        skill_md = skill_dir / "SKILL.md"
        if skill_md.exists():
            rows = extract_skill_rows(skill_md)
            if rows:
                print(f"  Found {len(rows)} entry(s) in {skill_dir.name}")
                skill_rows.extend(rows)

    if not skill_rows:
        print("No AGENTS.md entries found in skills.")
        return False

    # Read AGENTS.md
    agents_text = AGENTS_MD.read_text(encoding="utf-8")

    # Find the Reference Table section
    ref_idx = agents_text.find(REF_TABLE_HEADER)
    if ref_idx == -1:
        print("ERROR: '## Reference Table' section not found in AGENTS.md")
        return False

    # Find the end of the reference table (next ## section)
    after_ref = agents_text[ref_idx + len(REF_TABLE_HEADER):]
    next_section_match = SECTION_RE.search(after_ref)
    if next_section_match:
        table_end = ref_idx + len(REF_TABLE_HEADER) + next_section_match.start()
    else:
        table_end = len(agents_text)

    table_section = agents_text[ref_idx:table_end]
    table_lines = table_section.splitlines()

    # Find existing file paths in the table for matching
    existing_paths = set()
    for line in table_lines:
        if TABLE_ROW_RE.match(line.strip()) and "---" not in line and "Topic" not in line:
            existing_paths.add(extract_file_path(line.strip()))

    # Determine which skill rows need to be added or updated
    changes_made = False
    new_table_lines = list(table_lines)

    for skill_row in skill_rows:
        skill_path = extract_file_path(skill_row)

        # Check if a row with this file path already exists
        found = False
        for i, line in enumerate(new_table_lines):
            if TABLE_ROW_RE.match(line.strip()) and extract_file_path(line.strip()) == skill_path:
                # Update existing row
                if line.strip() != skill_row:
                    new_table_lines[i] = skill_row
                    print(f"  Updated: {skill_path}")
                    changes_made = True
                found = True
                break

        if not found:
            # Find the last table row to insert after
            last_row_idx = 0
            for i, line in enumerate(new_table_lines):
                if TABLE_ROW_RE.match(line.strip()) and "---" not in line and "Topic" not in line:
                    last_row_idx = i
            new_table_lines.insert(last_row_idx + 1, skill_row)
            print(f"  Added: {skill_path}")
            changes_made = True

    if changes_made:
        # Rebuild AGENTS.md
        new_table_section = "\n".join(new_table_lines)
        new_agents = agents_text[:ref_idx] + new_table_section + agents_text[table_end:]
        AGENTS_MD.write_text(new_agents, encoding="utf-8")
        print(f"\nAGENTS.md updated.")
    else:
        print("\nAGENTS.md already up to date.")

    return changes_made


def main() -> int:
    print("=== Sync Skills -> AGENTS.md ===")
    sync()
    return 0


if __name__ == "__main__":
    sys.exit(main())
