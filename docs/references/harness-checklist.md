# Unified Harness Engineering Checklist

> Derived from OpenAI's "Harness engineering: leveraging Codex in an agent-first world".
>
> Legend: **Y** = present, **P** = partial, **N** = missing, **—** = not applicable
>
> Column **Файлы** — конкретные файлы репозитория, реализующие пункт.
>
> Пункты помеченные `[OAI]` — добавлены из OpenAI LLM-audit checklist.

---

## 0. Operating Model `[OAI]`

| # | Practice | | Файлы |
|---|----------|-|-------|
| 0.1 | "Humans steer, agents execute" stated as explicit operating model | Y | `AGENTS.md` строка 3, `README.md`, `docs/references/METHOD.md` → "Принцип" |
| 0.2 | Engineers operate through prompts/plans/reviews, not manual coding habits | Y | `AGENTS.md` → Task Loop (11 шагов), `docs/references/METHOD.md` (6-step cycle) |
| 0.3 | On agent failure → improve capability/tooling, not "try harder" | Y | `AGENTS.md` → Failure Ledger (строки 109-114): failure → fix → enforcement |
| 0.4 | Humans work at prioritization/acceptance level, agents at execution | P | `AGENTS.md` → Autonomy table + `METHOD.md` → "Человек задаёт цель". Implicit, нет явной формулировки "humans prioritize backlog" |

---

## 1. Repository as System of Record

| # | Practice | | Файлы |
|---|----------|-|-------|
| 1.1 | AGENTS.md exists as short (~100 line) table of contents | Y | `AGENTS.md` (119 строк) |
| 1.2 | AGENTS.md has quick-command table (goal → make target) | Y | `AGENTS.md` → секция "Available Tools" (строки 39-53) |
| 1.3 | Knowledge lives in structured `docs/` directory | Y | `docs/` — 20+ файлов: design-docs, exec-plans, generated, product-specs, references |
| 1.4 | Design docs catalogued and indexed with verification status | Y | `docs/design-docs/index.md` (колонки: Document, Status, Last Verified, Owner) |
| 1.5 | docs/design-docs/core-beliefs.md — agent-first operating principles | Y | `.claude/skills/harness.core/docs/CORE_PRINCIPLES.md` (7 core beliefs) |
| 1.6 | Execution plans as first-class artifacts (active/completed/tech-debt) | Y | `docs/exec-plans/active/`, `docs/exec-plans/completed/`, `docs/exec-plans/tech-debt-tracker.md` |
| 1.7 | Progressive disclosure: small entry point → deeper docs | Y | `AGENTS.md` → Reference Table (строки 74-92) → ссылки на глубокие доки |
| 1.8 | No external knowledge dependency | Y | Всё в репо: `docs/`, `policies/`, `.claude/skills/` |
| 1.9 | Doc-gardening agent/process | Y | `.claude/skills/harness.entropy/SKILL.md`, `.claude/skills/harness.linters/scripts/doc-health/doc_health_check.py`, `Makefile` target `gardener` |
| 1.10 | Verification headers in docs (last-verified date, status) | Y | `docs/design-docs/index.md` — колонки Status + Last Verified |
| 1.11 | Process to encode external knowledge (Slack/Docs/heads) into repo `[OAI]` | P | `.claude/skills/harness.core/docs/CORE_PRINCIPLES.md` Principle #1: "If it is not committed, it does not exist". Принцип есть, но нет documented how-to процесса втягивания |
| 1.12 | Explicit docs per domain: architecture, design, product, plans, reliability, security, quality, observability `[OAI]` | Y | `ARCHITECTURE.md`, `docs/PROJECT_DESIGN.md`, `docs/PROJECT_PRODUCT_SENSE.md`, `docs/exec-plans/`, `docs/PROJECT_RELIABILITY.md`, `docs/PROJECT_SECURITY.md`, `docs/PROJECT_QUALITY_SCORE.md`, `docs/PROJECT_OBSERVABILITY.md` — все 8 доменов |

---

## 2. AGENTS.md Design

