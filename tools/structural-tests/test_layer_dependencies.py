"""Structural dependency checks inspired by ArchUnit/pytest-archon style tests."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC_DOMAIN = ROOT / "src"
LAYERS = ("Types", "Config", "Repo", "Service", "Runtime", "UI", "Providers")

ALLOWED_LAYER_IMPORTS: dict[str, set[str]] = {
    "Types": set(),
    "Config": {"Types"},
    "Repo": {"Config", "Types"},
    "Service": {"Repo", "Config", "Types", "Providers"},
    "Runtime": {"Service", "Repo", "Config", "Types", "Providers"},
    "UI": {"Runtime", "Service", "Repo", "Config", "Types", "Providers"},
    "Providers": {"Service", "Repo", "Config", "Types"},
}


def _layer_for_file(path: Path) -> str | None:
    rel = path.relative_to(SRC_DOMAIN)
    if not rel.parts:
        return None
    layer = rel.parts[0]
    return layer if layer in LAYERS else None


def _extract_layer_from_module(module_name: str) -> str | None:
    top = module_name.split(".", 1)[0]
    return top if top in LAYERS else None


def _parse_imported_layers(path: Path) -> set[str]:
    imported: set[str] = set()
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            layer = _extract_layer_from_module(node.module)
            if layer:
                imported.add(layer)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                layer = _extract_layer_from_module(alias.name)
                if layer:
                    imported.add(layer)

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
    graph = _build_layer_graph()
    violations: list[str] = []
    for layer, deps in graph.items():
        allowed = ALLOWED_LAYER_IMPORTS[layer]
        for dep in sorted(deps):
            if dep not in allowed:
                violations.append(f"Forbidden dependency: {layer} -> {dep}")

    assert not violations, "\n".join(violations)


def test_no_cycles_in_layer_graph() -> None:
    graph = _build_layer_graph()
    cycle = _find_cycle(graph)
    assert cycle is None, f"Detected cycle in layers: {' -> '.join(cycle)}"
