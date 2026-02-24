# Deep Research Backlog

Items from the harness engineering checklist that cannot be resolved with reference repos alone.
Each requires investigation, prototyping, or a human decision before implementation.

---

## 1. Application Legibility — Worktree Boot (Checklist 4.1)

**What the article says:** Every agent session boots a fresh worktree. The app must start
from zero in an isolated copy of the repo with no shared state.

**What's needed:**
- Define what "boot" means for EnHarnes (install deps → start services → run smoke).
- Create a `scripts/worktree-boot.sh` that handles the full sequence.
- Test that `git worktree add` + boot script works end-to-end.

**Depends on:** runtime/stack decision (TODO: [HUMAN]).

---

## 2. Application Legibility — Local Observability Stack (Checklist 4.2-4.3)

**What the article says:** Agents must be able to query logs (LogQL), metrics (PromQL),
and traces locally. The observability stack runs via `obs-up.sh` / `obs-down.sh`.

**What's needed:**
- Choose observability stack (Grafana+Loki+Tempo vs. simpler alternatives).
- Implement actual `docker-compose.yml` or equivalent in `scripts/obs-up.sh`.
- Add sample LogQL/PromQL queries to `docs/observability/queries.md`.
- Define acceptance criteria: startup < 800ms, no error logs in smoke.

**Research:** Compare lightweight options (OpenTelemetry collector + file export vs. full Grafana stack).
For Phase 1 without product code, a stub stack that accepts and stores structured logs may suffice.

---

## 3. Application Legibility — Browser Automation (Checklist 4.4)

**What the article says:** Agents use Chrome DevTools Protocol for UI validation —
screenshot comparison, element inspection, interaction replay.

**What's needed:**
- Evaluate if browser automation applies to EnHarnes (depends on whether there's a UI).
- If yes: choose framework (Playwright vs Puppeteer), add to skills registry.
- If no UI planned: mark as N/A and document why.

**Depends on:** product domain decision (TODO: [HUMAN]).

---

## 4. Automated Cleanup PRs (Checklist 7.4)

**What the article says:** Background Codex tasks scan for entropy and auto-generate
refactoring PRs. These run on a schedule, not triggered by humans.

**What's needed:**
- Design a GitHub Action or scheduled workflow that:
  1. Runs entropy check.
  2. For each fixable issue, creates a branch and PR.
- Define which entropy issues are auto-fixable vs. need human triage.
- Consider using OpenAI Codex API or Claude API for generating fixes.

**Research:** Look at how `reins` evolve --apply works. Could adapt that pattern
for scheduled auto-remediation PRs.

---

## 5. Agent-to-Agent Review Loop (Checklist 10.2)

**What the article says:** One agent writes code, another reviews. They iterate until
both the author-agent and reviewer-agent are satisfied. Human steps in only for
architectural decisions.

**What's needed:**
- Design the review protocol (structured JSON feedback? GitHub PR comments?).
- Define what the reviewer-agent checks (golden principles, layer violations, test coverage).
- Implement the iteration loop (how many rounds? what's the exit condition?).
- Decide if this runs in CI or as a separate tool.

**Research:** Study how OpenAI's internal agent-to-agent review works.
The article mentions this but doesn't give implementation details.

---

## 6. Full Agent Autonomy Loop (Checklist 10.3)

**What the article says:** Agent can: validate current state → reproduce bug →
implement fix → validate fix → open PR. Full cycle without human intervention
for Level 2+ autonomy.

**What's needed:**
- Define the state validation step (what does "current state" mean? CI green? specific tests?).
- Implement bug reproduction tooling (agent reads issue, writes repro test).
- Wire the full cycle: repro → fix → test → self-review → PR.

**Depends on:** having actual product code and test infrastructure.

---

## 7. Evaluation Harness for Control-Loop Metrics (Checklist 12.6)

**What the article says:** Setpoints are measured, not aspirational. When metrics
cross thresholds, it triggers a system response.

**What's needed:**
- `evals/control-loop-metrics.yaml` exists with targets, but nothing measures actuals.
- Build a script that reads GitHub API (PR pass rates, merge times, revert rates).
- Output comparison: actual vs. target, flag alerts.
- Optionally: post results to a dashboard or issue.

**Research:** GitHub API endpoints for:
- PR CI pass rate on first run
- Time from PR open to merge
- Revert rate (PRs that were later reverted)

---

## 8. Planned Structural Tests Not Yet Implemented

These are referenced in GOLDEN_PRINCIPLES.md enforcement summary as **(planned)**:

| Test | Principle | Complexity |
|------|-----------|------------|
| `test_duplicate_helpers.py` | 8. Shared utilities | Medium — needs similarity/clone detection |
| `test_side_effect_patterns.py` | 9. Idempotent side-effects | Medium — AST scan for external client calls |
| `test_contract_changes.py` | 11. Contract versioning | High — needs diff-based API/schema comparison |
| AST dynamic key access scan | 7. No data probing | Medium — detect `obj["key"]` outside schemas |
| Trace context check | 10. Trace propagation | Low — grep for trace_id in async handlers |

**Priority:** Implement when `src/` has actual product code. Currently no src/ files exist,
so these tests would have nothing to scan.
