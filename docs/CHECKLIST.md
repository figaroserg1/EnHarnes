# Harness Engineering Checklist

> Derived from the OpenAI article "Harness engineering: leveraging Codex in an agent-first world"
> (Ryan Lopopolo, Feb 11 2026). Each item is a concrete practice from the article.
>
> Legend: Y = present, P = partial, N = missing, — = not applicable

---

## 1. Repository as System of Record (p.5-8)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 1.1 | AGENTS.md exists as short (~100 line) table of contents, NOT encyclopedia | Y | Y | Y | — |
| 1.2 | AGENTS.md has quick-command table (goal → make target) | Y | Y | N | — |
| 1.3 | Knowledge lives in structured `docs/` directory | Y | Y | Y | Y |
| 1.4 | Design docs catalogued and indexed with verification status | Y | Y | Y | N |
| 1.5 | docs/design-docs/core-beliefs.md — agent-first operating principles | Y | Y | Y | N |
| 1.6 | Execution plans as first-class artifacts (active/completed/tech-debt) | Y | P | P | N |
| 1.7 | Progressive disclosure: small entry point → deeper docs elsewhere | Y | Y | Y | Y |
| 1.8 | No external knowledge dependency (Google Docs, Slack = invisible to agent) | Y | Y | Y | Y |
| 1.9 | Doc-gardening agent/process (scans for stale/obsolete docs, opens fix-up PRs) | Y | N | N | Y |
| 1.10 | Verification headers in docs (last-verified date, status) | Y | Y | Y | N |

---

## 2. AGENTS.md Design (p.5-6)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 2.1 | Short (~100 lines), not monolithic | Y | Y | Y | — |
| 2.2 | Pointers to deeper sources of truth | Y | Y | Y | — |
| 2.3 | Project map with file/folder → purpose | Y | Y | Y | — |
| 2.4 | Development workflow steps listed | Y | Y | Y | — |
| 2.5 | Key constraints section (what agent must NOT do) | Y | Y | Y | — |

---

## 3. Layered Domain Architecture (p.9-10)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 3.1 | Strict layer ordering defined (Types→Config→Repo→Service→Runtime→UI) | Y | — | Y | Y |
| 3.2 | Providers as single cross-cutting abstraction | Y | — | Y | Y |
| 3.3 | Dependency direction: forward-only (no backward imports) | Y | — | Y | Y |
| 3.4 | ARCHITECTURE.md with domain map + quality grades | Y | Y | P | N |
| 3.5 | Custom linters enforce layer boundaries | Y | P | N | Y |
| 3.6 | Structural tests validate dependency direction | Y | N | N | Y |
| 3.7 | Data parsed at layer boundaries (e.g. Zod) | Y (doc) | — | Y (doc) | Y (doc) |

---

## 4. Application Legibility (p.3-5)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 4.1 | App bootable per git worktree | P | — | N | Y |
| 4.2 | Local observability stack (logs/metrics/traces agent-readable) | P | — | N | Y |
| 4.3 | Agent can query logs (LogQL) and metrics (PromQL) | P | — | N | Y |
| 4.4 | Chrome DevTools / browser automation for UI validation | P | — | N | Y |
| 4.5 | Observability scripts (obs-up.sh / obs-down.sh) | Y | — | N | N |
| 4.6 | Acceptance checks defined (startup time, no errors in smoke) | P | — | N | Y |

---

## 5. Enforcing Architecture & Taste (p.9-11)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 5.1 | Golden principles doc (mechanical taste invariants) | Y | Y | Y | Y |
| 5.2 | Custom linters with actionable error messages (agent-readable remediation) | Y | P | N | Y |
| 5.3 | Structural tests (AST-based layer dependency checks) | Y | N | N | Y |
| 5.4 | Taste invariants: structured logging enforced | Y (doc) | Y (doc) | Y (doc) | Y |
| 5.5 | Taste invariants: naming conventions enforced | Y | Y | Y (doc) | Y |
| 5.6 | Taste invariants: file size limits enforced | Y | N | N | Y |
| 5.7 | Invariants over micromanagement (enforce boundaries, allow freedom within) | Y | Y | Y | Y |
| 5.8 | Human taste fed back via docs/tooling, not ad-hoc | Y | Y | P | Y |

