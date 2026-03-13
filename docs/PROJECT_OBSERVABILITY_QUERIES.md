# Observability Queries

## Phase 1: Python obs.py queries

```python
import obs

# Recent errors (last 5 minutes)
obs.query_logs(level="error", since_minutes=5)

# Logs containing a keyword
obs.query_logs(contains="timeout", since_minutes=30)

# All info logs from last hour
obs.query_logs(level="info", since_minutes=60, limit=100)

# Latest metric values
obs.query_metrics(name="startup_time_ms", since_minutes=60)

# Health summary (log counts + latest metrics)
obs.summary(since_minutes=30)
```

## Phase 1: CLI one-liners

```bash
# Recent errors as JSON
python3 -c "import scripts.obs as obs; import json; print(json.dumps(obs.query_logs(level='error'), indent=2))"

# Health summary
python3 scripts/obs.py

# Raw log files (human debugging)
cat .claude/observability/logs/log-$(date +%Y-%m-%d).jsonl | python3 -m json.tool
```

## Phase 2+: LogQL queries (when Loki is added)

```text
# All error logs
{level="error"}

# Errors from a specific component
{component="api"} |= "timeout"

# Rate of errors per minute
rate({level="error"}[1m])
```

## Phase 2+: PromQL queries (when Prometheus is added)

```text
# Request duration p95
histogram_quantile(0.95, http_request_duration_seconds_bucket)

# Error rate
rate(http_requests_total{status=~"5.."}[5m])
```
