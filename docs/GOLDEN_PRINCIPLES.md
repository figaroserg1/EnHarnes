# Golden Principles

These are mechanical invariants, not advice.
Every rule here maps directly to a linter check or structural test.
If a principle cannot be enforced automatically, it belongs in `docs/design-docs/rules.md` instead.

 ---

## Structural Rules

**1. Layered imports only flow downward.**
`Types → Config → Repo → Service → Runtime → UI`
Cross-cutting concerns go through `Providers` only.
Enforced by: `scripts/structural-tests/test_layer_dependencies.py`

**2. Validate at layer boundaries. Never inside.**
Data entering the system (API, queue, CLI) is validated at the boundary.
Inside the system, code works with already-valid typed models — no defensive re-parsing.
Enforced by: structural test + code review gate.

**3. No business logic in the UI layer.**
UI modules (`src/UI/`) may not import from `src/Repo/` directly.
Computation and branching belong in `Service` or `Runtime`.
Enforced by: `scripts/linters/dependency_guard.py`

**4. Structured logging only. No bare print statements in production code.**
Every log line must include: `service`, `env`, `trace_id`, `operation`, `result`.
Enforced by: `scripts/linters/dependency_guard.py` (Rule 4: bare print() detection in src/)

**5. Max file size: 500 lines soft limit, 1500 lines hard limit.**
Files above 500 lines get a warning. Above 1500 lines blocks merge (except `generated/`).
Enforced by: `scripts/linters/dependency_guard.py` (Rule 5: file size limits on src/ files)

**6. Every TODO in a markdown file must have an owner tag.**
Format: `TODO: [HUMAN]`, `TODO: [AI]`, or `TODO: [AI->HUMAN]`
Enforced by: `scripts/linters/custom_linter.py`


---

**7. No direct data probing or dynamic shape guessing.**
Code must not infer data structure via ad-hoc property access or trial parsing.
Allowed sources of truth: typed SDKs, validated schemas, shared model utilities.
Forbidden patterns include inline shape probing (`obj["maybe"]`, deep optional chaining without types, manual JSON guessing).
Purpose: prevent AI from building logic on unstable assumptions.
Enforced by: `scripts/linters/custom_linter.py` (AST rule scanning dynamic key access outside schema modules)

---

**8. Shared utilities over local helpers.**
If a function duplicates logic already present in `src/utils/` or shared packages, it must reuse the existing implementation.
Local helper duplication increases entropy and breaks invariants.
Enforced by: `scripts/structural-tests/test_duplicate_helpers.py` (similarity scan or import whitelist)

---

**9. Idempotent external side-effects only.**
Modules interacting with external systems (webhooks, queues, payments, async jobs) must expose an idempotency mechanism (`idempotency_key`, retry-safe handler, or deduplication guard).
Enforced by: `scripts/structural-tests/test_side_effect_patterns.py` (scan Runtime/Service layers for external clients without idempotency wrapper)

---

**10. Trace context propagation required across async boundaries.**
Any async job, queue handler, or background task must propagate `trace_id` or equivalent context field.
Purpose: maintain observability consistency for agent-generated code.
Enforced by: `scripts/linters/custom_linter.py` (check function signatures or logging context usage)

---

**11. Public contracts must be versioned or additive-only.**
Changes to API routes, events, or shared schemas must be additive or versioned (`v1`, `v2`, etc.).
Breaking changes without explicit version namespace are disallowed.
Enforced by: `scripts/structural-tests/test_contract_changes.py` (diff-based schema/API check)

---

**12. Providers are the only allowed cross-cutting abstraction layer.**
Shared concerns such as auth, config loading, logging, tracing, or secrets must be accessed via `Providers`.
Direct cross-layer imports to implement cross-cutting logic are forbidden.
Enforced by: `scripts/linters/dependency_guard.py`

---

## Naming Conventions

- Files: kebab-case (`user-service.py`, `auth-config.ts`)
- Types/Interfaces: PascalCase (`UserProfile`, `AuthConfig`)
- Functions/Variables: camelCase (`getUserProfile`, `authToken`)
- Constants: SCREAMING_SNAKE_CASE (`MAX_RETRY_COUNT`, `DEFAULT_TIMEOUT`)
- Domain directories: kebab-case (`app-settings/`)
- Layer directories: PascalCase from fixed set (`Types/`, `Config/`, `Repo/`, `Service/`, `Runtime/`, `UI/`, `Providers/`)

Enforced by: `scripts/linters/custom_linter.py` (naming convention checks on src/ files)

---

## Enforcement Summary

| Principle | Enforcer | Gate |
|-----------|----------|------|
| 1. Layer imports | `scripts/structural-tests/test_layer_dependencies.py` | `make structural` |
| 2. Boundary validation | structural test + code review | `make structural` |
| 3. No biz logic in UI | `scripts/linters/dependency_guard.py` | `make check` |
| 4. Structured logging | `scripts/linters/dependency_guard.py` + `rules/ast-grep/no-print-in-src.yml` | `make check` / `make ast-scan` |
| 5. File size limits | `scripts/linters/dependency_guard.py` | `make check` |
| 6. TODO ownership | `scripts/linters/custom_linter.py` | `make smoke` |
| 7. No data probing | `scripts/linters/custom_linter.py` (planned) | `make check` |
| 8. Shared utilities | `scripts/structural-tests/test_duplicate_helpers.py` (planned) | `make structural` |
| 9. Idempotent side-effects | `scripts/structural-tests/test_side_effect_patterns.py` (planned) | `make structural` |
| 10. Trace propagation | `scripts/linters/custom_linter.py` (planned) | `make check` |
| 11. Contract versioning | `scripts/structural-tests/test_contract_changes.py` (planned) | `make structural` |
| 12. Providers only | `scripts/linters/dependency_guard.py` | `make check` |
| Naming conventions | `scripts/linters/custom_linter.py` | `make smoke` |

Items marked **(planned)** have enforcement documented but the check is not yet implemented.
These are tracked in `docs/exec-plans/tech-debt-tracker.md`.

---

## What Is Not Here

Developer philosophy (avoid overengineering, prefer simple functions, start monolith-first)
lives in `docs/design-docs/rules.md`. It guides judgment — it is not a linter rule.
