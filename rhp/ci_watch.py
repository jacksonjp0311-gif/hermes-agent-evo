# RHP-013.5 CI Watch Loop automation.
from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any

CI_WATCH_SCHEMA = "RHP-CI-WATCH-PACKET-v0.1"
TERMINAL_GREEN = {"success", "skipped", "neutral"}
TERMINAL_RED = {"failure", "timed_out", "cancelled", "action_required"}
NONTERMINAL = {"queued", "in_progress", "requested", "waiting", "pending"}

@dataclass(frozen=True)
class CIWatchPacket:
    ok: bool
    schema: str
    commit_sha: str
    classification: str
    run_count: int
    selected_run: dict[str, Any] | None
    jobs: list[dict[str, Any]] = field(default_factory=list)
    failure_summary: list[str] = field(default_factory=list)
    source: str = "github_actions"
    degraded: bool = False
    degraded_reason: str = ""
    non_claim_lock: str = (
        "RHP-013.5 CI Watch observes GitHub Actions status and classifies the result. "
        "It does not mutate repository state, rerun jobs, call providers/models/tools, "
        "write CMS or memory, write APIs beyond optional public GitHub read requests, "
        "perform external ingestion, grant autonomy, or self-authorize."
    )

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def _headers() -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "hermes-rhp-ci-watch"}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def _get_json(url: str, *, timeout: int = 15) -> dict[str, Any]:
    req = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read().decode("utf-8", errors="replace")
    obj = json.loads(data)
    if not isinstance(obj, dict):
        raise ValueError("GitHub API returned non-object JSON")
    return obj

def classify_runs(runs: list[dict[str, Any]], jobs: list[dict[str, Any]] | None = None) -> tuple[str, bool, bool, str, list[str]]:
    jobs = jobs or []
    if not runs:
        return "unknown", False, True, "no workflow runs found for commit", []
    latest = runs[0]
    status = str(latest.get("status") or "").lower()
    conclusion = str(latest.get("conclusion") or "").lower()
    failures = []
    for job in jobs:
        jc = str(job.get("conclusion") or "").lower()
        js = str(job.get("status") or "").lower()
        if jc in TERMINAL_RED or js in TERMINAL_RED:
            failures.append(f"{job.get('name', 'unknown job')}: status={js or 'unknown'} conclusion={jc or 'unknown'}")
    if status in NONTERMINAL or not conclusion:
        return "pending", False, True, "workflow run is not complete", failures
    if conclusion in TERMINAL_GREEN and not failures:
        return "green", True, False, "", failures
    if conclusion in TERMINAL_RED or failures:
        return "red-actionable", False, True, "one or more workflow jobs failed", failures
    return "unknown", False, True, f"unrecognized workflow state status={status} conclusion={conclusion}", failures

def watch_commit(owner: str, repo: str, commit_sha: str, *, workflow: str = "Tests") -> CIWatchPacket:
    runs_url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs?head_sha={commit_sha}&per_page=20"
    try:
        runs_obj = _get_json(runs_url)
        runs = runs_obj.get("workflow_runs") or []
        if not isinstance(runs, list):
            runs = []
        if workflow:
            filtered = [r for r in runs if str(r.get("name") or "") == workflow]
            if filtered:
                runs = filtered
        jobs = []
        selected = runs[0] if runs else None
        if selected and selected.get("jobs_url"):
            jobs_obj = _get_json(str(selected["jobs_url"]))
            raw_jobs = jobs_obj.get("jobs") or []
            if isinstance(raw_jobs, list):
                jobs = raw_jobs
        classification, ok, degraded, reason, failures = classify_runs(runs, jobs)
        return CIWatchPacket(ok=ok, schema=CI_WATCH_SCHEMA, commit_sha=commit_sha, classification=classification, run_count=len(runs), selected_run=selected, jobs=jobs, failure_summary=failures, degraded=degraded, degraded_reason=reason)
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
        return CIWatchPacket(ok=False, schema=CI_WATCH_SCHEMA, commit_sha=commit_sha, classification="unknown", run_count=0, selected_run=None, jobs=[], failure_summary=[], degraded=True, degraded_reason=f"github_api_error:{exc.__class__.__name__}")

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="RHP-013.5 CI Watch Loop")
    parser.add_argument("--owner", default="jacksonjp0311-gif")
    parser.add_argument("--repo", default="hermes-agent-evo")
    parser.add_argument("--sha", required=True)
    parser.add_argument("--workflow", default="Tests")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    packet = watch_commit(args.owner, args.repo, args.sha, workflow=args.workflow)
    print(json.dumps(packet.as_dict(), indent=2, ensure_ascii=False))
    return 0 if packet.classification in {"green", "pending", "unknown"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
