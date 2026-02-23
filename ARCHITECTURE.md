# ARCHITECTURE (high-level map)

## Repository modules
- `.github/workflows/` — CI-проверки кода и документации.
- `.agent/` — правила и шаблоны для ExecPlans.
- `docs/` — source of truth для policy/design/reliability/security/quality/планов.
- `docs/observability/` — запросы и шаблоны проверок для logs/metrics/traces.
- `scripts/` — воспроизводимые команды запуска, проверки, observability, сидирования.
- `docs/OBSERVABILITY.md`, `docs/GOLDEN_PRINCIPLES.md`, `docs/AGENT_CAPABILITIES.md`, `docs/WORKTREE_WORKFLOW.md` — advanced harness layer для агентных процессов.
- `tools/` — custom linters, structural tests, agent skills, registries.
- `examples/` — демонстрационные артефакты `EXAMPLE (REPLACE ME)`.

## Layering
- **Policy layer**: `docs/system-spec.md`, `docs/rules.md`, `docs/product-specs/`.
- **Design layer**: `docs/architecture.md`, `docs/design-docs/`, `docs/adr/`.
- **Execution layer**: `scripts/`, `.github/workflows/`, `tooling/`, `tools/`, `docs/WORKTREE_WORKFLOW.md`.
- **Quality & risk layer**: `docs/RELIABILITY.md`, `docs/SECURITY.md`, `docs/QUALITY_SCORE.md`.
- **Planning layer**: `docs/PLANS.md`, `docs/exec-plans/`.

## Dependency rules
1. Policy и Design не зависят от `examples/`.
2. `scripts/` и `tools/` проверяют соответствие docs, но не подменяют продуктовые решения.
3. CI должен валидировать и код, и документацию.
4. Любое структурное изменение сопровождается обновлением `docs/todo-registry.md`.

## TODO
- TODO: [HUMAN] Уточнить доменную декомпозицию конкретного продукта.
- TODO: [AI] Интегрировать `tools/linters/dependency_guard.py` в общий lint pipeline.
- TODO: [AI->HUMAN] Утвердить merge policy для короткоживущих PR.
