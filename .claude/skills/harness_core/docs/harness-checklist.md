# Unified Harness Engineering Checklist

> Merged from `CHECKLIST.md` (148-item evaluation matrix) and `rollout-checklist.md` (4-phase rollout).
> Derived from OpenAI's "Harness engineering: leveraging Codex in an agent-first world".
>
> Legend: Y = present, P = partial, N = missing, — = not applicable
>
> Projects: **EnH** = EnHarnes, **boot** = agentic-harness-bootstrap, **ex** = example_proj,
> **skill** = harness-engineering-skill, **plug** = harness-engineering plugin,
> **reins** = reins CLI, **maj** = majestic_harness, **core** = harness-core

---

## 1. Repository as System of Record

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 1.1 | AGENTS.md exists as short (~100 line) table of contents | Y | Y | Y | — | N | Y | — | Y |
| 1.2 | AGENTS.md has quick-command table (goal → make target) | Y | N | N | — | N | Y | — | Y |
| 1.3 | Knowledge lives in structured `docs/` directory | Y | P | Y | Y | Y | Y | N | Y |
| 1.4 | Design docs catalogued and indexed with verification status | Y | N | Y | N | N | Y | N | Y |
| 1.5 | docs/design-docs/core-beliefs.md — agent-first operating principles | Y | N | Y | N | N | Y | Y | Y |
| 1.6 | Execution plans as first-class artifacts (active/completed/tech-debt) | Y | N | P | N | N | P | N | Y |
| 1.7 | Progressive disclosure: small entry point → deeper docs | Y | Y | Y | Y | Y | Y | Y | Y |
| 1.8 | No external knowledge dependency | Y | Y | Y | Y | Y | Y | Y | Y |
| 1.9 | Doc-gardening agent/process | Y | N | N | Y | N | N | N | Y |
| 1.10 | Verification headers in docs (last-verified date, status) | Y | N | Y | N | N | Y | N | Y |

---

## 2. AGENTS.md Design

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 2.1 | Short (~100 lines), not monolithic | Y | Y | Y | — | — | Y | — | Y |
| 2.2 | Pointers to deeper sources of truth | Y | Y | Y | — | — | Y | — | Y |
| 2.3 | Project map with file/folder → purpose | Y | N | Y | — | — | Y | — | Y |
| 2.4 | Development workflow steps listed | Y | Y | Y | — | — | Y | — | Y |
| 2.5 | Key constraints section (what agent must NOT do) | Y | Y | Y | — | — | Y | — | Y |

---

## 3. Layered Domain Architecture

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 3.1 | Strict layer ordering defined | Y | P | Y | Y | N | — | Y | Y |
| 3.2 | Providers as single cross-cutting abstraction | Y | N | Y | Y | N | — | P | Y |
| 3.3 | Dependency direction: forward-only | Y | P | Y | Y | N | — | Y | Y |
| 3.4 | ARCHITECTURE.md with domain map + quality grades | Y | Y | P | P | N | Y | N | Y |
| 3.5 | Custom linters enforce layer boundaries | Y | P | N | Y | N | P | P | Y |
| 3.6 | Structural tests validate dependency direction | Y | N | N | Y | N | N | P | Y |
| 3.7 | Data parsed at layer boundaries | Y | N | Y | Y | N | — | Y | Y |

---

## 4. Application Legibility

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 4.1 | App bootable per git worktree | Y | — | N | Y | — | — | Y | Y |
| 4.2 | Local observability stack (logs/metrics/traces) | Y | — | N | Y | — | — | Y | Y |
| 4.3 | Agent can query logs (LogQL) and metrics (PromQL) | Y | — | N | Y | — | — | Y | Y |
| 4.4 | Chrome DevTools / browser automation for UI validation | Y | — | N | Y | — | — | N | Y |
| 4.5 | Observability scripts (obs-up.sh / obs-down.sh) | Y | — | N | N | — | — | N | Y |
| 4.6 | Acceptance checks defined (startup time, no errors in smoke) | Y | N | N | Y | N | — | Y | Y |

---

