from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

VERSION = "v0.4.7"

NON_CLAIM_LOCK = (
    "Authorized apply packets and diff manifests are repository-bound authorization evidence and do not "
    "prove code correctness, truth, AGI, consciousness, production readiness, security, external "
    "validation, autonomous repair authority, or real-world correctness."
)

PRIMARY_LOCK = (
    "No apply packet may authorize a repair unless it references a validated apply gate, includes a "
    "human authorization artifact, declares exact diff entries for every target write, binds rollback "
    "entries one-to-one with diff entries, preserves blocked actions, and passes pre-apply validation."
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


def _packet_id(gate_id: str) -> str:
    return "CMS-APPLY-PACKET-" + hashlib.sha256(gate_id.encode("utf-8")).hexdigest()[:10]


def build_apply_packet_manifest(apply_gate_report: dict[str, Any]) -> dict[str, Any]:
    gates = apply_gate_report.get("gates", [])
    if not isinstance(gates, list):
        gates = []

    packets: list[dict[str, Any]] = []
    diff_manifest: list[dict[str, Any]] = []

    for gate in gates:
        if not isinstance(gate, dict):
            continue

        gate_id = str(gate.get("apply_gate_id", "unknown"))
        blocked = list(gate.get("blocked_actions_preserved", []))
        for action in BLOCKED_ACTIONS_ALWAYS:
            if action not in blocked:
                blocked.append(action)

        target_writes_allowed = gate.get("target_writes_allowed", [])
        if not isinstance(target_writes_allowed, list):
            target_writes_allowed = [str(target_writes_allowed)]

        exact_diff_entries = []
        rollback_entries = []
        for target in target_writes_allowed:
            if not target:
                continue
            entry = {
                "target": str(target),
                "operation": "not_authorized",
                "before_hash": None,
                "after_hash": None,
                "diff_preview": None,
                "write_authority": False,
            }
            exact_diff_entries.append(entry)
            rollback_entries.append({
                "target": str(target),
                "rollback_operation": "not_available_without_authorized_diff",
                "rollback_before_hash": None,
                "rollback_ready": False,
            })

        packet = {
            "apply_packet_id": _packet_id(gate_id),
            "source_apply_gate_id": gate_id,
            "source_dry_run_id": gate.get("source_dry_run_id", "unknown"),
            "source_plan_id": gate.get("source_plan_id", "unknown"),
            "source_recommendation_id": gate.get("source_recommendation_id", "unknown"),
            "repair_class": gate.get("repair_class", "HUMAN_REVIEW_REQUIRED"),
            "packet_state": "blocked_missing_human_authorization_packet",
            "human_authorization_artifact_present": False,
            "human_authorization_artifact_id": None,
            "apply_authority": False,
            "exact_diff_entries_declared": bool(exact_diff_entries),
            "diff_entry_count": len(exact_diff_entries),
            "rollback_entry_count": len(rollback_entries),
            "rollback_binds_every_diff": len(exact_diff_entries) == len(rollback_entries),
            "target_writes_requested": target_writes_allowed,
            "target_writes_performed": 0,
            "api_writes_performed": 0,
            "git_commits_performed": 0,
            "git_pushes_performed": 0,
            "release_tags_created": 0,
            "pre_apply_validation_required": gate.get("pre_apply_validation_required", []),
            "post_apply_validation_required": gate.get("post_apply_validation_required", []),
            "blocked_actions_preserved": blocked,
            "diff_manifest": exact_diff_entries,
            "rollback_entries": rollback_entries,
            "non_claim_lock": NON_CLAIM_LOCK,
        }
        packet["apply_packet_hash"] = _hash(packet)
        packets.append(packet)

        diff_manifest.append({
            "apply_packet_id": packet["apply_packet_id"],
            "source_apply_gate_id": gate_id,
            "diff_state": "blocked_no_authorized_diff",
            "diff_entry_count": len(exact_diff_entries),
            "rollback_entry_count": len(rollback_entries),
            "target_writes_performed": 0,
            "non_claim_lock": NON_CLAIM_LOCK,
        })

    report = {
        "schema": "CMS-SA-v0.4.7-authorized-apply-packet-and-diff-manifest",
        "version": VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_apply_gate_hash": apply_gate_report.get("apply_gate_hash"),
        "source_pressure_state": apply_gate_report.get("source_pressure_state"),
        "source_apply_gate_count": apply_gate_report.get("apply_gate_count", 0),
        "apply_packet_count": len(packets),
        "diff_manifest_count": len(diff_manifest),
        "packets": packets,
        "diff_manifest_ledger": diff_manifest,
        "target_writes_performed": 0,
        "api_writes_performed": 0,
        "git_commits_performed": 0,
        "git_pushes_performed": 0,
        "release_tags_created": 0,
        "passed": (
            len(packets) > 0
            and all(p.get("apply_authority") is False for p in packets)
            and all(p.get("human_authorization_artifact_present") is False for p in packets)
            and all(p.get("target_writes_performed") == 0 for p in packets)
            and all(p.get("api_writes_performed") == 0 for p in packets)
            and all(p.get("git_commits_performed") == 0 for p in packets)
            and all(p.get("rollback_binds_every_diff") is True for p in packets)
        ),
        "primary_lock": PRIMARY_LOCK,
        "non_claim_lock": NON_CLAIM_LOCK,
    }
    report["apply_packet_manifest_hash"] = _hash(report)
    return report