#!/usr/bin/env python3
"""Evaluation harness: measures control-loop metrics against setpoints.

Reads targets from evals/control-loop-metrics.yaml, measures actuals
via GitHub API (using `gh` CLI), and reports pass/fail per metric.

Usage:
    python scripts/measure_metrics.py --owner OWNER --repo REPO [--days 30]

Requires: gh CLI authenticated (gh auth login).

Metrics:
    1. pr_pass_at_1              - % of PRs where CI passes on first commit
    2. merge_cycle_time_hours    - median hours from PR open to merge
    3. revert_rate               - % of merged PRs later reverted
    4. human_intervention_rate   - % of PRs with human (non-bot) comments
    5. time_to_actionable_failure_minutes - median minutes from push to CI failure
"""

import argparse
import json
import re
import statistics
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

KNOWN_BOTS = {
    "dependabot[bot]", "github-actions[bot]", "renovate[bot]",
    "codecov[bot]", "copilot-swe-agent[bot]", "netlify[bot]",
    "vercel[bot]", "sonarcloud[bot]", "coderabbitai[bot]",
}


def gh_api(path: str, params: dict | None = None) -> list | dict:
    """Call GitHub REST API via `gh` CLI."""
    cmd = ["gh", "api", path, "--header", "Accept: application/vnd.github+json"]
    for k, v in (params or {}).items():
        cmd.extend(["-f", f"{k}={v}"])
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[ERROR] gh api {path} failed: {result.stderr.strip()}", file=sys.stderr)
        return []
    return json.loads(result.stdout)


def parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def is_bot(user: dict) -> bool:
    return (
        user.get("type") == "Bot"
        or user.get("login", "").endswith("[bot]")
        or user.get("login", "") in KNOWN_BOTS
    )


def load_setpoints() -> dict:
    """Load targets from policies/control-loop-metrics.yaml."""
    yaml_path = ROOT / "policies" / "control-loop-metrics.yaml"
    if not yaml_path.exists():
        return {}
    # Simple YAML parsing (no PyYAML dependency)
    setpoints = {}
    current_metric = None
    for line in yaml_path.read_text().splitlines():
        stripped = line.strip()
        if stripped.startswith("- name:"):
            current_metric = stripped.split(":", 1)[1].strip()
        elif stripped.startswith("target:") and current_metric:
            val = stripped.split(":", 1)[1].strip()
            try:
                setpoints[current_metric] = {"target": float(val)}
            except ValueError:
                pass
        elif stripped.startswith("alert_below:") and current_metric:
            val = stripped.split(":", 1)[1].strip()
            try:
                setpoints.setdefault(current_metric, {})["alert_below"] = float(val)
            except ValueError:
                pass
        elif stripped.startswith("alert_above:") and current_metric:
            val = stripped.split(":", 1)[1].strip()
            try:
                setpoints.setdefault(current_metric, {})["alert_above"] = float(val)
            except ValueError:
                pass
    return setpoints


# --- Metric computation ---

def compute_pr_pass_at_1(owner: str, repo: str, prs: list) -> float:
    passing = {"success", "skipped", "neutral"}
    passed = evaluated = 0
    for pr in prs:
        commits = gh_api(f"/repos/{owner}/{repo}/pulls/{pr['number']}/commits")
        if not commits:
            continue
        first_sha = commits[0]["sha"]
        checks = gh_api(f"/repos/{owner}/{repo}/commits/{first_sha}/check-runs")
        runs = checks.get("check_runs", []) if isinstance(checks, dict) else []
        if not runs:
            continue
        evaluated += 1
        if all(r.get("conclusion") in passing for r in runs):
            passed += 1
    return passed / evaluated if evaluated else 0.0


def compute_merge_cycle_times(prs: list) -> list[float]:
    times = []
    for pr in prs:
        if pr.get("merged_at"):
            created = parse_iso(pr["created_at"])
            merged = parse_iso(pr["merged_at"])
            times.append((merged - created).total_seconds() / 3600)
    return times


REVERT_TITLE_RE = re.compile(r'^Revert\s+"', re.IGNORECASE)
REVERT_BODY_RE = re.compile(r"Reverts\s+[\w.-]+/[\w.-]+#(\d+)")


def compute_revert_rate(prs: list) -> float:
    merged_numbers = {pr["number"] for pr in prs if pr.get("merged_at")}
    reverted = set()
    for pr in prs:
        if not pr.get("merged_at"):
            continue
        title = pr.get("title", "")
        body = pr.get("body", "") or ""
        if REVERT_TITLE_RE.match(title):
            m = REVERT_BODY_RE.search(body)
            if m:
                orig = int(m.group(1))
                if orig in merged_numbers:
                    reverted.add(orig)
    return len(reverted) / len(merged_numbers) if merged_numbers else 0.0


