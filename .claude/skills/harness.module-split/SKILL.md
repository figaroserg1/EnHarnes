---
name: harness-module-split
description: Split an oversized or multi-concern module into a package, by feature, without changing behaviour or the public API. Use when a module exceeds the file-size soft limit (code_conventions Rule 5 / Golden Principle 5) or has accreted several independent concerns. Preserves every importer via package re-exports — zero blast radius. Not a logic refactor.
---

# Module Split

Turn one grown module `foo.py` into a package `foo/` whose **public surface is
unchanged**, so every `from pkg.foo import X` keeps working without edits. The
implementation moves into private, feature-scoped submodules; the package
`__init__` re-exports the public names.

This is a **pure structural move** — no behaviour change, no logic refactor. If
the module needs its logic reworked, that is a separate task (see *When not to
use* below).

## When to use

- A module trips the file-size soft limit (Golden Principle 5; warned by
  `code-health/code_conventions.py`) and the size comes from several distinct
  responsibilities rather than one irreducible algorithm.
- A module has accreted unrelated concerns that already read as separate
  sections (often marked by banner comments or grouped around distinct
  dataclasses / entry points).

Do **not** reach for this to shrink a single cohesive algorithm — extracting
helpers in place (or accepting the size with a documented reason) is better than
fragmenting one tight unit across files.

## Core idea — zero blast radius

Importers depend on names, not files. If `foo.py` becomes the package `foo/` and
`foo/__init__.py` re-exports the same names, callers and tests see no change:

```python
# foo/__init__.py — the public surface (the ONLY public module)
from ._common import shared_helper, CONSTANT
from ._reader import Row, read_rows
from ._writer import write_row

__all__ = ["shared_helper", "CONSTANT", "Row", "read_rows", "write_row"]
```

```python
# unchanged at every call site:
from pkg.foo import read_rows, write_row
```

## Procedure

1. **Map the seams.** Read the whole module. Identify independent concerns and
   the shared primitives they lean on. Each concern becomes one submodule;
   shared primitives go to `_common`.
2. **List the importers first** so you know the public contract you must keep:
   `grep -rn "pkg.foo" src tests` (and any `from .foo import …` relative forms).
   Every name imported anywhere is public and must be re-exported.
3. **Create the package.** Replace `foo.py` with a `foo/` directory:
   - `__init__.py` — carry the original module docstring, re-export the public
     names, and declare `__all__`. Keep it to re-exports; no logic.
   - `_<feature>.py` — one private submodule per concern.
   - `_common.py` — shared constants/helpers used by more than one submodule.
4. **Move, don't rewrite.** Copy each section verbatim into its submodule. Keep
   any **deferred (function-local) imports** exactly where they were — they
   usually exist to keep import light or to break a cycle; promoting them to
   module top-level can reintroduce the problem.
5. **Delete the old file** with `git rm pkg/foo.py` — a module and a package of
   the same name cannot coexist.
6. **Verify** (see checklist) before committing.

### Keep submodules private to avoid doc-coverage churn

The harness doc-coverage gate treats every **public** module (one not named
`__init__.py`/`__main__.py` and not `_`-prefixed) as something that must be
surfaced on the docs site or listed in the exceptions policy. Naming the
implementation submodules with a leading underscore (`_reader.py`, `_common.py`)
keeps them private: the gate ignores them, the package's public surface is just
its `__init__`, and no new exception entries are needed. If the original module
already had a doc-coverage exception, it now covers the package `__init__`
unchanged. Make a submodule public only if you deliberately want it documented
on its own — and then surface it or except it explicitly.

## Verification checklist

- [ ] Every name from step 2's importer list is re-exported by `__init__` and in
      `__all__`.
- [ ] Relevant tests pass (run the suites that touch the module).
- [ ] Doc-coverage gate passes (`doc-health/doc_coverage.py`): no new orphan
      modules, no stale `:::` references.
- [ ] Import smoke: importing all public names from the package and importing
      each downstream caller both succeed.
- [ ] No unused imports left in any submodule.
- [ ] Each submodule is comfortably under the size limit; the module no longer
      appears in `code_conventions.py` output.

## When not to use — escalate to a plan instead

If the module holds **shared mutable state, side effects, or tightly coupled
internal call graphs** (typical of core runtime modules), a naive split risks
circular imports and split-brain state. In that case do not move code blind:
first map the inter-section dependency graph, then propose a decomposition for
review (`harness.plan`) before touching code. Splitting is safe and mechanical
for collections of independent functions; it is a design task for stateful
engines.
