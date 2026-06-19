---
name: harness-feedback
description: Format for logging in-flight observations about the harness (skills, hooks, agents, dev policies, methodology docs) to docs/harness-feedback.md. Triggered by the AGENTS.md Self-Improvement step-exit scan. Skip silently if nothing surfaces — quality over quantity.
---

# harness-feedback

Channel for the executor agent to flag issues with the **harness itself**
while doing real work. Output goes to `docs/harness-feedback.md`. Triage is
operator-driven; this skill defines only the format and the calibration.

## When to write

Add a feedback entry when, during a task or session, you noticed a concrete
piece of friction in the **harness**:

- a skill instruction that is unclear, contradictory, or stale,
- a hook that blocked a legitimate operation,
- two policies / docs / templates overlapping on the same concern,
- a methodology step that wasted time without payoff,
- an ambiguity between what the doc said and what the code or repo actually
  does.

## When NOT to write

- Bugs in the product — open a real fix or an ExecPlan.
- Drift / orphan-script findings from `make check-entropy` — those belong in the
  tech-debt tracker (separate concern).
- Generic preferences ("I'd like the docs in another language", "rewrite in Rust").
- Task-specific failures — those go to the Failure Ledger (see `AGENTS.md`).

## Categories (closed list, pick one)

| Category | Meaning |
|---|---|
| `improvement` | A skill/doc/hook works but could be smaller, clearer, faster, or better-named |
| `problem` | A skill/doc/hook is broken, contradicts current code, or misleads |
| `ambiguity` | Two valid interpretations of the same instruction; you had to guess |
| `duplication` | Same concern covered in two places; risk of drift |
| `impediment` | The harness actively blocked or slowed legitimate work |

## Target (namespace prefix, concrete path)

| Prefix | Example |
|---|---|
| `skill:` | `skill:harness.linters/SKILL.md` |
| `hook:` | `hook:validate-bash.py` |
| `agent:` | `agent:reviewer` (under `.claude/agents/harness/`) |
| `policy:` | `policy:risk-policy.json` |
| `doc:` | `doc:AGENTS.md`, `doc:CLAUDE.md`, `doc:harness.core/docs/ENTROPY_PRINCIPLES.md` |
| `template:` | `template:harness.plan/OPENAI_PLANS.md` |
| `convention:` | `convention:exec-plan-naming` (when the issue is unwritten convention, not a single file) |

Use one target per entry. If the issue spans multiple files, write multiple
entries — each with its own concrete target.

## Entry template

Append to `docs/harness-feedback.md`:

```markdown
## YYYY-MM-DD — <one-line summary, ≤80 chars>

- **Category:** <one of: improvement | problem | ambiguity | duplication | impediment>
- **Target:** <prefix:path>
- **Phase:** <one of: step | pr | session | interactive>
- **Context:** <ExecPlan name, or short note like "session 2026-03-14 docs refactor">
- **Observation:** <1–3 sentences of what you noticed>
- **Suggested fix:** <optional, 1 line, concrete change the operator could make>

---
```

Newest entries at the bottom (append-only, mirrors the Failure Ledger).

## Calibration

- **Cap: ≤3 entries per task / session.** If you have more candidates, pick the
  3 with the most concrete `Target` and clearest `Observation`. Better one
  high-quality entry than five vague ones.
- **Concrete `Target` required.** "The harness is hard to use" without a file
  path is noise.
- **Observation describes friction**, not the suggested fix. The fix is
  optional and lives in its own field.
- **Skip silently** when no friction surfaced this turn. Empty is a valid
  outcome.

## Good vs bad

**Good:**

```markdown
## 2026-03-14 — harness.plan filename convention is ambiguous

- **Category:** ambiguity
- **Target:** skill:harness.plan/SKILL.md
- **Phase:** interactive
- **Context:** session 2026-03-14, tidying exec-plans hygiene
- **Observation:** SKILL.md line 14 says new ExecPlans go to
  `docs/exec-plans/active/YYYY-MM-DD-<slug>.md`, but several existing plans in
  `docs/exec-plans/done/` use a different stem. New contributors get
  conflicting guidance.
- **Suggested fix:** document the single canonical stem, or state the criteria
  for choosing between them.
```

**Bad (vague target, no observation):**

```markdown
## 2026-03-14 — Things are confusing

- **Category:** improvement
- **Target:** doc:everything
- **Phase:** interactive
- **Context:** today
- **Observation:** The whole harness is confusing.
```

**Bad (out of scope — product bug, not harness):**

```markdown
## 2026-03-14 — service crashes on missing config

- **Category:** problem
- **Target:** code:src/Service/service.py
- ...
```

This is a product bug — fix it or open an ExecPlan. Not for this journal.

## Lifecycle

1. Executor (model or interactive agent session) appends an entry per the
   trigger in `AGENTS.md` (Self-Improvement step-exit scan).
2. Operator reviews `docs/harness-feedback.md` periodically.
3. Each entry is flipped to either:
   - `<-- TRIAGED: ExecPlan created>` (a real plan opens for the fix), or
   - `<-- TRIAGED: noise, ignored>` (false positive or out of scope).
4. Entries stay in the file as historical record — they are not deleted.

No automation enforces this lifecycle; it is a social/operator process.

## Trigger reference

- **Per-step / step-exit scan** (every meaningful unit of work — a completed
  milestone, before a commit, before a PR): see the Self-Improvement step-exit
  scan in `AGENTS.md`. This applies equally to interactive CLI sessions.

This skill itself does not auto-trigger — read it from that entry point when
you are composing an entry.
