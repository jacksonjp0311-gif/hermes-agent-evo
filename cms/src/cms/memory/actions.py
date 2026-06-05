"""Candidate-level memory actions for CMS-SA v0.4.1."""

from __future__ import annotations

from hashlib import sha256
from typing import Any, Dict, List


VERSION = "v0.4.1"
SCHEMA = "CMS-SA-v0.4.1-candidate-memory-action-report"
NON_CLAIM_LOCK = (
    "Candidate memory actions are repository-bound and do not prove code correctness, "
    "truth, AGI, consciousness, production readiness, security, external validation, "
    "or real-world correctness."
)


def _decision(candidate: Dict[str, Any]) -> str:
    raw = str(candidate.get("memory_decision", "observe_only"))
    if raw in {"promote_memory", "downgrade_memory", "observe_only", "block_memory"}:
        return raw
    if candidate.get("promoted") is True:
        return "promote_memory"
    if candidate.get("downgraded") is True:
        return "downgrade_memory"
    if candidate.get("observe_only") is True:
        return "observe_only"
    if candidate.get("blocked") is True:
        return "block_memory"
    return "observe_only"


def _action_for(decision: str) -> str:
    if decision == "promote_memory":
        return "may_influence_next_cycle_after_rehydration_scan"
    if decision == "downgrade_memory":
        return "remain_visible_as_downgraded_boundary"
    if decision == "observe_only":
        return "hold_for_future_evidence_recheck"
    return "block_from_next_cycle_influence"


def _blocked_for(decision: str) -> list[str]:
    base = ["external_truth_claim", "autonomous_patch_write", "api_write_without_authorization"]
    if decision != "promote_memory":
        base.append("direct_next_cycle_influence")
    if decision == "observe_only":
        base.append("promotion_without_new_evidence")
    if decision == "downgrade_memory":
        base.append("silent_removal_from_memory_surface")
    return base


def build_candidate_memory_actions(memory_report: Dict[str, Any], loop_report: Dict[str, Any]) -> Dict[str, Any]:
    actions: List[Dict[str, Any]] = []
    for candidate in memory_report.get("candidates", []):
        decision = _decision(candidate)
        item = {
            "candidate_id": candidate.get("candidate_id"),
            "source": candidate.get("source"),
            "memory_decision": decision,
            "allowed_next_action": _action_for(decision),
            "blocked_actions": _blocked_for(decision),
            "required_evidence_next": (
                "retain_replay_hash_control_hash_and_rehydration_visibility"
                if decision == "promote_memory"
                else "new_repository_bound_evidence_required_before_promotion"
            ),
            "downgrade_visibility_required": decision in {"downgrade_memory", "observe_only", "block_memory"},
            "observe_only_recheck_condition": (
                candidate.get("falsification_condition")
                if decision == "observe_only"
                else "not_applicable"
            ),
            "rehydration_visible": True,
            "evidence_utility": candidate.get("evidence_utility"),
            "negative_control_passed": candidate.get("negative_control_passed"),
            "falsification_condition": candidate.get("falsification_condition"),
            "downgrade_path": candidate.get("downgrade_path"),
            "non_claim_lock": candidate.get("non_claim_lock") or NON_CLAIM_LOCK,
        }
        actions.append(item)

    stable = repr(actions) + repr(loop_report.get("loop_hash")) + repr(memory_report.get("promotion_hash"))
    return {
        "schema": SCHEMA,
        "version": VERSION,
        "passed": True,
        "candidate_action_count": len(actions),
        "actions": actions,
        "input_hashes": {
            "memory_promotion_hash": memory_report.get("promotion_hash"),
            "loop_hash": loop_report.get("loop_hash"),
        },
        "primary_lock": "No promoted memory may influence the next cycle without a typed candidate-level action, downgrade boundary, evidence requirement, and rehydration-visible status.",
        "action_hash": sha256(stable.encode("utf-8")).hexdigest(),
        "non_claim_lock": NON_CLAIM_LOCK,
    }
