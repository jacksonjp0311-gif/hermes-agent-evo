from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

RECOMMENDATION_VERSION = "v0.4.3"

NON_CLAIM_LOCK = (
    "Loop pressure repair recommendations are repository-bound and do not prove code correctness, "
    "truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness."
)

PRIMARY_LOCK = (
    "No repair recommendation may write, promote, or seal a change unless it declares "
    "pressure source, repair class, allowed action, blocked action, required validation, "
    "and non-claim boundary."
)

REPAIR_CLASSES: dict[str, dict[str, Any]] = {
    "NO_REPAIR": {
        "pressure_state": "stable",
        "severity": "none",
        "allowed_repair_action": "continue_after_validation",
        "blocked_actions": ["autonomous_patch", "version_promotion_without_validation", "api_write"],
        "required_validation_stack": ["validate_loop_drift_pressure", "validate_loop_repair_recommendations"],
        "downgrade_path": "if_pressure_reappears_emit_typed_repair_recommendation",
    },
    "SURFACE_REPAIR": {
        "pressure_state": "warning",
        "severity": "medium",
        "allowed_repair_action": "patch_readme_badge_route_map_mini_readme_or_public_table_only",
        "blocked_actions": ["runtime_code_patch", "memory_promotion", "public_release_seal", "api_write", "autonomous_patch"],
        "required_validation_stack": ["audit_readme_surface", "validate_surface_alignment", "emit_runtime_decision", "validate_runtime_decision"],
        "downgrade_path": "hold_release_until_surface_alignment_passes",
    },
    "REGISTRY_REPAIR": {
        "pressure_state": "warning",
        "severity": "medium",
        "allowed_repair_action": "normalize_version_registry_lifecycle_previous_seal_or_next_anchor",
        "blocked_actions": ["runtime_code_patch", "memory_promotion", "release_tag_creation", "api_write", "autonomous_patch"],
        "required_validation_stack": ["validate_surface_alignment", "emit_multilevel_alignment", "validate_multilevel_alignment", "validate_public_sync"],
        "downgrade_path": "mark_version_preseal_or_pending_until_registry_agrees",
    },
    "VALIDATOR_REPAIR": {
        "pressure_state": "warning",
        "severity": "medium",
        "allowed_repair_action": "patch_validator_expectation_grammar_or_registry_derivation_only",
        "blocked_actions": ["version_promotion", "public_sync_refresh_as_fix", "memory_promotion", "api_write", "autonomous_patch"],
        "required_validation_stack": ["validate_surface_alignment", "emit_multilevel_alignment", "validate_multilevel_alignment", "emit_runtime_decision", "validate_runtime_decision"],
        "downgrade_path": "block_promotion_until_validator_false_failure_removed",
    },
    "REPORT_REFRESH": {
        "pressure_state": "warning",
        "severity": "low",
        "allowed_repair_action": "refresh_report_artifacts_after_valid_state_transition",
        "blocked_actions": ["runtime_code_patch", "validator_patch", "memory_promotion", "api_write", "autonomous_patch"],
        "required_validation_stack": ["validate_public_sync", "validate_multilevel_alignment", "validate_loop_drift_pressure"],
        "downgrade_path": "keep_report_refresh_as_documentation_commit_only",
    },
    "MEMORY_ACTION_REPAIR": {
        "pressure_state": "warning",
        "severity": "high",
        "allowed_repair_action": "repair_candidate_memory_action_schema_evidence_or_rehydration_visibility",
        "blocked_actions": ["memory_promotion", "release_seal", "api_write", "autonomous_patch"],
        "required_validation_stack": ["emit_candidate_memory_actions", "validate_candidate_memory_actions", "validate_thread_rehydration_score", "validate_memory_promotion"],
        "downgrade_path": "downgrade_or_observe_only_until_candidate_action_is_valid",
    },
    "REHYDRATION_REPAIR": {
        "pressure_state": "warning",
        "severity": "medium",
        "allowed_repair_action": "refresh_rehydration_protocol_score_origin_runtime_or_architecture_scan",
        "blocked_actions": ["memory_promotion", "release_seal", "api_write", "autonomous_patch"],
        "required_validation_stack": ["validate_thread_rehydration_protocol", "emit_thread_rehydration_score", "validate_thread_rehydration_score"],
        "downgrade_path": "hold_next_cycle_influence_until_rehydration_visible",
    },
    "DOWNGRADE_RECOMMENDATION": {
        "pressure_state": "downgrade",
        "severity": "high",
        "allowed_repair_action": "keep_candidate_visible_but_remove_or_reduce_next_cycle_influence",
        "blocked_actions": ["memory_promotion", "release_seal", "api_write", "autonomous_patch"],
        "required_validation_stack": ["validate_negative_control_harness", "validate_memory_promotion", "validate_candidate_memory_actions"],
        "downgrade_path": "downgrade_candidate_or_loop_until_evidence_improves",
    },
    "BLOCK_RELEASE": {
        "pressure_state": "blocked",
        "severity": "critical",
        "allowed_repair_action": "stop_release_and_repair_failed_required_surface",
        "blocked_actions": ["version_promotion", "release_tag_creation", "public_sync_claim", "memory_promotion", "api_write", "autonomous_patch"],
        "required_validation_stack": ["validate_loop_drift_pressure", "validate_runtime_decision", "validate_release"],
        "downgrade_path": "block_release_until_pressure_under_threshold_and_required_validators_pass",
    },
    "HUMAN_REVIEW_REQUIRED": {
        "pressure_state": "review",
        "severity": "critical",
        "allowed_repair_action": "pause_and_request_human_review_of_ambiguous_or_conflicting_state",
        "blocked_actions": ["autonomous_patch", "version_promotion", "release_tag_creation", "api_write", "memory_promotion"],
        "required_validation_stack": ["manual_review", "rerun_full_validation_stack"],
        "downgrade_path": "observe_only_until_conflict_resolved",
    },
}

