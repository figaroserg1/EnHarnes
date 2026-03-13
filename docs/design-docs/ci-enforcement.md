# CI Enforcement and Risk Policy

<!-- Verified: 2026-02-24 -->

This document captures how EnHarnes enforces quality gates and doc-drift policy.
Agents read this to understand *why* the CI structure is the way it is — not just what commands to run.

## Decisions

**1. Policy-as-code is required.**
`risk-policy.json` at repo root defines:
- risk tiers (`low`, `medium`, `high`)
- `watchPaths` for change detection
- `docsDriftRules` mapping code areas to docs that must stay current

When code in a watched path changes, the agent checks `risk-policy.json` and verifies
that all listed docs still accurately reflect the code. This happens in `agent_self_review.py`.

**2. CI quality gates are explicit and composite.**
`.github/workflows/ci.yml` runs `make lint`.
`make lint` is a composite target that runs three gates:
1. `make lint-todos` — TODO ownership, unreplaced template markers
2. `make lint-src` — Python source guard (print detection, file size limits)
3. `make lint-structural` — AST-based layer dependency validation (Types → Config → Repo → Service → Runtime → UI)

All gates are blocking. No advisory-only CI steps.

**3. `make ci` equals `make lint` locally.**
`make ci` is an alias for `make lint`. Agents and CI use the same command surface.
No divergence between local runs and CI behavior.

**4. Nightly entropy check is separate from PR-triggered CI.**
`.github/workflows/nightly-entropy.yml` runs daily at 03:00 UTC via cron.
It checks for: stale doc placeholders, orphaned scripts, blank setpoints, oversized files,
broken doc references in `risk-policy.json`.
Failures go to the maintainer for triage — they are not PR merge blockers.

**5. Unresolved review threads block merge.**
When branch protection enforces conversation resolution, unresolved review comments
block merge even when CI is green. This is the only non-automated merge gate.

**6. Harness scripts provide portable entry points.**
`.claude/skills/harness.ci/scripts/lint_runner.py` and `.claude/skills/harness.ci/scripts/typecheck.py` auto-detect the project
runtime (Rust/Node/Python) and run the appropriate toolchain. For EnHarnes (Python),
they delegate to `todo_linter.py` and `code_conventions.py`.

## Rationale

- One CI command (`make lint`) makes local reproduction trivial: copy the CI command, run it, done.
- Separating nightly entropy from PR CI avoids noise on every commit.
- Machine-readable drift policy (`risk-policy.json`) means agents can audit their own impact
  without prompting — they know which docs to check before opening a PR.
- The `lint-todos → lint-src → lint-structural` sequence catches three distinct failure classes in order:
  doc hygiene → code conventions → architecture violations.

## Merge Philosophy

**Short-lived PRs.** PRs should be small, focused, and merged quickly. Large PRs increase
review burden and merge conflict risk. Prefer multiple small PRs over one large one.

**Minimal blocking gates.** Only block merge on things that can be verified mechanically
(lint, structural tests, doc-drift). Human review focuses on intent and architecture fit,
not style or formatting (those are enforced by linters).

**Flakes get follow-up, not retries.** If CI fails due to a flake, fix the flake in a
follow-up PR. Do not retry CI hoping it passes — that hides real issues.

**Conversation resolution is a merge gate.** Unresolved review threads block merge even
when CI is green. This ensures every comment is addressed, not ignored.

## Consequences

- Any violation of Golden Principles (print statements, oversized files) in `src/` blocks merge at `make lint-src`.
- Layer boundary violations block merge at `make lint-structural`.
- Doc references in `risk-policy.json` that no longer resolve are caught by the nightly entropy scan, not PR CI.
- Adding a new script to `scripts/` without a Makefile target will be flagged by `make check-entropy`.
