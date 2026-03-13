#!/usr/bin/env python3
"""sync_skills_to_agents.py — Sync installed skills into AGENTS.md.

Scans .claude/skills/*/SKILL.md, reads YAML frontmatter (name, description),
and ensures a row exists in the Reference Table of AGENTS.md.

Generated row format:
    | <name> | `.claude/skills/<dir>/SKILL.md` | <description> |

Matching is by file path (column 2). Existing rows are updated in place.
New rows are appended at the end of the table.

Usage:
    python scripts/generators/sync_skills_to_agents.py
    or: make sync-skills
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
AGENTS_MD = ROOT / "AGENTS.md"
SKILLS_DIR = ROOT / ".claude" / "skills"

REF_TABLE_HEADER = "## Reference Table"
SECTION_RE = re.compile(r"^## ", re.MULTILINE)
TABLE_ROW_RE = re.compile(r"^\|[^|]+\|[^|]+\|[^|]+\|$")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Parse simple YAML frontmatter (key: value pairs only)."""
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    result = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            result[key.strip()] = value.strip()
    return result


def extract_file_path(row: str) -> str:
    """Extract column 2 from a table row."""
    cols = [c.strip() for c in row.split("|")]
    return cols[2] if len(cols) >= 3 else ""


def sync() -> bool:
    """Sync skill entries into AGENTS.md. Returns True if changes were made."""
    if not AGENTS_MD.exists():
        print(f"ERROR: {AGENTS_MD} not found")
        return False

    if not SKILLS_DIR.exists():
        print("No .claude/skills/ directory found. Nothing to sync.")
        return False

    # Collect skill rows from frontmatter
    skill_rows: list[str] = []
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue

        fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if not name:
            print(f"  SKIP: {skill_dir.name} (no name in frontmatter)")
            continue

        rel_path = f".claude/skills/{skill_dir.name}/SKILL.md"
        row = f"| {name} | `{rel_path}` | {desc} |"
        skill_rows.append(row)
        print(f"  Found: {name}")

    if not skill_rows:
        print("No skills with frontmatter found.")
        return False

    # Read AGENTS.md
    agents_text = AGENTS_MD.read_text(encoding="utf-8")

    ref_idx = agents_text.find(REF_TABLE_HEADER)
    if ref_idx == -1:
        print("ERROR: '## Reference Table' not found in AGENTS.md")
        return False

    # Find the table boundaries
    after_ref = agents_text[ref_idx + len(REF_TABLE_HEADER):]
    next_section_match = SECTION_RE.search(after_ref)
    table_end = ref_idx + len(REF_TABLE_HEADER) + (next_section_match.start() if next_section_match else len(after_ref))

    table_section = agents_text[ref_idx:table_end]
    table_lines = table_section.splitlines()

    changes_made = False
    new_table_lines = list(table_lines)

    for skill_row in skill_rows:
        skill_path = extract_file_path(skill_row)

        # Check if row with this path already exists
        found = False
        for i, line in enumerate(new_table_lines):
            if TABLE_ROW_RE.match(line.strip()) and extract_file_path(line.strip()) == skill_path:
                if line.strip() != skill_row:
                    new_table_lines[i] = skill_row
                    print(f"  Updated: {skill_path}")
                    changes_made = True
                found = True
                break

        if not found:
            # Append after last table row
            last_row_idx = 0
            for i, line in enumerate(new_table_lines):
                if TABLE_ROW_RE.match(line.strip()) and "---" not in line and "Topic" not in line:
                    last_row_idx = i
            new_table_lines.insert(last_row_idx + 1, skill_row)
            print(f"  Added: {skill_path}")
            changes_made = True

    if changes_made:
        new_table_section = "\n".join(new_table_lines)
        new_agents = agents_text[:ref_idx] + new_table_section + agents_text[table_end:]
        AGENTS_MD.write_text(new_agents, encoding="utf-8")
        print("\nAGENTS.md updated.")
    else:
        print("\nAGENTS.md already up to date.")

    return changes_made


def main() -> int:
    print("=== Sync Skills -> AGENTS.md ===")
    sync()
    return 0


if __name__ == "__main__":
    sys.exit(main())
