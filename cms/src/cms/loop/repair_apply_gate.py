from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

VERSION = "v0.4.6"

NON_CLAIM_LOCK = (
    "Authorized repair apply gates are repository-bound authorization ledgers and do not prove code "
    "correctness, truth, AGI, consciousness, production readiness, security, external validation, "
    "autonomous repair authority, or real-world correctness."
)

PRIMARY_LOCK = (
    "No repair apply may execute unless it references a validated dry-run id, carries explicit human "
    "authorization, declares exact target writes, includes rollback entries for every target, preserves "
    "blocked actions, and passes the required validation stack before and after apply."
)

BLOCKED_ACTIONS_ALWAYS = [
    "autonomous_patch",
    "api_write",
    "silent_target_write",
    "unreviewed_git_commit",
    "unreviewed_git_push",
    "release_tag_creation",
    "memory_promotion",
]


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _gate_id(dry_run_id: str) -> str:
    return "CMS-APPLY-GATE-" + hashlib.sha256(dry_run_id.encode("utf-8")).hexdigest()[:10]


def build_apply_gate(dry_run_report: dict[str, Any]) -> dict[str, Any]:
    dry_runs = dry_run_report.get("dry_runs", [])
    if not isinstance(dry_runs, list):
        dry_runs = []

    gates: list[dict[str, Any]] = []
    rollback_ledger: list[dict[str, Any]] = []

    for dry in dry_runs:
        if not isinstance(dry, dict):
            continue

        dry_run_id = str(dry.get("dry_run_id", "unknown"))
        blocked = list(dry.get("blocked_actions_preserved", []))
        for action in BLOCKED_ACTIONS_ALWAYS:
            if action not in blocked:
                blocked.append(action)

        requested_targets = dry.get("target_surface_writes", [])
        if not isinstance(requested_targets, list):
            requested_targets = [str(requested_targets)]

        gate = {
            "apply_gate_id": _gate_id(dry_run_id),
            "source_dry_run_id": dry_run_id,
            "source_plan_id": dry.get("source_plan_id", "unknown"),
            "source_recommendation_id": dry.get("source_recommendation_id", "unknown"),
            "repair_class": dry.get("repair_class", "HUMAN_REVIEW_REQUIRED"),
            "gate_state": "blocked_pending_explicit_human_authorization",
            "apply_authority": False,
            "human_authorization_present": False,
            "authorization_packet_id": None,
            "exact_target_writes_declared": bool(requested_targets),
            "target_writes_allowed": [],
            "target_writes_performed": 0,
            "api_writes_performed": 0,
            "git_commits_performed": 0,
            "git_pushes_performed": 0,
            "release_tags_created": 0,
            "rollback_required": True,
            "rollback_ready": False,
            "rollback_entries": [],
            "pre_apply_validation_required": dry.get("required_validation_evidence", []),
            "post_apply_validation_required": dry.get("required_validation_evidence", []),
            "blocked_actions_preserved": blocked,
            "touched_surface_boundary": dry.get("touched_surface_boundary", []),
            "non_claim_lock": NON_CLAIM_LOCK,
        }

        gate["gate_hash"] = _hash(gate)
        gates.append(gate)

        rollback_ledger.append({
            "apply_gate_id": gate["apply_gate_id"],
            "source_dry_run_id": dry_run_id,
            "rollback_state": "not_ready_no_authorized_apply",
            "rollback_required": True,
            "rollback_ready": False,
            "rollback_entries": [],
            "target_writes_performed": 0,
            "non_claim_lock": NON_CLAIM_LOCK,
        })

    report = {
        "schema": "CMS-SA-v0.4.6-authorized-repair-apply-gate-and-rollback-ledger",
        "version": VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_dry_run_hash": dry_run_report.get("dry_run_hash"),
        "source_pressure_state": dry_run_report.get("source_pressure_state"),
        "source_dry_run_count": dry_run_report.get("dry_run_count", 0),
        "apply_gate_count": len(gates),
        "rollback_ledger_count": len(rollback_ledger),
        "gates": gates,
        "rollback_ledger": rollback_ledger,
        "target_writes_performed": 0,
        "api_writes_performed": 0,
        "git_commits_performed": 0,
        "git_pushes_performed": 0,
        "release_tags_created": 0,
        "passed": (
            len(gates) > 0
            and all(g.get("apply_authority") is False for g in gates)
            and all(g.get("human_authorization_present") is False for g in gates)
            and all(g.get("target_writes_performed") == 0 for g in gates)
            and all(g.get("api_writes_performed") == 0 for g in gates)
            and all(g.get("git_commits_performed") == 0 for g in gates)
            and all(g.get("rollback_required") is True for g in gates)
            and all(g.get("rollback_ready") is False for g in gates)
        ),
        "primary_lock": PRIMARY_LOCK,
        "non_claim_lock": NON_CLAIM_LOCK,
    }
    report["apply_gate_hash"] = _hash(report)
    return report