def compute_human_intervention_rate(owner: str, repo: str, prs: list) -> float:
    human_touched = 0
    for pr in prs:
        num = pr["number"]
        pr_author = pr.get("user", {}).get("login", "")
        comments = gh_api(f"/repos/{owner}/{repo}/issues/{num}/comments")
        reviews = gh_api(f"/repos/{owner}/{repo}/pulls/{num}/reviews")
        has_human = False
        for c in (comments if isinstance(comments, list) else []):
            if not is_bot(c.get("user", {})) and c.get("user", {}).get("login") != pr_author:
                has_human = True
                break
        if not has_human:
            for r in (reviews if isinstance(reviews, list) else []):
                if not is_bot(r.get("user", {})) and r.get("user", {}).get("login") != pr_author:
                    has_human = True
                    break
        if has_human:
            human_touched += 1
    return human_touched / len(prs) if prs else 0.0


def compute_time_to_failure(owner: str, repo: str, prs: list) -> list[float]:
    times = []
    for pr in prs:
        commits = gh_api(f"/repos/{owner}/{repo}/pulls/{pr['number']}/commits")
        for commit in (commits if isinstance(commits, list) else []):
            sha = commit["sha"]
            runs_resp = gh_api(
                f"/repos/{owner}/{repo}/actions/runs",
                params={"head_sha": sha},
            )
            wf_runs = runs_resp.get("workflow_runs", []) if isinstance(runs_resp, dict) else []
            failures = [r for r in wf_runs if r.get("conclusion") == "failure"]
            if failures:
                failures.sort(key=lambda r: r.get("updated_at", ""))
                first = failures[0]
                push_t = parse_iso(first["created_at"])
                fail_t = parse_iso(first["updated_at"])
                times.append((fail_t - push_t).total_seconds() / 60)
                break
    return times


# --- Main ---

def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--days", type=int, default=30)
    args = parser.parse_args()

    since = (datetime.now(timezone.utc) - timedelta(days=args.days)).isoformat()
    setpoints = load_setpoints()

    # Fetch merged PRs
    page = 1
    all_prs: list[dict] = []
    while True:
        batch = gh_api(
            f"/repos/{args.owner}/{args.repo}/pulls",
            params={"state": "closed", "sort": "updated", "direction": "desc",
                    "per_page": "100", "page": str(page)},
        )
        if not isinstance(batch, list) or not batch:
            break
        for pr in batch:
            if pr.get("merged_at") and pr["merged_at"] >= since:
                all_prs.append(pr)
            if pr.get("updated_at", "") < since:
                batch = []
                break
        if not batch or len(batch) < 100:
            break
        page += 1

    print(f"Found {len(all_prs)} merged PRs in the last {args.days} days\n")

    if not all_prs:
        print("No PRs to measure. Exiting.")
        return

    # Compute metrics
    results = {}

    pass1 = compute_pr_pass_at_1(args.owner, args.repo, all_prs)
    results["pr_pass_at_1"] = round(pass1, 4)
    print(f"pr_pass_at_1:                     {pass1:.1%}")

    cycle_times = compute_merge_cycle_times(all_prs)
    median_cycle = statistics.median(cycle_times) if cycle_times else 0
    results["merge_cycle_time_hours"] = round(median_cycle, 2)
    print(f"merge_cycle_time_hours (median):  {median_cycle:.1f}h")

    rr = compute_revert_rate(all_prs)
    results["revert_rate"] = round(rr, 4)
    print(f"revert_rate:                      {rr:.1%}")

    hir = compute_human_intervention_rate(args.owner, args.repo, all_prs)
    results["human_intervention_rate"] = round(hir, 4)
    print(f"human_intervention_rate:          {hir:.1%}")

    ttf = compute_time_to_failure(args.owner, args.repo, all_prs)
    median_ttf = statistics.median(ttf) if ttf else 0
    results["time_to_actionable_failure_minutes"] = round(median_ttf, 2)
    print(f"time_to_failure_minutes (median): {median_ttf:.1f}m")

    # Compare against setpoints
    print("\n--- Setpoint Comparison ---")
    alerts = []
    for name, actual in results.items():
        sp = setpoints.get(name, {})
        target = sp.get("target")
        alert_below = sp.get("alert_below")
        alert_above = sp.get("alert_above")
        status = "OK"
        if alert_below is not None and actual < alert_below:
            status = "ALERT (below threshold)"
            alerts.append(name)
        elif alert_above is not None and actual > alert_above:
            status = "ALERT (above threshold)"
            alerts.append(name)
        target_str = f" (target: {target})" if target is not None else ""
        print(f"  {name}: {actual}{target_str} — {status}")

    # Machine-readable output
    output = {**results, "sample_size": len(all_prs), "window_days": args.days, "alerts": alerts}
    print(f"\n{json.dumps(output, indent=2)}")

    if alerts:
        sys.exit(1)


if __name__ == "__main__":
    main()