## 5. Enforcing Architecture & Taste

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 5.1 | Golden principles doc (mechanical taste invariants) | Y | N | Y | Y | N | Y | Y | Y |
| 5.2 | Custom linters with actionable error messages | Y | P | N | Y | N | P | P | Y |
| 5.3 | Structural tests (AST-based layer dependency checks) | Y | N | N | Y | N | N | P | Y |
| 5.4 | Taste invariants: structured logging enforced | Y | N | Y | Y | N | Y | Y | Y |
| 5.5 | Taste invariants: naming conventions enforced | Y | N | Y | Y | N | Y | Y | Y |
| 5.6 | Taste invariants: file size limits enforced | Y | N | N | Y | N | N | N | Y |
| 5.7 | Invariants over micromanagement | Y | Y | Y | Y | Y | Y | Y | Y |
| 5.8 | Human taste fed back via docs/tooling, not ad-hoc | Y | Y | P | Y | Y | Y | Y | Y |

---

## 6. Golden Principles

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 6.1 | Shared utilities over hand-rolled helpers | Y | N | Y | Y | N | Y | Y | Y |
| 6.2 | Boundary validation (typed SDKs, no YOLO data probing) | Y | N | Y | Y | N | Y | Y | Y |
| 6.3 | Prefer boring technology | Y | Y | Y | Y | Y | Y | Y | Y |
| 6.4 | Each principle maps to an enforcement mechanism | Y | N | N | Y | N | P | P | Y |
| 6.5 | Principles are mechanical rules, not philosophy | Y | N | P | Y | N | Y | Y | Y |

---

## 7. Entropy & Garbage Collection

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 7.1 | ENTROPY.md doc defining drift sources and cleanup cadence | Y | N | N | Y | N | N | Y | Y |
| 7.2 | Entropy check script (stale docs, dead scripts, orphan TODOs) | Y | N | N | Y | N | N | N | Y |
| 7.3 | Quality grades per domain/layer (A/B/C/D with tracking) | Y | N | N | Y | N | Y | N | Y |
| 7.4 | Background Codex tasks for refactoring PRs | Y | N | N | Y | N | N | N | Y |
| 7.5 | Nightly/weekly entropy scan separate from PR CI | Y | N | N | Y | N | N | N | Y |
| 7.6 | Tech-debt tracker doc | Y | N | N | N | N | P | N | Y |

---

## 8. CI & Merge Philosophy

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 8.1 | Stable command surface: `make smoke`, `make check`, `make test`, `make ci` | Y | N | N | Y | N | P | N | Y |
| 8.2 | CI runs lint + typecheck + structural tests + unit tests | Y | P | N | Y | N | Y | N | Y |
| 8.3 | Minimal blocking merge gates (speed over perfection) | Y | Y | — | Y | — | Y | — | Y |
| 8.4 | Short-lived PRs, flakes addressed with follow-up runs | Y | Y | — | Y | — | Y | — | Y |
| 8.5 | CI config as code in repo (.github/workflows/) | Y | Y | N | Y | N | Y | N | Y |
| 8.6 | `make ci` = exact local reproduction of CI pipeline | Y | N | N | Y | N | Y | N | Y |

---

## 9. Policy-as-Code

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 9.1 | risk-policy.json exists (risk tiers, watch paths, doc drift) | Y | N | Y | N | N | Y | N | Y |
| 9.2 | Watch paths map source dirs to docs | Y | N | Y | N | N | Y | N | Y |
| 9.3 | CI or agent self-review reads risk-policy.json | Y | N | N | Y | N | P | N | Y |
| 9.4 | .coderabbit.yaml or equivalent AI code review config | Y | N | N | N | N | Y | N | N |

---

## 10. Agent Autonomy & Workflow

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 10.1 | Agent reviews own changes locally before PR | Y | Y | N | Y | N | Y | Y | Y |
| 10.2 | Agent-to-agent review | Y | N | N | Y | P | N | N | N |
| 10.3 | Agent can: validate → reproduce → fix → validate → open PR | P | P | N | Y | P | P | P | P |
| 10.4 | Escalation only when human judgment required | Y | Y | N | Y | Y | Y | Y | Y |
| 10.5 | Agent control-loop metrics / setpoints defined | Y | N | N | Y | N | N | Y | Y |
| 10.6 | Skills registry (filesystem, observability, browser, etc.) | Y | N | N | Y | Y | Y | N | Y |