| # | Practice | | Файлы |
|---|----------|-|-------|
| 2.1 | Short (~100 lines), not monolithic | Y | `AGENTS.md` (119 строк) |
| 2.2 | Pointers to deeper sources of truth | Y | `AGENTS.md` → Reference Table (строки 74-92) |
| 2.3 | Project map with file/folder → purpose | Y | `AGENTS.md` → Reference Table (Topic → File → When to load) |
| 2.4 | Development workflow steps listed | Y | `AGENTS.md` → Task Loop (строки 19-31), Cadenced Ops (строки 33-37) |
| 2.5 | Key constraints section (what agent must NOT do) | Y | `AGENTS.md` → Core Rules (строки 64-72), DO NOT USE (строки 55-62) |

---

## 3. Layered Domain Architecture

| # | Practice | | Файлы |
|---|----------|-|-------|
| 3.1 | Strict layer ordering defined | Y | `policies/architecture.yaml` (layers + allowed_imports), `ARCHITECTURE.md` → "Логика слоёв" |
| 3.2 | Providers as single cross-cutting abstraction | Y | `policies/architecture.yaml` → `cross_cutting_modules`, `AGENTS.md` строка 66 |
| 3.3 | Dependency direction: forward-only | Y | `.claude/skills/harness.linters/scripts/architecture/test_layer_dependencies.py` (AST-проверка) |
| 3.4 | ARCHITECTURE.md with domain map + quality grades | Y | `ARCHITECTURE.md` → "Основные зоны" + Quality Grades (A/B/C/D) |
| 3.5 | Custom linters enforce layer boundaries | Y | `.claude/skills/harness.linters/scripts/architecture/test_layer_dependencies.py` |
| 3.6 | Structural tests validate dependency direction | Y | `.claude/skills/harness.linters/scripts/architecture/test_layer_dependencies.py`, `Makefile` target `structural` |
| 3.7 | Data parsed at layer boundaries | Y | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` (Principle #2: boundary validation) |

---

## 4. Application Legibility

| # | Practice | | Файлы |
|---|----------|-|-------|
| 4.1 | App bootable per git worktree | Y | `scripts/harness/worktree_boot.py`, `.claude/skills/harness.core/docs/WORKTREE_WORKFLOW.md` |
| 4.2 | Local observability stack (logs/metrics/traces) | Y | `docs/PROJECT_OBSERVABILITY.md` (Phase 1-3), `.claude/skills/harness.generators/scripts/observability/structured_log.py` |
| 4.3 | Agent can query logs (LogQL) and metrics (PromQL) | Y | `docs/PROJECT_OBSERVABILITY.md` → agent capabilities: log, metric, query, summary |
| 4.4 | Chrome DevTools / browser automation for UI validation | Y | `.claude/skills/harness.core/docs/BROWSER_AUTOMATION.md` (Playwright MCP, agent-browser CLI, Chrome DevTools MCP) |
| 4.5 | Observability scripts (obs-up / obs-down) | Y | `Makefile` targets `obs-up`, `obs-down` (строка 54 AGENTS.md) |
| 4.6 | Acceptance checks defined (startup time, no errors in smoke) | Y | `docs/PROJECT_OBSERVABILITY.md` → acceptance checks, `policies/control-loop-metrics.yaml` → setpoints |
| 4.7 | Agent legibility is explicit design goal `[OAI]` | Y | `.claude/skills/harness.core/docs/CORE_PRINCIPLES.md` Principle #2: "Documentation and architecture are written for **agent consumption first**" |
| 4.8 | Technology choices favor agent-inspectable, predictable stacks `[OAI]` | P | `.claude/skills/harness.anti-overengineering/SKILL.md` (12 rules: simplicity, linear flow, readability). Философия есть, но нет анализа конкретных tech choices |
| 4.9 | Evidence-based prompts: perf/latency/SLO constraints available to agent `[OAI]` | Y | `policies/control-loop-metrics.yaml` (5 setpoints с targets и alert thresholds), `docs/PROJECT_OBSERVABILITY.md` → acceptance checks |

---

## 5. Enforcing Architecture & Taste

| # | Practice | | Файлы |
|---|----------|-|-------|
| 5.1 | Golden principles doc (mechanical taste invariants) | Y | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` (14 mechanical invariants) |
| 5.2 | Custom linters with actionable error messages | Y | `.claude/skills/harness.linters/scripts/code-quality/code_conventions.py`, `.claude/skills/harness.linters/scripts/code-quality/validate_lint_rules.py` |
| 5.3 | Structural tests (AST-based layer dependency checks) | Y | `.claude/skills/harness.linters/scripts/architecture/test_layer_dependencies.py` |
| 5.4 | Taste invariants: structured logging enforced | Y | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` → Principle #13, `.claude/skills/harness.generators/scripts/observability/structured_log.py` |
| 5.5 | Taste invariants: naming conventions enforced | Y | `.claude/skills/harness.linters/scripts/code-quality/code_conventions.py` |
| 5.6 | Taste invariants: file size limits enforced | Y | `policies/architecture.yaml` → `file_size: { soft_limit: 500, hard_limit: 1500 }` |
| 5.7 | Invariants over micromanagement | Y | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` — каждый принцип = механическое правило |
| 5.8 | Human taste fed back via docs/tooling, not ad-hoc | Y | `AGENTS.md` → Failure Ledger (строки 109-114): failure → fix → enforcement |
| 5.9 | Linter errors include remediation hints useful to agent `[OAI]` | Y | `code_conventions.py`: `"Fix: split into smaller modules. See Golden Principle 5."`, `doc_linter.py`: `"Fix: add [HUMAN], [AI]..."` — все ошибки с Fix + ссылкой |

