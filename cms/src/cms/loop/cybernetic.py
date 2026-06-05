"""Cybernetic memory loop report builder for CMS-SA v0.4.0."""

from __future__ import annotations

from hashlib import sha256
from typing import Any, Dict


VERSION = "v0.4.0"
SCHEMA = "CMS-SA-v0.4.0-cybernetic-memory-loop"
NON_CLAIM_LOCK = (
    "The cybernetic memory loop is repository-bound and does not prove code "
    "correctness, truth, AGI, consciousness, production readiness, security, "
    "external validation, or real-world correctness."
)


def _safe_int(value: Any) -> int:
    try:
        return int(value)
    except Exception:
        return 0


def build_cybernetic_memory_loop(memory_report: Dict[str, Any], decision_report: Dict[str, Any], control_report: Dict[str, Any]) -> Dict[str, Any]:
    promoted = _safe_int(memory_report.get("promoted_count"))
    downgraded = _safe_int(memory_report.get("downgraded_count"))
    observe_only = _safe_int(memory_report.get("observe_only_count"))
    candidates = _safe_int(memory_report.get("candidate_count"))

    false_promote_rejected = control_report.get("false_promote_rejected") is True
    downgrade_preserved = control_report.get("downgrade_preserved") is True
    observe_only_preserved = control_report.get("observe_only_preserved") is True

    decision_state = decision_report.get("decision") or decision_report.get("runtime_decision") or decision_report.get("state") or "unknown"

    influence_rules = []
    if promoted:
        influence_rules.append("promoted_memory_candidates_may_influence_next_cycle")
    if downgraded:
        influence_rules.append("downgraded_memory_candidates_must_remain_visible")
    if observe_only:
        influence_rules.append("observe_only_candidates_require_more_evidence")
    if false_promote_rejected:
        influence_rules.append("false_promote_controls_remain_active")

    loop_closed = candidates > 0 and promoted > 0 and false_promote_rejected and downgrade_preserved and observe_only_preserved and bool(memory_report.get("promotion_hash"))

    next_cycle_influence = {
        "allowed": loop_closed,
        "mode": "bounded_repository_influence" if loop_closed else "observe_only",
        "promoted_candidate_count": promoted,
        "downgraded_candidate_count": downgraded,
        "observe_only_candidate_count": observe_only,
        "rules": influence_rules,
        "hard_boundary": "no_api_write_no_autonomous_patch_no_external_truth_claim",
    }

    body: Dict[str, Any] = {
        "schema": SCHEMA,
        "version": VERSION,
        "passed": loop_closed,
        "loop_closed": loop_closed,
        "loop_chain": ["observe", "validate", "decide", "promote_or_downgrade", "write_memory_state", "emit_next_cycle_influence", "validate_loop_report"],
        "input_hashes": {
            "memory_promotion_hash": memory_report.get("promotion_hash"),
            "runtime_decision_hash": decision_report.get("decision_hash"),
            "negative_control_hash": control_report.get("harness_hash"),
        },
        "decision_state": decision_state,
        "memory_counts": {
            "candidate_count": candidates,
            "promoted_count": promoted,
            "downgraded_count": downgraded,
            "observe_only_count": observe_only,
        },
        "control_state": {
            "false_promote_rejected": false_promote_rejected,
            "downgrade_preserved": downgrade_preserved,
            "observe_only_preserved": observe_only_preserved,
        },
        "next_cycle_influence": next_cycle_influence,
        "core_law": "Memory is not storage; memory is controlled influence on the next cycle.",
        "non_claim_lock": NON_CLAIM_LOCK,
    }
    stable = repr(sorted((k, v) for k, v in body.items() if k != "loop_hash"))
    body["loop_hash"] = sha256(stable.encode("utf-8")).hexdigest()
    return body
