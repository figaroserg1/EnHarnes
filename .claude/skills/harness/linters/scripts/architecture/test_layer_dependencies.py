"""Structural dependency checks — layer DAG, cycles, cross-cutting rules.

Reads architecture policy from policies/architecture.yaml.

Checks (per docs/harness/GOLDEN_PRINCIPLES.md):
  Rule 1  — Layer imports only flow downward.
  Rule 3  — UI must not import Repo directly.
  Rule 12 — Cross-cutting imports must go through Providers.
  Cycles  — No circular dependencies between layers.
"""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[6]
SRC_DOMAIN = ROOT / "src"


def _load_architecture() -> dict:
    """Load architecture policy from YAML (simple parser, no PyYAML needed)."""
    yaml_path = ROOT / "policies" / "architecture.yaml"
    if not yaml_path.exists():
        return {}
    text = yaml_path.read_text(encoding="utf-8")
    result: dict = {"layers": [], "allowed_imports": {}, "cross_cutting_modules": []}
    current_section = None
    current_key = None
    for line in text.splitlines():
        stripped = line.split("#")[0].strip()  # strip inline comments
        if not stripped:
            continue
        if stripped == "layers:":
            current_section = "layers"
            current_key = None
            continue
        if stripped == "allowed_imports:":
            current_section = "allowed_imports"
            current_key = None
            continue
        if stripped == "cross_cutting_modules:":
            current_section = "cross_cutting_modules"
            current_key = None
            continue
        if stripped.startswith("file_size:"):
            current_section = "file_size"
            continue
        if current_section == "layers" and stripped.startswith("- "):
            result["layers"].append(stripped[2:].strip())
        elif current_section == "allowed_imports":
            if stripped.startswith("- "):
                if current_key:
                    result["allowed_imports"].setdefault(current_key, []).append(stripped[2:].strip())
            elif ":" in stripped:
                key, _, val = stripped.partition(":")
                current_key = key.strip()
                val = val.strip()
                if val.startswith("[") and val.endswith("]"):
                    items = [x.strip() for x in val[1:-1].split(",") if x.strip()]
                    result["allowed_imports"][current_key] = items
                elif not val:
                    result["allowed_imports"][current_key] = []
        elif current_section == "cross_cutting_modules" and stripped.startswith("- "):
            result["cross_cutting_modules"].append(stripped[2:].strip())
    return result


_ARCH = _load_architecture()
LAYERS = tuple(_ARCH.get("layers", []))
ALLOWED_LAYER_IMPORTS: dict[str, set[str]] = {
    k: set(v) for k, v in _ARCH.get("allowed_imports", {}).items()
}
CROSS_CUTTING_MODULES = set(_ARCH.get("cross_cutting_modules", []))


def _layer_for_file(path: Path) -> str | None:
    rel = path.relative_to(SRC_DOMAIN)
    if not rel.parts:
        return None
    layer = rel.parts[0]
    return layer if layer in LAYERS else None


def _module_root(module_name: str) -> str:
    return module_name.split(".")[0]


def _parse_imported_layers(path: Path) -> set[str]:
    imported: set[str] = set()
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and _module_root(node.module) in LAYERS:
            imported.add(_module_root(node.module))
        elif isinstance(node, ast.Import):
            for alias in node.names:
                root = _module_root(alias.name)
                if root in LAYERS:
                    imported.add(root)

    return imported


def _build_layer_graph() -> dict[str, set[str]]:
    graph = {layer: set() for layer in LAYERS}
    for file_path in SRC_DOMAIN.rglob("*.py"):
        if file_path.name == "__init__.py":
            continue
        layer = _layer_for_file(file_path)
        if not layer:
            continue
        graph[layer].update(_parse_imported_layers(file_path) - {layer})
    return graph


def _find_cycle(graph: dict[str, set[str]]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    stack: list[str] = []

    def dfs(node: str) -> list[str] | None:
        visiting.add(node)
        stack.append(node)
        for nxt in graph[node]:
            if nxt in visiting:
                idx = stack.index(nxt)
                return stack[idx:] + [nxt]
            if nxt not in visited:
                cycle = dfs(nxt)
                if cycle:
                    return cycle
        stack.pop()
        visiting.remove(node)
        visited.add(node)
        return None

    for layer in graph:
        if layer not in visited:
            cycle = dfs(layer)
            if cycle:
                return cycle
    return None


def test_layer_dependencies_follow_architecture() -> None:
    if not LAYERS:
        return
    graph = _build_layer_graph()
    violations: list[str] = []
    for layer, deps in graph.items():
        allowed = ALLOWED_LAYER_IMPORTS.get(layer, set())
        for dep in sorted(deps):
            if dep not in allowed:
                violations.append(f"Forbidden dependency: {layer} -> {dep}")

    assert not violations, "\n".join(violations)


def test_no_cycles_in_layer_graph() -> None:
    if not LAYERS:
        return
    graph = _build_layer_graph()
    cycle = _find_cycle(graph)
    assert cycle is None, f"Detected cycle in layers: {' -> '.join(cycle)}"


def _parse_all_module_names(path: Path) -> list[str]:
    """Return all imported module names (full dotted paths) from a file."""
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.append(alias.name)
    return names


def test_cross_cutting_through_providers_only() -> None:
    """Rule 12: cross-cutting modules must only be imported inside Providers/."""
    if not SRC_DOMAIN.exists() or not CROSS_CUTTING_MODULES:
        return
    violations: list[str] = []
    for py in SRC_DOMAIN.rglob("*.py"):
        if py.name == "__init__.py":
            continue
        layer = _layer_for_file(py)
        if layer == "Providers":
            continue
        for mod in _parse_all_module_names(py):
            root = _module_root(mod)
            if root.lower() in CROSS_CUTTING_MODULES:
                rel = py.relative_to(ROOT)
                violations.append(
                    f"{rel}: imports cross-cutting module '{mod}' directly. "
                    f"Route through Providers/ instead. See Golden Principle 12."
                )
    assert not violations, "\n".join(violations)
