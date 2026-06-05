"""Loop Drift Pressure metrics for CMS-SA v0.4.2.

This layer detects pressure inside an otherwise-green repository loop.
It is a governance signal, not a correctness proof.
"""

from __future__ import annotations

from hashlib import sha256
from typing import Any, Dict, List

VERSION = "v0.4.2"
SCHEMA = "CMS-SA-v0.4.2-loop-drift-pressure-report"
LOCK = "No green loop is considered stable if drift pressure exceeds the declared threshold without downgrade, warning, or repair recommendation."
NON_CLAIM_LOCK = "Loop drift pressure metrics are repository-bound and do not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness."


def _has_non_claim(value: Any) -> bool:
    text = str(value)
    return ("does not prove" in text) or ("do not prove" in text)


def _ok(value: Any) -> bool:
    return value is True


def _metric(ok: bool) -> float:
    return 0.0 if ok else 1.0


def build_loop_drift_pressure(
    *,
    loop: Dict[str, Any],
    candidate_actions: Dict[str, Any],
    rehydration_score: Dict[str, Any],
    registry: Dict[str, Any],
    public_sync: Dict[str, Any],
    runtime_decision: Dict[str, Any],
    validation_surfaces: Dict[str, Dict[str, Any]],
    threshold: float = 0.25,
) -> Dict[str, Any]:
    findings: List[str] = []

    loop_closed = _ok(loop.get("loop_closed"))
    next_influence = loop.get("next_cycle_influence", {})
    influence_allowed = _ok(next_influence.get("allowed"))

    action_count = int(candidate_actions.get("candidate_action_count", 0) or 0)
    actions = candidate_actions.get("actions", [])
    rehydration_visible_count = 0
    action_issues = 0

    for action in actions if isinstance(actions, list) else []:
        if action.get("rehydration_visible") is True:
            rehydration_visible_count += 1
        for key in ["candidate_id", "downgrade_path", "required_evidence_next", "allowed_next_action"]:
            if not action.get(key):
                action_issues += 1
        if not _has_non_claim(action.get("non_claim_lock", "")):
            action_issues += 1

    counts = loop.get("memory_counts", {})
    candidate_count = int(counts.get("candidate_count", action_count) or action_count)
    promoted = int(counts.get("promoted_count", 0) or 0)
    downgraded = int(counts.get("downgraded_count", 0) or 0)
    observe_only = int(counts.get("observe_only_count", 0) or 0)

    rehydration_ready = _ok(rehydration_score.get("version_ready"))
    rehydration_gap_count = len(rehydration_score.get("missing_surfaces", []) or []) + len(rehydration_score.get("stale_surface_risks", []) or [])

    registry_version_ok = registry.get("current_version") == "v0.4.2"
    registry_next_ok = "v0.4.3" in str(registry.get("next_anchor", ""))
    registry_prev_ok = registry.get("previous_version") == "v0.4.1"

    v041_status = "unknown"
    for item in registry.get("versions", []):
        if isinstance(item, dict) and item.get("version") == "v0.4.1":
            v041_status = str(item.get("status", "unknown"))
            break

    public_sync_preseal_tag_pending = (
        public_sync.get("passed") is not True
        and public_sync.get("registry_current_version") == registry.get("current_version")
        and public_sync.get("head_origin_match") is True
        and public_sync.get("readme_checkpoint_present") is True
        and public_sync.get("release_tag_status") == "missing"
    )
    public_sync_preseal_pending = (
        public_sync.get("registry_current_version") != registry.get("current_version")
        or public_sync_preseal_tag_pending
    )
    public_sync_core_ok = (
        public_sync.get("passed") is True
        and public_sync.get("head_origin_match") is True
        and public_sync.get("release_tag_status") == "present_and_ancestor_of_head"
    ) or public_sync_preseal_tag_pending

    validation_failures = [
        name
        for name, obj in validation_surfaces.items()
        if obj.get("passed") is not True and not (name == "public_sync" and public_sync_preseal_tag_pending)
    ]

    grammar_drift = 0
    if "are repository-bound and does not prove" in str(candidate_actions.get("non_claim_lock", "")):
        grammar_drift += 1

    memory_action_drift = 0.0
    if action_count <= 0:
        memory_action_drift += 0.50
    if candidate_count and action_count != candidate_count:
        memory_action_drift += 0.25
    if action_count and rehydration_visible_count != action_count:
        memory_action_drift += 0.25
    if action_issues:
        memory_action_drift += min(0.50, action_issues * 0.10)
    memory_action_drift = min(1.0, memory_action_drift)

    rehydration_gap_pressure = min(1.0, rehydration_gap_count * 0.25 + _metric(rehydration_ready) * 0.50)
    registry_status_drift = min(1.0, (_metric(registry_version_ok) + _metric(registry_next_ok) + _metric(registry_prev_ok)) / 3.0)
    public_surface_delta = 0.20 if public_sync_preseal_pending and public_sync_core_ok else (0.0 if public_sync_core_ok else 1.0)
    validator_expectation_drift = min(1.0, len(validation_failures) * 0.20)
    non_claim_lock_drift = min(1.0, grammar_drift * 0.50 + _metric(_has_non_claim(candidate_actions.get("non_claim_lock", ""))) * 0.50)

    report_surface_lag = 0.0
    if v041_status in {"pending_validation", "unknown", ""}:
        report_surface_lag += 0.25
    if not loop_closed:
        report_surface_lag += 0.25
    if not influence_allowed:
        report_surface_lag += 0.25
    if runtime_decision.get("decision") != "promote":
        report_surface_lag += 0.25
    report_surface_lag = min(1.0, report_surface_lag)

    components = {
        "memory_action_drift": round(memory_action_drift, 4),
        "rehydration_gap_count": rehydration_gap_count,
        "rehydration_gap_pressure": round(rehydration_gap_pressure, 4),
        "registry_status_drift": round(registry_status_drift, 4),
        "public_surface_delta": round(public_surface_delta, 4),
        "validator_expectation_drift": round(validator_expectation_drift, 4),
        "non_claim_lock_drift": round(non_claim_lock_drift, 4),
        "report_surface_lag": round(report_surface_lag, 4),
    }

    weighted = (
        components["memory_action_drift"] * 0.18
        + components["rehydration_gap_pressure"] * 0.16
        + components["registry_status_drift"] * 0.14
        + components["public_surface_delta"] * 0.14
        + components["validator_expectation_drift"] * 0.14
        + components["non_claim_lock_drift"] * 0.12
        + components["report_surface_lag"] * 0.12
    )
    loop_drift_pressure = round(float(weighted), 4)

    if grammar_drift:
        findings.append("candidate_action_non_claim_grammar_drift")
    if v041_status == "pending_validation":
        findings.append("registry_v0_4_1_status_pending_after_public_sync")
    if validation_failures:
        findings.append("validation_failures:" + ",".join(validation_failures))
    if rehydration_gap_count:
        findings.append("rehydration_gap_surfaces_present")
    if public_sync_preseal_tag_pending:
        findings.append("public_sync_phase:preseal_tag_pending")
    elif public_sync_preseal_pending:
        findings.append("public_sync_preseal_pending_until_v0_4_2_tag")

    if loop_drift_pressure > threshold:
        stability_state = "pressure_exceeds_threshold"
        recommended_action = "downgrade_or_repair_before_next_cycle_promotion"
        passed = False
    elif findings:
        stability_state = "green_with_repair_recommendation"
        recommended_action = "repair_pressure_findings_before_release_seal"
        passed = True
    else:
        stability_state = "stable_green_loop"
        recommended_action = "continue_to_next_layer_after_validation"
        passed = True

    stable = repr(components) + repr(loop.get("loop_hash")) + repr(candidate_actions.get("action_hash")) + repr(rehydration_score.get("rehydration_hash"))

    return {
        "schema": SCHEMA,
        "version": VERSION,
        "passed": passed,
        "threshold": threshold,
        "loop_drift_pressure": loop_drift_pressure,
        "components": components,
        "stability_state": stability_state,
        "recommended_action": recommended_action,
        "findings": findings,
        "validation_failures": validation_failures,
        "memory_counts": {
            "candidate_count": candidate_count,
            "promoted_count": promoted,
            "downgraded_count": downgraded,
            "observe_only_count": observe_only,
            "candidate_action_count": action_count,
            "rehydration_visible_count": rehydration_visible_count,
        },
        "input_hashes": {
            "loop_hash": loop.get("loop_hash"),
            "candidate_action_hash": candidate_actions.get("action_hash"),
            "rehydration_hash": rehydration_score.get("rehydration_hash"),
            "runtime_decision_hash": runtime_decision.get("decision_hash"),
        },
        "primary_lock": LOCK,
        "pressure_hash": sha256(stable.encode("utf-8")).hexdigest(),
        "non_claim_lock": NON_CLAIM_LOCK,
    }