FINDING_TO_CLASS: dict[str, str] = {
    "validation_failures:public_sync": "REPORT_REFRESH",
    "public_sync_phase:preseal_tag_pending": "REPORT_REFRESH",
    "public_sync_preseal_pending_until_v0_4_2_tag": "REPORT_REFRESH",
    "validation_failures:runtime_decision": "VALIDATOR_REPAIR",
    "validation_failures:surface_alignment": "SURFACE_REPAIR",
    "validation_failures:multilevel_alignment": "VALIDATOR_REPAIR",
    "validation_failures:negative_control": "BLOCK_RELEASE",
    "validation_failures:memory_promotion": "MEMORY_ACTION_REPAIR",
    "validation_failures:candidate_memory_actions": "MEMORY_ACTION_REPAIR",
    "validation_failures:thread_rehydration_score": "REHYDRATION_REPAIR",
    "validation_failures:non_claim_lock": "HUMAN_REVIEW_REQUIRED",
}

COMPONENT_TO_CLASS: dict[str, str] = {
    "memory_action_drift": "MEMORY_ACTION_REPAIR",
    "rehydration_gap_pressure": "REHYDRATION_REPAIR",
    "registry_status_drift": "REGISTRY_REPAIR",
    "public_surface_delta": "SURFACE_REPAIR",
    "validator_expectation_drift": "VALIDATOR_REPAIR",
    "non_claim_lock_drift": "HUMAN_REVIEW_REQUIRED",
    "report_surface_lag": "REPORT_REFRESH",
}

def normalize_findings(raw_findings: list[str], validation_failures: list[str]) -> list[str]:
    findings: list[str] = []
    for item in raw_findings:
        if isinstance(item, str) and item.strip():
            item = item.strip()
            if item.startswith("validation_failures:") and "," in item:
                prefix, rest = item.split(":", 1)
                findings.extend(prefix + ":" + part.strip() for part in rest.split(",") if part.strip())
            else:
                findings.append(item)
    for item in validation_failures:
        if isinstance(item, str) and item.strip():
            findings.append("validation_failures:" + item.strip())
    seen: set[str] = set()
    ordered: list[str] = []
    for item in findings:
        if item not in seen:
            ordered.append(item)
            seen.add(item)
    return ordered

def pressure_state_from_value(value: float, threshold: float, findings: list[str]) -> str:
    if value > threshold:
        return "blocked"
    if findings:
        return "warning"
    return "stable"

def dominant_component(components: dict[str, Any]) -> str:
    numeric: list[tuple[str, float]] = []
    for key, value in components.items():
        if key == "rehydration_gap_count":
            continue
        try:
            numeric.append((key, float(value)))
        except Exception:
            pass
    if not numeric:
        return "none"
    key, value = max(numeric, key=lambda item: item[1])
    return key if value > 0 else "none"

def recommendation_id(seed: str) -> str:
    return "CMS-RR-" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:10]