---

## 6. Golden Principles (p.13-14)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 6.1 | Shared utilities over hand-rolled helpers | Y | Y | Y | Y |
| 6.2 | Boundary validation (typed SDKs, no YOLO data probing) | Y | Y | Y | Y |
| 6.3 | Prefer boring technology (composable, stable API, well-represented in training) | Y (doc) | Y | Y | Y |
| 6.4 | Each principle maps to an enforcement mechanism (linter, test, CI gate) | Y | P | N | Y |
| 6.5 | Principles are mechanical rules, not philosophy (philosophy in separate doc) | Y | Y | P | Y |

---

## 7. Entropy & Garbage Collection (p.13-14)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 7.1 | ENTROPY.md doc defining drift sources and cleanup cadence | Y | N | N | Y |
| 7.2 | Entropy check script (stale docs, dead scripts, orphan TODOs) | Y | N | N | Y |
| 7.3 | Quality grades per domain/layer (A/B/C/D with tracking) | P | Y | N | Y |
| 7.4 | Background Codex tasks for refactoring PRs (automated cleanup) | N | N | N | Y (doc) |
| 7.5 | Nightly/weekly entropy scan separate from PR CI | P | N | N | Y |
| 7.6 | Tech-debt tracker doc | Y | N | N | N |

---

## 8. CI & Merge Philosophy (p.11-12)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 8.1 | Stable command surface: `make smoke`, `make check`, `make test`, `make ci` | Y | P | N | Y |
| 8.2 | CI runs lint + typecheck + structural tests + unit tests | Y | Y | N | Y |
| 8.3 | Minimal blocking merge gates (speed over perfection) | Y | Y | — | Y |
| 8.4 | Short-lived PRs, flakes addressed with follow-up runs | Y | Y | — | Y |
| 8.5 | CI config as code in repo (.github/workflows/) | P | Y | N | N |
| 8.6 | `make ci` = exact local reproduction of CI pipeline | Y | Y | N | Y |

---

## 9. Policy-as-Code (p.9, p.14)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 9.1 | risk-policy.json exists (risk tiers, watch paths, doc drift rules) | Y | Y | Y | N |
| 9.2 | Watch paths map source dirs to docs that must stay synchronized | Y | Y | Y | N |
| 9.3 | CI or agent self-review reads risk-policy.json | Y | P | N | Y |
| 9.4 | .coderabbit.yaml or equivalent AI code review config | Y | Y | N | N |

---

## 10. Agent Autonomy & Workflow (p.3, p.12-13)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 10.1 | Agent reviews own changes locally before PR | Y | Y | N | Y |
| 10.2 | Agent-to-agent review (iterates until reviewers satisfied) | N | N | N | Y (doc) |
| 10.3 | Agent can: validate state → reproduce bug → fix → validate → open PR | N | P | N | Y (doc) |
| 10.4 | Escalation only when human judgment required | Y (doc) | Y | N | Y |
| 10.5 | Agent control-loop metrics / setpoints defined | Y | N | N | Y |
| 10.6 | Skills registry (filesystem, observability, browser, etc.) | Y | Y | N | Y |

---

## 11. Plans & Execution (p.7)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 11.1 | PLANS.md spec for execution plans | Y | N | N | Y |
| 11.2 | exec-plans/active/ and completed/ directories | Y | P | P | N |
| 11.3 | Plans are self-contained (novice can implement from plan alone) | Y | — | — | Y |
| 11.4 | Living plan sections (progress log, decision log, retrospective) | Y | — | — | Y |
| 11.5 | Product specs in-repo (not external tools) | Y | N | P | Y |

---

## 12. Agent-Generated Everything (p.12)

| # | Practice | EnHarnes | reins | example_proj | harness-skill |
|---|----------|----------|-------|--------------|---------------|
| 12.1 | Product code and tests | — | Y | — | — |
| 12.2 | CI configuration and release tooling | P | Y | N | Y |
| 12.3 | Internal developer tools (scripts, linters) | Y | Y | N | Y |
| 12.4 | Documentation and design history | Y | Y | P | Y |
| 12.5 | Scripts that manage the repository itself | Y | P | N | Y |
| 12.6 | Evaluation harnesses | P | N | N | Y |