---

## 11. Plans & Execution

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 11.1 | PLANS.md spec for execution plans | Y | N | N | Y | N | N | N | Y |
| 11.2 | exec-plans/active/ and completed/ directories | Y | N | P | N | P | P | N | Y |
| 11.3 | Plans are self-contained (novice can implement from plan alone) | Y | — | — | Y | — | — | — | Y |
| 11.4 | Living plan sections (progress log, decision log, retrospective) | Y | — | — | Y | — | — | — | Y |
| 11.5 | Product specs in-repo (not external tools) | Y | N | P | Y | N | N | N | Y |

---

## 12. Agent-Generated Everything

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 12.1 | Product code and tests | — | — | — | — | — | Y | — | — |
| 12.2 | CI configuration and release tooling | Y | Y | N | Y | N | Y | N | Y |
| 12.3 | Internal developer tools (scripts, linters) | Y | Y | N | Y | N | Y | N | Y |
| 12.4 | Documentation and design history | Y | Y | P | Y | Y | Y | N | Y |
| 12.5 | Scripts that manage the repository itself | Y | N | N | Y | N | P | N | Y |
| 12.6 | Evaluation harnesses | Y | N | N | Y | N | N | N | Y |

---

## 13. Rollout & Onboarding (from rollout-checklist.md)

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 13.1 | Baseline recording (current entrypoints, flaky checks, environments) | Y | Y | N | Y | N | P | N | P |
| 13.2 | Wizard/bootstrap to scaffold harness from scratch | N | Y | N | Y | N | Y | N | N |
| 13.3 | Harness audit script runnable in CI | Y | Y | N | Y | N | Y | N | Y |
| 13.4 | Static analysis mandatory before full test runs | Y | P | N | Y | N | Y | N | Y |
| 13.5 | Periodic review cadence for doc/script drift | Y | N | N | Y | N | N | N | Y |
| 13.6 | New contributors can run harness commands without tribal knowledge | Y | Y | N | Y | N | Y | N | Y |
| 13.7 | Agent runs reproducible from clean checkout | Y | Y | N | Y | — | Y | — | Y |
| 13.8 | Core workflows observable and debuggable | Y | N | N | Y | N | P | N | Y |

---

## 14. Safety & Hooks (additional — identified from project comparison)

| # | Practice | EnH | boot | ex | skill | plug | reins | maj | core |
|---|----------|-----|------|----|-------|------|-------|-----|------|
| 14.1 | PreToolUse hooks for bash/command validation | Y | N | N | N | Y | N | N | Y |
| 14.2 | Prompt validation hooks (secret detection) | Y | N | N | N | Y | N | N | Y |
| 14.3 | Post-response hooks (auto-sync, doc generation) | Y | N | N | N | N | N | N | Y |
| 14.4 | Config-as-code (harness-config.yaml or equivalent) | Y | N | N | N | N | N | N | Y |
| 14.5 | ast-grep rules for code pattern enforcement | Y | N | N | N | Y | N | N | Y |
| 14.6 | AGENTS.md as failure ledger (failure → fix → enforcement) | Y | N | N | N | N | N | Y | Y |
| 14.7 | Tool declaration table (safe vs dangerous operations) | Y | Y | N | N | N | N | Y | P |
| 14.8 | Doc index auto-generation | Y | N | N | N | N | N | N | Y |

---

## Score Summary

Counting Y=2, P=1, N=0 across all applicable items:

