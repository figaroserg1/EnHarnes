# Scripts Reference

All scripts are cross-platform (Python) unless marked as platform-specific stubs.
Python scripts work on Windows, Linux, and macOS with Python 3.10+.

---

## scripts/dev/worktree_boot.py

Creates an isolated git worktree for an agent task. Auto-detects runtime (Python/Node/Rust), installs dependencies, runs smoke check.

```bash
python scripts/dev/worktree_boot.py feature-login
# Creates ../worktree_feature-login on branch task/feature-login
```

---

## scripts/health/agent_self_review.py

Pre-PR gate — 5 sequential checks: static analysis (`make check`), structural tests (`make structural`), doc-drift validation, watch-path reminders from `risk-policy.json`, entropy spot-check. Exit 1 = don't open PR.

```bash
python scripts/health/agent_self_review.py
# or: make review
```

---

## scripts/health/check_doc_drift.py

Reads `policies/risk-policy.json`, verifies all `docsDriftRules` documents exist. If changed files match a watch path, warns about docs to update. Runs in CI and self-review.

```bash
python scripts/health/check_doc_drift.py
```

---

## scripts/health/doc_gardener.py

Documentation health checker — 5 checks:
1. Stale verification headers (older than 30 days)
2. Broken internal markdown links
3. Sparse index files (< 5 lines)
4. Doc lint (calls `custom_linter.py`)
5. Doc drift (calls `check_doc_drift.py`)

```bash
python scripts/health/doc_gardener.py
# or: make gardener
```

---

## scripts/health/entropy_check.py

Scans for project degradation:
1. Unreplaced `REPLACE ME` placeholders in docs/
2. Orphan scripts not referenced in Makefile or CI
3. Blank target values in `policies/control-loop-metrics.yaml`
4. Python files over 500 lines in src/
5. Missing doc references in `risk-policy.json`

```bash
python scripts/health/entropy_check.py
# or: make entropy
```

---

## scripts/health/measure_metrics.py

Measures 5 control-loop metrics via GitHub API (`gh` CLI): PR pass-at-1, merge cycle time, revert rate, human intervention rate, time to actionable failure. Compares with setpoints from `policies/control-loop-metrics.yaml`.

```bash
python scripts/health/measure_metrics.py --owner myorg --repo myrepo --days 30
```

Requires: `gh auth login`.

---

## scripts/linters/custom_linter.py

Enforces project conventions on markdown and source files:
- TODO markers must have owner: `[HUMAN]`, `[AI]`, or `[AI->HUMAN]`
- EXAMPLE blocks must contain `(REPLACE ME)`
- Files in `src/` must be kebab-case
- Layer directories must match ARCHITECTURE.md

```bash
python scripts/linters/custom_linter.py
# or: make smoke
```

---

## scripts/linters/dependency_guard.py

Enforces Golden Principles on Python source in `src/`:
- No direct Repo imports from UI layer
- No bare `print()` in production code
- File size limits (500 soft, 1500 hard)
- Cross-cutting concerns via Providers only

```bash
python scripts/linters/dependency_guard.py
```

---

## scripts/linters/lint.py

Auto-detects project type and runs the appropriate linter:
- Rust → `cargo clippy`
- Node.js → `npm run lint`
- Python → `custom_linter.py` + `dependency_guard.py`

Override via `HARNESS_LINT_CMD` environment variable.

```bash
python scripts/linters/lint.py
# or: make check
```

---

## scripts/linters/typecheck.py

Auto-detects project type and runs the appropriate type checker:
- Rust → `cargo check`
- Node.js → `npm run typecheck`
- Python → `pyright` or `mypy`

Override via `HARNESS_TYPECHECK_CMD` environment variable.

```bash
python scripts/linters/typecheck.py
```

---

## scripts/linters/validate-ast-rules.py

Validates ast-grep rule YAML files: syntax, required fields, severity values, no duplicate keys, proper nesting.

```bash
python scripts/linters/validate-ast-rules.py rules/ast-grep/
# or: make ast-rules
```

---

## scripts/generators/build_handbook.py

Generates `dist/project-handbook.md` — concatenation of core Phase 1 docs (README, METHOD, QUICKSTART, ARCHITECTURE, specs, rules) into a single file for LLM context or quick reading.

```bash
python scripts/generators/build_handbook.py
# or: make build
```

---

## scripts/generators/sync_todo_registry.py

Counts TODO markers by owner across all markdown files. Outputs summary table.

```bash
python scripts/generators/sync_todo_registry.py
# or: make todo-sync
```

---

## scripts/structural-tests/test_layer_dependencies.py

AST-based structural tests: verifies layer imports follow ARCHITECTURE.md rules. Run via pytest.

```bash
pytest scripts/structural-tests/test_layer_dependencies.py
# or: make structural
```

---

## scripts/observability/obs.py

Zero-infrastructure structured logging and metrics. Writes JSON lines to `.claude/observability/`. Has query and summary APIs.

```python
import obs
obs.log("info", "task started", component="ci")
obs.metric("startup_time_ms", 1230, component="api")
```

---

## Platform-specific stubs

These are placeholder scripts that users replace with project-specific commands.
Each has both `.sh` (Linux/Mac) and `.cmd` (Windows) versions.

| Script | Purpose | Make target |
|--------|---------|-------------|
| `scripts/dev/dev-start.sh` / `.cmd` | Start local dev environment | `make dev` |
| `scripts/dev/seed-dev-data.sh` / `.cmd` | Seed local DB with test data | `make seed` |
| `scripts/observability/obs-up.sh` / `.cmd` | Start observability stack | `make obs-up` |
| `scripts/observability/obs-down.sh` / `.cmd` | Stop observability stack | `make obs-down` |
