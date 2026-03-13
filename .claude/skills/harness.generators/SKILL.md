---
name: harness-generators
description: Code and doc generators — handbook builder, doc index sync, TODO registry, skill-to-agent sync, structured logging setup.
---

# Harness Generators

Scripts that generate or sync documentation artifacts and observability infrastructure.

## Scripts

### generators/
- `build_handbook.py` — Compiles harness docs into a single handbook
- `sync_doc_indexes.py` — Generates/updates index.md tables per `policies/doc-indexes.yaml`
- `sync_skills_to_agents.py` — Syncs skill definitions to agent configs
- `sync_todo_registry.py` — Scans codebase TODOs and updates registry

### observability/
- `structured_log.py` — JSON structured logging library setup (up/down)

## Dependencies

- Requires **harness-core** (for policies/ and docs)
- `sync_doc_indexes.py` reads from `policies/doc-indexes.yaml`

## Makefile Targets

```makefile
gen-handbook: build_handbook.py
sync-indexes: sync_doc_indexes.py
sync-skills:  sync_skills_to_agents.py
sync-todos:   sync_todo_registry.py
obs-up/down:  structured_log.py
```