def build_recommendation(
    *,
    pressure_source: str,
    repair_class: str,
    source_kind: str,
    source_value: Any,
) -> dict[str, Any]:
    spec = REPAIR_CLASSES[repair_class]
    return {
        "id": recommendation_id(pressure_source + ":" + repair_class),
        "pressure_source": pressure_source,
        "source_kind": source_kind,
        "source_value": source_value,
        "repair_class": repair_class,
        "pressure_state": spec["pressure_state"],
        "severity": spec["severity"],
        "allowed_repair_action": spec["allowed_repair_action"],
        "blocked_actions": spec["blocked_actions"],
        "required_validation_stack": spec["required_validation_stack"],
        "required_files": [],
        "downgrade_path": spec["downgrade_path"],
        "non_claim_lock": NON_CLAIM_LOCK,
        "status": "no_repair_required" if repair_class == "NO_REPAIR" else "repair_recommended",
    }

def build_loop_repair_recommendations(pressure: dict[str, Any]) -> dict[str, Any]:
    raw_findings = pressure.get("findings", [])
    if not isinstance(raw_findings, list):
        raw_findings = []
    validation_failures = pressure.get("validation_failures", [])
    if not isinstance(validation_failures, list):
        validation_failures = []

    findings = normalize_findings(raw_findings, validation_failures)
    components = pressure.get("components", {})
    if not isinstance(components, dict):
        components = {}

    pressure_value = float(pressure.get("loop_drift_pressure", 0.0) or 0.0)
    threshold = float(pressure.get("threshold", 0.25) or 0.25)
    stability_state = str(pressure.get("stability_state", "unknown"))
    overall_state = pressure_state_from_value(pressure_value, threshold, findings)

    recommendations: list[dict[str, Any]] = []
    unknown_findings: list[str] = []

    if pressure_value > threshold:
        recommendations.append(build_recommendation(
            pressure_source="loop_drift_pressure",
            repair_class="BLOCK_RELEASE",
            source_kind="threshold",
            source_value=pressure_value,
        ))

    for finding in findings:
        repair_class = FINDING_TO_CLASS.get(finding)
        if repair_class is None:
            unknown_findings.append(finding)
            repair_class = "HUMAN_REVIEW_REQUIRED"
        recommendations.append(build_recommendation(
            pressure_source=finding,
            repair_class=repair_class,
            source_kind="finding",
            source_value=finding,
        ))

    for component, value in components.items():
        if component == "rehydration_gap_count":
            continue
        try:
            numeric = float(value)
        except Exception:
            continue
        if numeric > 0:
            repair_class = COMPONENT_TO_CLASS.get(component, "HUMAN_REVIEW_REQUIRED")
            recommendations.append(build_recommendation(
                pressure_source=component,
                repair_class=repair_class,
                source_kind="component",
                source_value=numeric,
            ))

    if not recommendations and pressure_value <= threshold and stability_state == "stable_green_loop":
        recommendations.append(build_recommendation(
            pressure_source="none",
            repair_class="NO_REPAIR",
            source_kind="stable_green_loop",
            source_value=0.0,
        ))

    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for rec in recommendations:
        key = rec["pressure_source"] + "|" + rec["repair_class"]
        if key not in seen:
            deduped.append(rec)
            seen.add(key)

    dominant = dominant_component(components)
    dominant_class = COMPONENT_TO_CLASS.get(dominant, "NO_REPAIR" if dominant == "none" else "HUMAN_REVIEW_REQUIRED")

    passed = (
        len(deduped) > 0
        and pressure_value <= threshold
        and all(rec.get("repair_class") in REPAIR_CLASSES for rec in deduped)
        and all(rec.get("allowed_repair_action") for rec in deduped)
        and all(rec.get("blocked_actions") for rec in deduped)
        and all(rec.get("required_validation_stack") for rec in deduped)
        and all(rec.get("non_claim_lock") for rec in deduped)
    )

    report = {
        "schema": "CMS-SA-v0.4.3-loop-pressure-repair-recommendation",
        "version": RECOMMENDATION_VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_pressure_version": pressure.get("version"),
        "source_pressure_hash": pressure.get("pressure_hash"),
        "loop_drift_pressure": pressure_value,
        "threshold": threshold,
        "pressure_state": overall_state,
        "source_stability_state": stability_state,
        "dominant_pressure_source": dominant,
        "dominant_repair_class": dominant_class,
        "source_findings": findings,
        "recommendation_count": len(deduped),
        "recommendations": deduped,
        "unknown_findings": unknown_findings,
        "passed": passed,
        "primary_lock": PRIMARY_LOCK,
        "non_claim_lock": NON_CLAIM_LOCK,
    }
    canonical = json.dumps(report, sort_keys=True, separators=(",", ":"))
    report["recommendation_hash"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return report