---

## Score Summary

Counting Y=2, P=1, N=0 across all applicable items:

| Category | EnHarnes | reins | example_proj | harness-skill |
|----------|----------|-------|--------------|---------------|
| 1. Repo as System of Record | 18/20 | 15/20 | 13/20 | 12/20 |
| 2. AGENTS.md Design | 10/10 | 10/10 | 10/10 | — |
| 3. Layered Architecture | 13/14 | 3/14 | 7/14 | 12/14 |
| 4. Application Legibility | 7/12 | 0/12 | 1/12 | 9/12 |
| 5. Enforcing Taste | 15/16 | 11/16 | 7/16 | 16/16 |
| 6. Golden Principles | 10/10 | 8/10 | 5/10 | 10/10 |
| 7. Entropy/Garbage Collection | 7/12 | 2/12 | 0/12 | 9/12 |
| 8. CI & Merge | 12/12 | 10/12 | 0/12 | 10/12 |
| 9. Policy-as-Code | 8/8 | 7/8 | 4/8 | 2/8 |
| 10. Agent Autonomy | 7/12 | 6/12 | 0/12 | 10/12 |
| 11. Plans & Execution | 10/10 | 2/10 | 3/10 | 8/10 |
| 12. Agent-Generated Everything | 8/12 | 8/12 | 1/12 | 10/12 |
| **TOTAL** | **125/148** | **82/148** | **51/148** | **108/148** |
| **Percentage** | **84%** | **55%** | **34%** | **73%** |

---

## Top Gaps Remaining in EnHarnes

> Items resolved in this pass are struck through. Remaining items tracked in `docs/DEEP_RESEARCH.md`.

| Priority | Gap | Status |
|----------|-----|--------|
| **HIGH** | 4.1-4.4 Application legibility (worktree boot, observability, browser) | Open — needs runtime/stack decision. See DEEP_RESEARCH.md #1-3 |
| **HIGH** | 10.2-10.3 Agent-to-agent review + full autonomy loop | Open — needs design. See DEEP_RESEARCH.md #5-6 |
| **HIGH** | 7.4 Automated cleanup PRs | Open — needs design. See DEEP_RESEARCH.md #4 |
| ~~MED~~ | ~~8.2 CI completeness~~ | **Closed** — CI now runs check + structural + doc-drift |
| ~~MED~~ | ~~5.2 Linter error messages~~ | **Closed** — all linters now emit agent-readable remediation |
| **MED** | 12.6 Evaluation harnesses | Open — needs GitHub API integration. See DEEP_RESEARCH.md #7 |
| ~~LOW~~ | ~~7.3 Quality grades~~ | **Closed** — ARCHITECTURE.md now has quality grades |
| ~~LOW~~ | ~~9.3 Policy enforcement~~ | **Closed** — CI + self-review now read risk-policy.json |

---

## What EnHarnes Does Better Than Others

| Strength | Detail |
|----------|--------|
| Plans & Execution | Best PLANS.md spec of all repos. Self-contained exec plan format is production-ready |
| Structural tests | Only repo with working AST-based layer dependency tests |
| Entropy management | Only repo with ENTROPY.md + entropy-check.sh + tech-debt tracker |
| Custom linters | dependency_guard.py + custom_linter.py actually enforce golden principles |
| Observability scripts | obs-up.sh / obs-down.sh exist (other repos have nothing) |
| Control-loop metrics | Only repo with measurable setpoints (evals/control-loop-metrics.yaml) |

---

## What to Borrow from Other Repos

| From | What | Status |
|------|------|--------|
| ~~reins~~ | ~~CI workflows~~ | **Done** — adapted into .github/workflows/ci.yml |
| reins | Biome config (biome.json) | When TypeScript is chosen as runtime |
| ~~reins~~ | ~~ARCHITECTURE.md quality grades~~ | **Done** — added to ARCHITECTURE.md |
| reins | SKILL.md pattern | When agent skills are formalized |
| harness-skill | Audit script (harness_wizard.py audit) | Future — automated readiness scoring |
| harness-skill | Bootstrap script | Future — one-command repo scaffolding |
| ~~harness-skill~~ | ~~Nightly CI workflow for entropy~~ | **Done** — already had nightly-entropy.yml |
