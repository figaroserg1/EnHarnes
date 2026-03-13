# Golden Principles

These are mechanical invariants, not advice.
Every rule here maps directly to a linter check or structural test.
If a principle cannot be enforced automatically, it belongs in `.claude/skills/harness.core/docs/WORKFLOW_RULES.md` instead.

 ---

## Structural Rules

**1. Layered imports only flow downward.**
`Types → Config → Repo → Service → Runtime → UI`
Cross-cutting concerns go through `Providers` only.
Enforced by: `.claude/skills/harness.linters/scripts/architecture/test_layer_dependencies.py`

**2. Validate at layer boundaries. Never inside.**
Data entering the system (API, queue, CLI) is validated at the boundary.
Inside the system, code works with already-valid typed models — no defensive re-parsing.
Enforced by: structural test + code review gate.

**3. No business logic in the UI layer.**
UI modules (`src/UI/`) may not import from `src/Repo/` directly.
Computation and branching belong in `Service` or `Runtime`.
Enforced by: `.claude/skills/harness.linters/scripts/architecture/test_layer_dependencies.py`

**4. Structured logging only. No bare print statements in production code.**
Every log line must include: `service`, `env`, `trace_id`, `operation`, `result`.
Enforced by: `.claude/skills/harness.linters/scripts/code-quality/code_conventions.py` (Rule 4: bare print() detection in src/)

**5. Max file size: 500 lines soft limit, 1500 lines hard limit.**
Files above 500 lines get a warning. Above 1500 lines blocks merge (except `generated/`).
Enforced by: `.claude/skills/harness.linters/scripts/code-quality/code_conventions.py` (Rule 5: file size limits on src/ files)

**6. Every TODO in a markdown file must have an owner tag.**
Format: `TODO: [HUMAN]`, `TODO: [AI]`, or `TODO: [AI->HUMAN]`
Enforced by: `.claude/skills/harness.linters/scripts/doc-health/todo_linter.py`


---

**7. No direct data probing or dynamic shape guessing.**
Code must not infer data structure via ad-hoc property access or trial parsing.
Allowed sources of truth: typed SDKs, validated schemas, shared model utilities.
Forbidden patterns include inline shape probing (`obj["maybe"]`, deep optional chaining without types, manual JSON guessing).
Purpose: prevent AI from building logic on unstable assumptions.
Enforced by: `.claude/skills/harness.linters/scripts/doc-health/todo_linter.py` (planned: AST rule scanning dynamic key access outside schema modules)

---

**8. Shared utilities over local helpers.**
If a function duplicates logic already present in `src/utils/` or shared packages, it must reuse the existing implementation.
Local helper duplication increases entropy and breaks invariants.
Enforced by: `.claude/skills/harness.linters/scripts/architecture/test_duplicate_helpers.py` (similarity scan or import whitelist)

---

**9. Idempotent external side-effects only.**
Modules interacting with external systems (webhooks, queues, payments, async jobs) must expose an idempotency mechanism (`idempotency_key`, retry-safe handler, or deduplication guard).
Enforced by: `.claude/skills/harness.linters/scripts/architecture/test_side_effect_patterns.py` (scan Runtime/Service layers for external clients without idempotency wrapper)

---

**10. Trace context propagation required across async boundaries.**
Any async job, queue handler, or background task must propagate `trace_id` or equivalent context field.
Purpose: maintain observability consistency for agent-generated code.
Enforced by: `.claude/skills/harness.linters/scripts/doc-health/todo_linter.py` (planned: check function signatures or logging context usage)

---

**11. Public contracts must be versioned or additive-only.**
Changes to API routes, events, or shared schemas must be additive or versioned (`v1`, `v2`, etc.).
Breaking changes without explicit version namespace are disallowed.
Enforced by: `.claude/skills/harness.linters/scripts/architecture/test_contract_changes.py` (diff-based schema/API check)

---

**12. Providers are the only allowed cross-cutting abstraction layer.**
Shared concerns such as auth, config loading, logging, tracing, or secrets must be accessed via `Providers`.
Direct cross-layer imports to implement cross-cutting logic are forbidden.
Enforced by: `.claude/skills/harness.linters/scripts/architecture/test_layer_dependencies.py`

---

**13. Detailed logging required — console and file.**
All production code must emit verbose structured logs to both console and file.
Every operation, decision branch, and error must be logged with enough context for an agent to diagnose issues without guessing or adding debug prints.
Minimum fields: `service`, `operation`, `result`, `duration_ms`, `error` (if any).
File logs go to `logs/` directory (gitignored). Console logs use human-readable format.
Enforced by: `.claude/skills/harness.linters/scripts/code-quality/code_conventions.py` (planned: check that service modules contain logging setup)


--- 

**14. Parse, Don’t Validate**
- Parse untrusted input at system boundaries.
- Convert raw data immediately into strict domain models.
- Work only with parsed, trusted representations.
- Encode invariants in types, schemas, constructors, and value objects.
- Do not scatter repeated validation checks across the codebase.
- Fail early and explicitly on invalid input.
- Make invalid states unrepresentable.

