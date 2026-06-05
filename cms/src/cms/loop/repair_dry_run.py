from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

VERSION = "v0.4.5"

NON_CLAIM_LOCK = (
    "Authorized repair dry-runs are repository-bound simulations and do not prove code correctness, "
    "truth, AGI, consciousness, production readiness, security, external validation, autonomous repair "
    "authority, or real-world correctness."
)

PRIMARY_LOCK = (
    "No repair dry-run may write target surfaces unless explicit human authorization, dry-run diff, "
    "rollback path, touched-surface boundary, blocked-action preservation, and required validation "
    "evidence are declared."
)

BLOCKED_ACTIONS_ALWAYS = [
    "target_surface_write",
    "api_write",
    "autonomous_patch",
    "release_tag_creation",
    "memory_promotion",
    "git_commit",
    "git_push",
]

def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def _dry_run_id(plan_id: str) -> str:
    return "CMS-DRYRUN-" + hashlib.sha256(plan_id.encode("utf-8")).hexdigest()[:10]

def build_authorized_dry_run(closure_report: dict[str, Any]) -> dict[str, Any]:
    plans = closure_report.get("plans", [])
    if not isinstance(plans, list):
        plans = []

    dry_runs: list[dict[str, Any]] = []
    for plan in plans:
        if not isinstance(plan, dict):
            continue

        repair_class = str(plan.get("repair_class", "HUMAN_REVIEW_REQUIRED"))
        plan_id = str(plan.get("plan_id", "unknown"))
        touched = plan.get("touched_surface_boundary", [])
        required_validation = plan.get("required_validation_evidence", [])
        blocked = list(plan.get("blocked_actions_preserved", []))
        for item in BLOCKED_ACTIONS_ALWAYS:
            if item not in blocked:
                blocked.append(item)

        dry_run = {
            "dry_run_id": _dry_run_id(plan_id),
            "source_plan_id": plan_id,
            "source_recommendation_id": plan.get("source_recommendation_id", "unknown"),
            "repair_class": repair_class,
            "execution_mode": "dry_run_only",
            "write_authority": False,
            "human_authorization_required_for_write": True,
            "target_surface_writes": [],
            "proposed_diff_manifest": [],
            "touched_surface_boundary": touched if isinstance(touched, list) else [str(touched)],
            "required_validation_evidence": required_validation if isinstance(required_validation, list) else [str(required_validation)],
            "rollback_path": "discard_dry_run_report_and_recompute_from_latest_validated_closure_plan",
            "blocked_actions_preserved": blocked,
            "dry_run_state": "simulated_no_write",
            "closure_state_before": plan.get("closure_state", "unknown"),
            "closure_state_after_dry_run": plan.get("closure_state", "unknown"),
            "non_claim_lock": NON_CLAIM_LOCK,
        }
        dry_run["dry_run_hash"] = _hash(dry_run)
        dry_runs.append(dry_run)

    report = {
        "schema": "CMS-SA-v0.4.5-authorized-repair-dry-run-executor",
        "version": VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_closure_hash": closure_report.get("closure_hash"),
        "source_pressure_state": closure_report.get("source_pressure_state"),
        "source_plan_count": closure_report.get("plan_count", 0),
        "dry_run_count": len(dry_runs),
        "dry_runs": dry_runs,
        "target_writes_performed": 0,
        "api_writes_performed": 0,
        "commits_performed": 0,
        "tags_created": 0,
        "passed": (
            len(dry_runs) > 0
            and all(d.get("write_authority") is False for d in dry_runs)
            and all(d.get("target_surface_writes") == [] for d in dry_runs)
            and all(d.get("rollback_path") for d in dry_runs)
            and all(d.get("required_validation_evidence") for d in dry_runs)
            and all("autonomous_patch" in d.get("blocked_actions_preserved", []) for d in dry_runs)
        ),
        "primary_lock": PRIMARY_LOCK,
        "non_claim_lock": NON_CLAIM_LOCK,
    }
    report["dry_run_hash"] = _hash(report)
    return report