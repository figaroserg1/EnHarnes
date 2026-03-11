#!/usr/bin/env python3
"""Validate ast-grep rule YAML files for common mistakes.

Checks:
  1. YAML syntax validity
  2. Required fields (id, language, severity, message, rule)
  3. Constraints/utils not nested inside rule: (must be top-level)
  4. Severity is one of: error, warning, hint, info
  5. No duplicate YAML keys

Usage:
    python3 scripts/linters/validate-ast-rules.py rules/ast-grep/*.yml
"""

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("[validate-ast-rules] PyYAML not installed. pip install pyyaml")
    sys.exit(1)


REQUIRED_FIELDS = {"id", "language", "severity", "message", "rule"}
VALID_SEVERITIES = {"error", "warning", "hint", "info"}
TOP_LEVEL_ONLY = {"constraints", "utils", "transform", "fix"}


class DuplicateKeyError(Exception):
    pass


def no_duplicate_loader(stream):
    """YAML loader that detects duplicate keys."""
    class NoDupLoader(yaml.SafeLoader):
        pass

    def check_duplicates(loader, node, deep=False):
        mapping = {}
        for key_node, value_node in node.value:
            key = loader.construct_object(key_node, deep=deep)
            if key in mapping:
                raise DuplicateKeyError(
                    f"Duplicate key '{key}' at line {key_node.start_mark.line + 1}"
                )
            mapping[key] = loader.construct_object(value_node, deep=deep)
        return mapping

    NoDupLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        check_duplicates,
    )
    return yaml.load(stream, Loader=NoDupLoader)


def validate_file(path: Path) -> list[str]:
    """Validate a single rule file. Returns list of error messages."""
    errors = []
    text = path.read_text(encoding="utf-8")

    # 1. YAML syntax + duplicate keys
    try:
        data = no_duplicate_loader(text)
    except DuplicateKeyError as e:
        errors.append(f"  DUPLICATE KEY: {e}")
        try:
            data = yaml.safe_load(text)
        except yaml.YAMLError:
            errors.append("  YAML SYNTAX ERROR: cannot parse file")
            return errors
    except yaml.YAMLError as e:
        errors.append(f"  YAML SYNTAX ERROR: {e}")
        return errors

    if not isinstance(data, dict):
        errors.append("  STRUCTURE: root must be a mapping")
        return errors

    # 2. Required fields
    missing = REQUIRED_FIELDS - set(data.keys())
    if missing:
        errors.append(f"  MISSING FIELDS: {', '.join(sorted(missing))}")

    # 3. Severity validation
    severity = data.get("severity", "")
    if severity and severity not in VALID_SEVERITIES:
        errors.append(
            f"  INVALID SEVERITY: '{severity}' — must be one of: {', '.join(VALID_SEVERITIES)}"
        )

    # 4. Constraints/utils must NOT be inside rule:
    rule = data.get("rule", {})
    if isinstance(rule, dict):
        nested_top = TOP_LEVEL_ONLY & set(rule.keys())
        if nested_top:
            errors.append(
                f"  WRONG PLACEMENT: {', '.join(nested_top)} must be at root level, not inside 'rule:'"
            )

    return errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate-ast-rules.py <rule-files...>")
        sys.exit(1)

    paths = []
    for arg in sys.argv[1:]:
        p = Path(arg)
        if p.is_file():
            paths.append(p)
        elif p.is_dir():
            paths.extend(p.glob("*.yml"))
            paths.extend(p.glob("*.yaml"))

    if not paths:
        print("No rule files found.")
        sys.exit(1)

    total_errors = 0
    for path in sorted(paths):
        errors = validate_file(path)
        if errors:
            print(f"FAIL: {path}")
            for e in errors:
                print(e)
            total_errors += len(errors)
        else:
            print(f"  OK: {path}")

    print(f"\n{len(paths)} files checked, {total_errors} error(s).")
    if total_errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
