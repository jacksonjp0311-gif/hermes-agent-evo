from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

VERSION = "v0.4.8"

NON_CLAIM_LOCK = (
    "Authorized dry-apply sandbox reports are repository-bound execution simulations and do not prove "
    "code correctness, truth, AGI, consciousness, production readiness, security, external validation, "
    "autonomous repair authority, or real-world correctness."
)

PRIMARY_LOCK = (
    "No dry-apply sandbox may write live target surfaces. It may only simulate packet execution against "
    "virtual or copied targets, compare before/after hashes inside the sandbox, simulate rollback, "
    "preserve blocked actions, and emit validation evidence."
)

BLOCKED_ACTIONS_ALWAYS = [
    "live_target_write",
    "api_write",
    "git_commit",
    "git_push",
    "release_tag_creation",
    "autonomous_patch",
    "memory_promotion",
    "production_apply",
]


def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _sandbox_id(packet_id: str) -> str:
    return "CMS-DRY-APPLY-" + hashlib.sha256(packet_id.encode("utf-8")).hexdigest()[:10]


def build_dry_apply_sandbox(packet_manifest: dict[str, Any]) -> dict[str, Any]:
    packets = packet_manifest.get("packets", [])
    if not isinstance(packets, list):
        packets = []

    runs: list[dict[str, Any]] = []

    for packet in packets:
        if not isinstance(packet, dict):
            continue

        packet_id = str(packet.get("apply_packet_id", "unknown"))
        blocked = list(packet.get("blocked_actions_preserved", []))
        for action in BLOCKED_ACTIONS_ALWAYS:
            if action not in blocked:
                blocked.append(action)

        diff_entries = packet.get("diff_manifest", [])
        if not isinstance(diff_entries, list):
            diff_entries = []

        sandbox_operations: list[dict[str, Any]] = []
        rollback_simulation: list[dict[str, Any]] = []

        for entry in diff_entries:
            if not isinstance(entry, dict):
                continue
            target = str(entry.get("target", "unknown"))
            before_hash = entry.get("before_hash")
            after_hash = entry.get("after_hash")
            sandbox_operations.append({
                "target": target,
                "operation": entry.get("operation", "not_authorized"),
                "sandbox_target": f"sandbox://{target}",
                "live_target_write": False,
                "before_hash": before_hash,
                "after_hash": after_hash,
                "hash_compared": before_hash is not None and after_hash is not None,
                "diff_preview_present": entry.get("diff_preview") is not None,
            })
            rollback_simulation.append({
                "target": target,
                "sandbox_target": f"sandbox://{target}",
                "rollback_simulated": before_hash is not None,
                "rollback_restores_before_hash": before_hash is not None,
                "live_target_write": False,
            })

        run = {
            "dry_apply_run_id": _sandbox_id(packet_id),
            "source_apply_packet_id": packet_id,
            "source_apply_gate_id": packet.get("source_apply_gate_id", "unknown"),
            "packet_state": packet.get("packet_state", "unknown"),
            "sandbox_state": "simulated_no_live_writes",
            "apply_authority": False,
            "human_authorization_artifact_present": packet.get("human_authorization_artifact_present", False),
            "diff_entry_count": packet.get("diff_entry_count", len(diff_entries)),
            "sandbox_operation_count": len(sandbox_operations),
            "rollback_simulation_count": len(rollback_simulation),
            "rollback_simulation_passed": len(sandbox_operations) == len(rollback_simulation),
            "virtual_target_writes_performed": len(sandbox_operations),
            "live_target_writes_performed": 0,
            "api_writes_performed": 0,
            "git_commits_performed": 0,
            "git_pushes_performed": 0,
            "release_tags_created": 0,
            "sandbox_operations": sandbox_operations,
            "rollback_simulation": rollback_simulation,
            "pre_apply_validation_required": packet.get("pre_apply_validation_required", []),
            "post_apply_validation_required": packet.get("post_apply_validation_required", []),
            "blocked_actions_preserved": blocked,
            "non_claim_lock": NON_CLAIM_LOCK,
        }
        run["dry_apply_hash"] = _hash(run)
        runs.append(run)

    report = {
        "schema": "CMS-SA-v0.4.8-authorized-apply-executor-dry-apply-sandbox",
        "version": VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_apply_packet_manifest_hash": packet_manifest.get("apply_packet_manifest_hash"),
        "source_pressure_state": packet_manifest.get("source_pressure_state"),
        "source_apply_packet_count": packet_manifest.get("apply_packet_count", 0),
        "dry_apply_run_count": len(runs),
        "runs": runs,
        "virtual_target_writes_performed": sum(int(r.get("virtual_target_writes_performed", 0)) for r in runs),
        "live_target_writes_performed": 0,
        "api_writes_performed": 0,
        "git_commits_performed": 0,
        "git_pushes_performed": 0,
        "release_tags_created": 0,
        "passed": (
            len(runs) > 0
            and all(r.get("apply_authority") is False for r in runs)
            and all(r.get("live_target_writes_performed") == 0 for r in runs)
            and all(r.get("api_writes_performed") == 0 for r in runs)
            and all(r.get("git_commits_performed") == 0 for r in runs)
            and all(r.get("git_pushes_performed") == 0 for r in runs)
            and all(r.get("release_tags_created") == 0 for r in runs)
            and all(r.get("rollback_simulation_passed") is True for r in runs)
        ),
        "primary_lock": PRIMARY_LOCK,
        "non_claim_lock": NON_CLAIM_LOCK,
    }
    report["dry_apply_sandbox_hash"] = _hash(report)
    return report