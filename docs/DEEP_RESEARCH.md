# Deep Research Backlog

Items from the harness engineering checklist that required investigation.
Status: RESOLVED items have been implemented. OPEN items need human decisions.

---

## 1. Application Legibility — Worktree Boot (Checklist 4.1) -- RESOLVED

**Implemented:** `scripts/worktree-boot.sh`
- Creates worktree, auto-detects runtime, installs deps, runs smoke check.
- Naming: `../worktree_<task-name>` on branch `task/<task-name>`.
- See `docs/WORKTREE_WORKFLOW.md` for full docs.

**Still OPEN:** TODO: [HUMAN] Decide target runtime/stack for Phase 2.

---

## 2. Application Legibility — Local Observability Stack (Checklist 4.2-4.3) -- RESOLVED

**Decision:** Phase 1 uses zero-infrastructure Python module (`scripts/obs.py`).

**Rationale:** No product code exists yet. Running 1-4 containers to observe nothing is
pure overhead. The upgrade path is clean:
- Phase 1: `obs.py` with JSONL files (0ms startup, 0 containers)
- Phase 2: Add Vector as single container, `obs.py` write API unchanged
- Phase 3: Add Loki + Grafana for dashboards

**Implemented:**
- `scripts/obs.py` — log/metric write + query API
- `docs/OBSERVABILITY.md` — updated with phased approach
- `docs/observability/queries.md` — example queries for each phase

---

## 3. Application Legibility — Browser Automation (Checklist 4.4) -- RESOLVED

**Research findings:** Four viable options identified:

| Tool | Type | Best for |
|------|------|----------|
| `@playwright/mcp` | MCP server | Primary browser automation (recommended) |
| `agent-browser` | CLI tool | Codex/background tasks needing shell-based browser control |
| `chrome-devtools-mcp` | MCP server | Performance profiling + CrUX data |
| `@browserbasehq/mcp` | MCP server (cloud) | Cloud browsers (paid, for production) |

**Decision:** Use `@playwright/mcp` as primary when UI exists.
Config: `claude mcp add playwright -- npx @playwright/mcp --headless --caps vision`

**Implemented:** `docs/BROWSER_AUTOMATION.md` — full setup guide for all options.

**Still OPEN:** TODO: [HUMAN] Decide if product has a UI (determines when to activate).

---

## 4. Automated Cleanup PRs (Checklist 7.4) -- RESOLVED

**Implemented:** `.github/workflows/weekly-cleanup.yml`
- Runs every Monday at 06:00 UTC (and on manual dispatch).
- Runs `make entropy`, captures output.
- Auto-fixes TODOs without owner markers.
- Creates PR with entropy report if fixes were made.
- Labels: `entropy`, `automated`.

**Limitations:** Only auto-fixes simple issues (TODO ownership). Complex entropy
(stale docs, dead scripts) still requires human triage from the entropy report.

---

## 5. Agent-to-Agent Review Loop (Checklist 10.2) -- OPEN

**Research:** The OpenAI article mentions agent-to-agent review but provides no
implementation details. Key design questions remain:

**Protocol options:**
- A) GitHub PR comments (reviewer agent posts structured JSON feedback)
- B) Local JSON file exchange (author writes, reviewer reads, outputs verdict)
- C) CodeRabbit / AI review tool as the "reviewer agent"

**Recommended approach for Phase 2:**
1. Author agent opens PR and runs `make review`.
2. CodeRabbit (already configured via `.coderabbit.yaml`) acts as first reviewer.
3. If CodeRabbit flags issues, author agent reads comments and fixes.
4. Human reviews only for architectural decisions.

This gives agent-to-agent review without building custom infrastructure.

**TODO: [AI] Implement a `scripts/parse-review-comments.py` that reads PR comments
from CodeRabbit and outputs structured fix suggestions.**

---

## 6. Full Agent Autonomy Loop (Checklist 10.3) -- OPEN

**Depends on:** Having actual product code and test infrastructure.

**Design for Phase 2:**
1. Agent reads GitHub issue → writes repro test → runs test (should fail).
2. Agent implements fix → runs test (should pass) → runs `make test`.
3. Agent runs `make review` (self-review) → opens PR.
4. CodeRabbit reviews → agent fixes comments → merge.

**TODO: [HUMAN] Decide target autonomy level for Phase 2 (Level 1 prompted vs Level 2 review loop).**

---

## 7. Evaluation Harness for Control-Loop Metrics (Checklist 12.6) -- RESOLVED

**Implemented:** `scripts/measure_metrics.py`

Uses `gh` CLI (GitHub API) to measure all 5 control-loop metrics:
1. `pr_pass_at_1` — first-commit CI pass rate (check-runs per first SHA)
2. `merge_cycle_time_hours` — PR created_at to merged_at
3. `revert_rate` — title/body pattern matching for revert PRs
4. `human_intervention_rate` — non-bot comments/reviews on PRs
5. `time_to_actionable_failure_minutes` — workflow run created→completed

Compares actuals against setpoints in `evals/control-loop-metrics.yaml`.
Exits non-zero if any metric crosses alert threshold.

**Usage:**
```bash
python scripts/measure_metrics.py --owner figaroserg1 --repo EnHarnes --days 30
```

**Rate limits:** ~300-500 GitHub API calls per 100 PRs. Stay within 5000/hour limit.

---

## 8. Planned Structural Tests Not Yet Implemented -- OPEN

Still blocked: no `src/` code exists yet. These tests would scan empty directories.

| Test | Principle | Status |
|------|-----------|--------|
| `test_duplicate_helpers.py` | 8. Shared utilities | Blocked — needs src/ code |
| `test_side_effect_patterns.py` | 9. Idempotent side-effects | Blocked — needs src/ code |
| `test_contract_changes.py` | 11. Contract versioning | Blocked — needs src/ code |
| AST dynamic key access scan | 7. No data probing | Blocked — needs src/ code |
| Trace context check | 10. Trace propagation | Blocked — needs src/ code |

**TODO: [AI] Implement these tests when first product code is added to src/.**
