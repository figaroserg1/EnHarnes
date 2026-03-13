#!/usr/bin/env python3
"""Minimal observability for agent-first dev workflow.

Zero infrastructure. Structured JSON to files. Query with functions.
Phase 1 approach: no containers, no ports, instant startup.

Upgrade path:
  Phase 2 → add Vector sink inside log()/metric() without changing callers.
  Phase 3 → add Loki + Grafana, Vector forwards to Loki.

Usage:
    import obs
    obs.log("info", "task started", component="ci", task_id="abc123")
    obs.metric("startup_time_ms", 1230, component="api")

    errors = obs.query_logs(level="error", since_minutes=5)
    print(obs.summary())
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

OBS_DIR = Path(os.environ.get("OBS_DIR", ".claude/observability"))
LOG_DIR = OBS_DIR / "logs"
METRIC_DIR = OBS_DIR / "metrics"

LOG_DIR.mkdir(parents=True, exist_ok=True)
METRIC_DIR.mkdir(parents=True, exist_ok=True)


def _today_file(subdir: Path, prefix: str) -> Path:
    return subdir / f"{prefix}-{datetime.utcnow().strftime('%Y-%m-%d')}.jsonl"


# ---- Write API ----

def log(level: str, msg: str, **kwargs):
    """Append a structured log entry."""
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "level": level,
        "msg": msg,
        **kwargs,
    }
    with open(_today_file(LOG_DIR, "log"), "a") as f:
        f.write(json.dumps(entry) + "\n")


def metric(name: str, value: float, **tags):
    """Append a metric data point."""
    entry = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "metric": name,
        "value": value,
        **tags,
    }
    with open(_today_file(METRIC_DIR, "metric"), "a") as f:
        f.write(json.dumps(entry) + "\n")


# ---- Query API ----

def query_logs(
    level: Optional[str] = None,
    contains: Optional[str] = None,
    since_minutes: int = 60,
    limit: int = 50,
) -> list[dict]:
    """Query recent logs. Returns list of matching entries."""
    cutoff = datetime.utcnow() - timedelta(minutes=since_minutes)
    results: list[dict] = []
    for f in sorted(LOG_DIR.glob("log-*.jsonl"), reverse=True):
        for line in reversed(f.read_text().strip().split("\n")):
            if not line:
                continue
            entry = json.loads(line)
            entry_time = datetime.fromisoformat(entry["ts"].rstrip("Z"))
            if entry_time < cutoff:
                break
            if level and entry.get("level") != level:
                continue
            if contains and contains.lower() not in json.dumps(entry).lower():
                continue
            results.append(entry)
            if len(results) >= limit:
                return results
    return results


def query_metrics(
    name: Optional[str] = None,
    since_minutes: int = 60,
) -> list[dict]:
    """Query recent metrics. Returns list of matching data points."""
    cutoff = datetime.utcnow() - timedelta(minutes=since_minutes)
    results: list[dict] = []
    for f in sorted(METRIC_DIR.glob("metric-*.jsonl"), reverse=True):
        for line in reversed(f.read_text().strip().split("\n")):
            if not line:
                continue
            entry = json.loads(line)
            entry_time = datetime.fromisoformat(entry["ts"].rstrip("Z"))
            if entry_time < cutoff:
                break
            if name and entry.get("metric") != name:
                continue
            results.append(entry)
    return results


def summary(since_minutes: int = 60) -> dict:
    """Quick health summary for agent introspection."""
    logs = query_logs(since_minutes=since_minutes, limit=10000)
    metrics = query_metrics(since_minutes=since_minutes)
    level_counts: dict[str, int] = {}
    for entry in logs:
        lvl = entry.get("level", "unknown")
        level_counts[lvl] = level_counts.get(lvl, 0) + 1

    metric_latest: dict[str, float] = {}
    for entry in metrics:
        mname = entry.get("metric")
        if mname and mname not in metric_latest:
            metric_latest[mname] = entry["value"]

    return {
        "log_counts_by_level": level_counts,
        "total_log_entries": len(logs),
        "latest_metrics": metric_latest,
        "window_minutes": since_minutes,
    }


if __name__ == "__main__":
    print(json.dumps(summary(), indent=2))