---

## 6. Golden Principles

| # | Practice | | Файлы |
|---|----------|-|-------|
| 6.1 | Shared utilities over hand-rolled helpers | Y | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` → Principle #1 |
| 6.2 | Boundary validation (typed SDKs, no YOLO data probing) | Y | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` → Principle #2 |
| 6.3 | Prefer boring technology | Y | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` → Principle #3 |
| 6.4 | Each principle maps to an enforcement mechanism | Y | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` — каждый принцип имеет "Enforced by" |
| 6.5 | Principles are mechanical rules, not philosophy | Y | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` — 14 конкретных правил с линтерами |
| 6.6 | Parse-don't-validate: invalid states unrepresentable `[OAI]` | Y | `.claude/skills/harness.core/docs/GOLDEN_PRINCIPLES.md` → Principle #14: "Parse, Don't Validate" — parse at boundaries, encode invariants in types, make invalid states unrepresentable |

---

## 7. Entropy & Garbage Collection

| # | Practice | | Файлы |
|---|----------|-|-------|
| 7.1 | ENTROPY.md doc defining drift sources and cleanup cadence | Y | `.claude/skills/harness.core/docs/ENTROPY_PRINCIPLES.md` |
| 7.2 | Entropy check script (stale docs, dead scripts, orphan TODOs) | Y | `.claude/skills/harness.linters/scripts/entropy/entropy_check.py` |
| 7.3 | Quality grades per domain/layer (A/B/C/D with tracking) | Y | `ARCHITECTURE.md` → Quality Grades table |
| 7.4 | Background Codex tasks for refactoring PRs | Y | `.github/workflows/weekly-cleanup.yml` (авто-фикс энтропии + создание PR) |
| 7.5 | Nightly/weekly entropy scan separate from PR CI | Y | `.github/workflows/nightly-entropy.yml` (daily 03:00 UTC), `.github/workflows/weekly-cleanup.yml` (weekly Mon 06:00 UTC) |
| 7.6 | Tech-debt tracker doc | Y | `docs/exec-plans/tech-debt-tracker.md` |

---

## 8. CI & Merge Philosophy

| # | Practice | | Файлы |
|---|----------|-|-------|
| 8.1 | Stable command surface: `make smoke`, `make check`, `make test`, `make ci` | Y | `Makefile` — targets: smoke, check, test, ci, review, entropy, gardener, build, structural |
| 8.2 | CI runs lint + typecheck + structural tests + unit tests | Y | `.github/workflows/ci.yml` (static checks → structural → doc-drift → full test), `.claude/skills/harness.ci/scripts/lint_runner.py`, `.claude/skills/harness.ci/scripts/typecheck.py` |
| 8.3 | Minimal blocking merge gates (speed over perfection) | Y | `docs/design-docs/ci-enforcement.md` |
| 8.4 | Short-lived PRs, flakes addressed with follow-up runs | Y | `docs/design-docs/ci-enforcement.md` |
| 8.5 | CI config as code in repo (.github/workflows/) | Y | `.github/workflows/ci.yml`, `.github/workflows/nightly-entropy.yml`, `.github/workflows/weekly-cleanup.yml` |
| 8.6 | `make ci` = exact local reproduction of CI pipeline | Y | `Makefile` target `ci` |
| 8.7 | Throughput-aware: designed for agent output > human review bandwidth `[OAI]` | P | `.claude/skills/harness.core/docs/CORE_PRINCIPLES.md` Principle #3: "Corrections Are Cheap. Blocking Is Expensive." + `control-loop-metrics.yaml` → merge_cycle_time. Философия есть, но нет явного обсуждения tradeoff agent throughput vs human bandwidth |

---

## 9. Policy-as-Code

| # | Practice | | Файлы |
|---|----------|-|-------|
| 9.1 | risk-policy.json exists (risk tiers, watch paths, doc drift) | Y | `policies/risk-policy.json` (tiers: low/medium/high, watchPaths, docsDriftRules) |
| 9.2 | Watch paths map source dirs to docs | Y | `policies/risk-policy.json` → `watchPaths` (src/, scripts/harness/, policies/) + `docsDriftRules` (5 правил) |
| 9.3 | CI or agent self-review reads risk-policy.json | Y | `.claude/skills/harness.linters/scripts/doc-health/check_doc_drift.py`, `.claude/skills/harness.ci/scripts/pre_pr_gate.py` |
| 9.4 | .coderabbit.yaml or equivalent AI code review config | Y | `policies/.coderabbit.yaml` |

---

## 10. Agent Autonomy & Workflow

| # | Practice | | Файлы |
|---|----------|-|-------|
| 10.1 | Agent reviews own changes locally before PR | Y | `Makefile` target `review`, `.claude/skills/harness.ci/scripts/pre_pr_gate.py` |
| 10.2 | Agent-to-agent review | Y | `.claude/agents/harness/reviewer.md`, `AGENTS.md` → Task Loop шаг 8 |
| 10.3 | Agent can: validate → reproduce → fix → validate → open PR | **P** | `AGENTS.md` → Task Loop (11 шагов). Partial — нет running app для полного цикла reproduce→fix |
| 10.4 | Escalation only when human judgment required | Y | `AGENTS.md` → Autonomy table (строки 9-15): Low/Medium/High risk → разные действия |
| 10.5 | Agent control-loop metrics / setpoints defined | Y | `policies/control-loop-metrics.yaml` (pr_pass_at_1, merge_cycle_time, revert_rate, human_intervention_rate, time_to_actionable_failure) |
| 10.6 | Skills registry (filesystem, observability, browser, etc.) | Y | `.claude/skills/` — 6 skill-модулей + slash commands в `AGENTS.md` |
| 10.7 | Visible autonomy ladder: documented progression path, not all-or-nothing `[OAI]` | P | `AGENTS.md` → Autonomy table (3 risk tiers), `policies/risk-policy.json`. Тиры есть, но нет roadmap наращивания автономии по фазам (Phase 1 → 2 → 3) |

---

## 11. Plans & Execution

| # | Practice | | Файлы |
|---|----------|-|-------|
| 11.1 | PLANS.md spec for execution plans | Y | `docs/PLANS.MD`, `.claude/skills/harness.planner/OPENAI_PLANS.md` (каноничный формат) |
| 11.2 | exec-plans/active/ and completed/ directories | Y | `docs/exec-plans/active/`, `docs/exec-plans/completed/` |
| 11.3 | Plans are self-contained (novice can implement from plan alone) | Y | `.claude/skills/harness.planner/SKILL.md` — правила создания ExecPlan |
| 11.4 | Living plan sections (progress log, decision log, retrospective) | Y | `.claude/skills/harness.planner/OPENAI_PLANS.md` → формат плана с секциями |
| 11.5 | Product specs in-repo (not external tools) | Y | `docs/product-specs/index.md`, `docs/PROJECT_DESIGN.md`, `docs/PROJECT_PRODUCT_SENSE.md`, `docs/PROJECT_FRONTEND.md` |
| 11.6 | Acceptance criteria explicit enough for agent to verify completion `[OAI]` | Y | `.claude/skills/harness.planner/OPENAI_PLANS.md` → "Validation and Acceptance" mandatory section: "Phrase acceptance as behavior a human can verify". + `docs/PROJECT_OBSERVABILITY.md` → acceptance checks + `policies/control-loop-metrics.yaml` → setpoints |

---

## 12. Agent-Generated Everything

| # | Practice | | Файлы |
|---|----------|-|-------|
| 12.1 | Product code and tests | — | Нет application code (EnHarnes — harness-фреймворк, не приложение) |
| 12.2 | CI configuration and release tooling | Y | `.github/workflows/ci.yml`, `.github/workflows/nightly-entropy.yml`, `.github/workflows/weekly-cleanup.yml` |
| 12.3 | Internal developer tools (scripts, linters) | Y | `.claude/skills/harness.linters/scripts/` (7 скриптов), `.claude/skills/harness.ci/scripts/` (4 скрипта), `policies/ast-grep/` (5 правил) |
| 12.4 | Documentation and design history | Y | `docs/generated/project-handbook.md`, `docs/generated/scripts_registry.md`, `docs/generated/todo-registry.md`, `docs/generated/db-schema.md` |
| 12.5 | Scripts that manage the repository itself | Y | `.claude/skills/harness.generators/scripts/` (build_handbook, sync_doc_indexes, sync_skills_to_agents, sync_todo_registry), `scripts/harness/worktree_boot.py` |
| 12.6 | Evaluation harnesses | Y | `.claude/skills/harness.linters/` (вся подсистема линтеров), `.claude/skills/harness.ci/scripts/measure_metrics.py` |

---

## 13. Rollout & Onboarding

| # | Practice | | Файлы |
|---|----------|-|-------|
| 13.1 | Baseline recording (current entrypoints, flaky checks, environments) | Y | `.claude/skills/harness.core/docs/baseline-template.md` |
| 13.2 | Wizard/bootstrap to scaffold harness from scratch | **N** | By design: EnHarnes — конкретный инстанс, не шаблон. Bootstrap = harness-core plugin |
| 13.3 | Harness audit script runnable in CI | Y | `.claude/skills/harness.ci/scripts/pre_pr_gate.py`, `.github/workflows/ci.yml` |
| 13.4 | Static analysis mandatory before full test runs | Y | `.github/workflows/ci.yml` → static checks → structural → doc-drift → full test (строгий порядок) |
| 13.5 | Periodic review cadence for doc/script drift | Y | `.github/workflows/nightly-entropy.yml`, `AGENTS.md` → Cadenced Ops (weekly/monthly) |
| 13.6 | New contributors can run harness commands without tribal knowledge | Y | `AGENTS.md` → Available Tools table, `Makefile` (все команды — `make <target>`) |
| 13.7 | Agent runs reproducible from clean checkout | Y | `Makefile`, `requirements.txt`, `scripts/harness/worktree_boot.py` |
| 13.8 | Core workflows observable and debuggable | Y | `docs/PROJECT_OBSERVABILITY.md`, `.claude/skills/harness.generators/scripts/observability/structured_log.py` |

---

## 14. Safety & Hooks

| # | Practice | | Файлы |
|---|----------|-|-------|
| 14.1 | PreToolUse hooks for bash/command validation | Y | `.claude/hooks/validate-bash.py`, `.claude/settings.json` → PreToolUse |
| 14.2 | Prompt validation hooks (secret detection) | Y | `.claude/hooks/prompt-validator.py`, `.claude/settings.json` → UserPromptSubmit |
| 14.3 | Post-response hooks (auto-sync, doc generation) | Y | `.claude/hooks/post-response-sync.py`, `.claude/settings.json` → Stop |
| 14.4 | Config-as-code (harness-config.yaml or equivalent) | Y | `policies/risk-policy.json`, `policies/architecture.yaml`, `policies/control-loop-metrics.yaml`, `policies/doc-indexes.yaml` |
| 14.5 | ast-grep rules for code pattern enforcement | Y | `policies/ast-grep/no-bare-except.yml`, `no-breakpoint.yml`, `no-star-import.yml`, `no-exit-in-library.yml`, `no-os-environ-direct.yml` + `policies/ast-grep-tests/` |
| 14.6 | AGENTS.md as failure ledger (failure → fix → enforcement) | Y | `AGENTS.md` → Failure Ledger (строки 109-114) |
| 14.7 | Tool declaration table (safe vs dangerous operations) | Y | `AGENTS.md` → Available Tools (строки 39-53) + DO NOT USE (строки 55-62) |
| 14.8 | Doc index auto-generation | Y | `.claude/skills/harness.generators/scripts/sync_doc_indexes.py`, `policies/doc-indexes.yaml` |

---

## 15. Closed-Loop Evidence `[OAI]`

| # | Practice | | Файлы |
|---|----------|-|-------|
| 15.1 | At least one completed task→impl→verify→review→merge cycle evidenced | Y | Git history: 73 коммита, 10+ merged PRs (codex/* branches → main). Примеры: `4b4ab73` "Split harness into 6 skills", `7fbb1c8` "Restructure harness" |

---

## Score Summary

| Category | Items | Max | Score | % |
|----------|-------|-----|-------|---|
| 0. Operating Model `[OAI]` | 4 | 8 | 7 | 88% |
| 1. Repo as System of Record | 12 | 24 | 22 | 92% |
| 2. AGENTS.md Design | 5 | 10 | 10 | 100% |
| 3. Layered Architecture | 7 | 14 | 14 | 100% |
| 4. Application Legibility | 9 | 18 | 17 | 94% |
| 5. Enforcing Taste | 9 | 18 | 18 | 100% |
| 6. Golden Principles | 6 | 12 | 12 | 100% |
| 7. Entropy/GC | 6 | 12 | 12 | 100% |
| 8. CI & Merge | 7 | 14 | 13 | 93% |
| 9. Policy-as-Code | 4 | 8 | 8 | 100% |
| 10. Agent Autonomy | 7 | 14 | 12 | 86% |
| 11. Plans & Execution | 6 | 12 | 12 | 100% |
| 12. Agent-Generated | 6 | 12 | 10 | 83% |
| 13. Rollout/Onboarding | 8 | 16 | 14 | 88% |
| 14. Safety & Hooks | 8 | 16 | 16 | 100% |
| 15. Closed-Loop Evidence `[OAI]` | 1 | 2 | 2 | 100% |
| **TOTAL** | **105** | **210** | **199** | **95%** |

---

## Open Gaps (5%)

| # | Practice | Status | Причина | Remediation |
|---|----------|--------|---------|-------------|
| 0.4 | Humans at prioritization level | **P** | Implicit в Autonomy table, нет явной формулировки | Добавить строку в METHOD.md: "Humans own the backlog and acceptance; agents own execution" |
| 1.11 | Process to encode external knowledge | **P** | Принцип "if not committed, doesn't exist" есть, но нет how-to | Добавить секцию в WORKFLOW_RULES.md: process Slack/Docs → repo artifacts |
| 4.8 | Tech choices for agent-legibility | **P** | Anti-overengineering покрывает философию, нет анализа конкретных решений | Добавить раздел в ARCHITECTURE.md: "Why these technologies" |
| 8.7 | Throughput-aware merge | **P** | "Corrections cheap, blocking expensive" есть, но нет явного throughput discussion | Добавить параграф в ci-enforcement.md |
| 10.3 | Full autonomy loop | **P** | Нет running app для reproduce→fix | Закроется когда появится application code |
| 10.7 | Visible autonomy ladder | **P** | Тиры есть, roadmap фаз нет | Добавить Phase 1→2→3 autonomy progression в METHOD.md |
| 12.1 | Product code and tests | **—** | N/A — harness-фреймворк | — |
| 13.2 | Wizard/bootstrap | **N** | By design — bootstrap живёт в harness-core | — |
