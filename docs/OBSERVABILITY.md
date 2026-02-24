# OBSERVABILITY

Goal: make the system agent-verifiable without human intervention.

## Phase 1: Minimal Python (Zero Infrastructure)

Observability is provided by `scripts/obs.py` — a structured JSON log/metric module
with zero containers, zero ports, instant startup.

```python
import obs
obs.log("info", "task started", component="ci", task_id="abc123")
obs.metric("startup_time_ms", 1230, component="api")

# Query
errors = obs.query_logs(level="error", since_minutes=5)
health = obs.summary()
```

Data stored in `.claude/observability/logs/` and `.claude/observability/metrics/` as JSONL.

## Phase 2: Vector (When First Service Arrives)

Add Vector as a single container to collect from multiple sources.
`obs.py` write API stays the same — add a Vector HTTP sink internally.

## Phase 3: Full Stack (Multiple Services)

Add Loki + Grafana. Vector forwards to Loki. Humans get dashboards,
agent still uses `obs.py` query functions or switches to LogQL.

## Agent Capabilities

Agent must be able to:
- Write structured logs via `obs.log()`
- Write metrics via `obs.metric()`
- Query logs by level, content, time window via `obs.query_logs()`
- Get health summary via `obs.summary()`
- Run local observability stack via `./scripts/obs-up.sh` / `./scripts/obs-down.sh` (Phase 2+)

## Acceptance Checks

- Startup: instant (0ms — Python import only)
- No error logs during smoke test
- `obs.summary()` returns valid JSON with level counts and latest metrics

## Observability Queries

See `docs/observability/queries.md` for example queries.