| Category | EnH | boot | ex | skill | plug | reins | maj | core |
|----------|-----|------|----|-------|------|-------|-----|------|
| 1. Repo as System of Record (20) | 19 | 7 | 13 | 9 | 5 | 15 | 6 | 19 |
| 2. AGENTS.md Design (10) | 10 | 7 | 10 | — | — | 10 | — | 10 |
| 3. Layered Architecture (14) | 14 | 5 | 7 | 13 | 0 | 3 | 8 | 14 |
| 4. Application Legibility (12) | 12 | 0 | 0 | 9 | 0 | 0 | 7 | 12 |
| 5. Enforcing Taste (16) | 16 | 5 | 7 | 16 | 3 | 11 | 10 | 16 |
| 6. Golden Principles (10) | 10 | 2 | 5 | 10 | 2 | 8 | 8 | 10 |
| 7. Entropy/GC (12) | 12 | 0 | 0 | 9 | 0 | 3 | 2 | 12 |
| 8. CI & Merge (12) | 12 | 6 | 0 | 12 | 0 | 10 | 0 | 12 |
| 9. Policy-as-Code (8) | 8 | 0 | 4 | 2 | 0 | 7 | 0 | 7 |
| 10. Agent Autonomy (12) | 10 | 5 | 0 | 11 | 5 | 6 | 7 | 8 |
| 11. Plans & Execution (10) | 10 | 0 | 2 | 8 | 1 | 1 | 0 | 10 |
| 12. Agent-Generated (12) | 10 | 6 | 1 | 10 | 2 | 8 | 0 | 10 |
| 13. Rollout/Onboarding (16) | 14 | 9 | 0 | 14 | 0 | 10 | 0 | 13 |
| 14. Safety & Hooks (16) | 16 | 2 | 0 | 0 | 6 | 0 | 5 | 15 |
| **TOTAL** | **173** | **54** | **49** | **123** | **24** | **92** | **53** | **168** |
| **Max applicable** | 180 | 170 | 170 | 164 | 150 | 170 | 148 | 180 |
| **Percentage** | **96%** | **32%** | **29%** | **75%** | **16%** | **54%** | **36%** | **93%** |

---

## Key Findings

### EnHarnes Gaps (4% remaining)
| Priority | Gap | Notes |
|----------|-----|-------|
| ~~MED~~ | ~~10.2 Agent-to-agent review~~ | **Closed** — added `agent-reviewer` skill + task loop step 7 |
| **MED** | 10.3 Full autonomy loop (validate→reproduce→fix→validate→PR) | Partial — needs running app to test full cycle |
| **LOW** | 13.2 No wizard/bootstrap scaffolding | Bootstrap is `harness-core` plugin (separate project). EnHarnes is a concrete instance, not a template. |
| ~~LOW~~ | ~~14.6 AGENTS.md not used as failure ledger~~ | **Closed** — added Failure Ledger section |
| ~~LOW~~ | ~~14.7 No tool declaration table~~ | **Closed** — added Available Tools + DO NOT USE to AGENTS.md |
| ~~LOW~~ | ~~13.1 No formal baseline recording process~~ | **Closed** — added `docs/references/baseline-template.md` |
| ~~LOW~~ | ~~8.5 CI scored as partial~~ | **Closed** — 3 workflows already existed, re-scored to Y |

### What Each Project Does Best

| Project | Strengths |
|---------|-----------|
| **EnHarnes** | Most complete implementation. Best plans, structural tests, entropy, observability, hooks, doc auto-gen |
| **harness-core** | Mirrors EnHarnes as reusable plugin. Config-driven, templated |
| **harness-skill** | Best control-system model (sensors, actuators, setpoints, feedback loops). Wizard CLI for bootstrapping |
| **reins** | Only shipping CLI product. Audit scoring, evolve, doctor commands. Best CI/publish pipeline |
| **harness-engineering** | Richest agent/skill catalog. Best commands and prompt hooks library |
| **agentic-bootstrap** | Best auto-detection (discover→analyze→generate→verify). Multi-tool compatible (Claude, Codex, Copilot) |
| **majestic_harness** | Best articulation of failure-ledger and three-pillar methodology. Pure knowledge product |
| **example_proj** | Minimal but correct template. Good for quick starts |

### What to Borrow

| From | What | Priority |
|------|------|----------|
| majestic_harness | Failure-ledger pattern for AGENTS.md | MED |
| harness-skill | Control-system docs (sensors, actuators, setpoints) | LOW |
| agentic-bootstrap | Stack auto-detection for harness-core wizard | LOW |
| reins | `doctor` command concept (health check) | LOW |
| harness-engineering | Agent definitions catalog (research, security, perf) | LOW |
