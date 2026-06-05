from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

VERSION = "v0.4.4"

NON_CLAIM_LOCK = (
    "Repair execution planning and closure ledgers are repository-bound and do not prove "
    "code correctness, truth, AGI, consciousness, production readiness, security, external "
    "validation, autonomous repair authority, or real-world correctness."
)

PRIMARY_LOCK = (
    "No repair recommendation may be marked closed unless it has a plan id, source recommendation id, "
    "declared execution mode, touched-surface boundary, required validation evidence, closure state, "
    "blocked-action preservation, and non-claim boundary."
)

EXECUTION_MODE_BY_CLASS: dict[str, str] = {
    "NO_REPAIR": "no_op_stability_record",
    "SURFACE_REPAIR": "human_authorized_surface_patch_plan",
    "REGISTRY_REPAIR": "human_authorized_registry_lifecycle_plan",
    "VALIDATOR_REPAIR": "human_authorized_validator_compatibility_plan",
    "REPORT_REFRESH": "human_authorized_report_refresh_plan",
    "MEMORY_ACTION_REPAIR": "human_authorized_memory_action_schema_plan",
    "REHYDRATION_REPAIR": "human_authorized_rehydration_refresh_plan",
    "DOWNGRADE_RECOMMENDATION": "human_authorized_downgrade_plan",
    "BLOCK_RELEASE": "release_block_plan",
    "HUMAN_REVIEW_REQUIRED": "manual_review_plan",
}

TOUCHED_SURFACES_BY_CLASS: dict[str, list[str]] = {
    "NO_REPAIR": ["reports/loop"],
    "SURFACE_REPAIR": ["README.md", "configs/*/README.md", "src/cms/*/README.md", "scripts/*/README.md", "outputs/*/README.md", "reports/*/README.md"],
    "REGISTRY_REPAIR": ["outputs/version_registry/cms_version_registry.json", "outputs/roadmap/next_anchor.md", "reports/public_sync"],
    "VALIDATOR_REPAIR": ["scripts/validation", "reports/*"],
    "REPORT_REFRESH": ["outputs/*", "reports/*"],
    "MEMORY_ACTION_REPAIR": ["configs/memory", "src/cms/memory", "scripts/memory", "reports/memory"],
    "REHYDRATION_REPAIR": ["scripts/rehydration", "reports/rehydration"],
    "DOWNGRADE_RECOMMENDATION": ["outputs/memory", "reports/memory", "reports/controls"],
    "BLOCK_RELEASE": ["reports/decision", "reports/loop", "outputs/release_seals"],
    "HUMAN_REVIEW_REQUIRED": ["reports/review", "outputs/review"],
}

def _hash(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def _plan_id(recommendation_id: str, repair_class: str) -> str:
    return "CMS-PLAN-" + hashlib.sha256(f"{recommendation_id}:{repair_class}".encode("utf-8")).hexdigest()[:10]

def build_repair_closure_plan(recommendation_report: dict[str, Any]) -> dict[str, Any]:
    recommendations = recommendation_report.get("recommendations", [])
    if not isinstance(recommendations, list):
        recommendations = []

    plans: list[dict[str, Any]] = []
    closure_ledger: list[dict[str, Any]] = []

    for rec in recommendations:
        if not isinstance(rec, dict):
            continue
        repair_class = str(rec.get("repair_class", "HUMAN_REVIEW_REQUIRED"))
        rec_id = str(rec.get("id", "unknown"))
        mode = EXECUTION_MODE_BY_CLASS.get(repair_class, "manual_review_plan")
        required_validation = rec.get("required_validation_stack", [])
        if not isinstance(required_validation, list):
            required_validation = [str(required_validation)]
        blocked_actions = rec.get("blocked_actions", [])
        if not isinstance(blocked_actions, list):
            blocked_actions = [str(blocked_actions)]
        touched = TOUCHED_SURFACES_BY_CLASS.get(repair_class, ["reports/review"])

        state = "closed_no_op" if repair_class == "NO_REPAIR" else "planned_not_executed"
        authorization_required = repair_class != "NO_REPAIR"

        plan = {
            "plan_id": _plan_id(rec_id, repair_class),
            "source_recommendation_id": rec_id,
            "pressure_source": rec.get("pressure_source", "unknown"),
            "repair_class": repair_class,
            "execution_mode": mode,
            "authorization_required": authorization_required,
            "allowed_repair_action": rec.get("allowed_repair_action", ""),
            "blocked_actions_preserved": blocked_actions,
            "touched_surface_boundary": touched,
            "required_validation_evidence": required_validation,
            "closure_state": state,
            "closure_evidence": [] if authorization_required else required_validation,
            "downgrade_path": rec.get("downgrade_path", ""),
            "non_claim_lock": NON_CLAIM_LOCK,
        }
        plan["plan_hash"] = _hash(plan)
        plans.append(plan)
        closure_ledger.append({
            "plan_id": plan["plan_id"],
            "source_recommendation_id": rec_id,
            "repair_class": repair_class,
            "closure_state": state,
            "evidence_status": "not_applicable_no_op" if repair_class == "NO_REPAIR" else "pending_execution_evidence",
            "blocked_actions_preserved": blocked_actions,
            "non_claim_lock": NON_CLAIM_LOCK,
        })

    if not plans and recommendation_report.get("pressure_state") == "stable":
        plan = {
            "plan_id": "CMS-PLAN-STABLE-NOOP",
            "source_recommendation_id": "none",
            "pressure_source": "none",
            "repair_class": "NO_REPAIR",
            "execution_mode": "no_op_stability_record",
            "authorization_required": False,
            "allowed_repair_action": "continue_after_validation",
            "blocked_actions_preserved": ["autonomous_patch", "version_promotion_without_validation", "api_write"],
            "touched_surface_boundary": ["reports/loop"],
            "required_validation_evidence": ["validate_loop_drift_pressure", "validate_loop_repair_recommendations"],
            "closure_state": "closed_no_op",
            "closure_evidence": ["stable_green_loop"],
            "downgrade_path": "if_pressure_reappears_emit_typed_repair_recommendation",
            "non_claim_lock": NON_CLAIM_LOCK,
        }
        plan["plan_hash"] = _hash(plan)
        plans.append(plan)
        closure_ledger.append({
            "plan_id": plan["plan_id"],
            "source_recommendation_id": "none",
            "repair_class": "NO_REPAIR",
            "closure_state": "closed_no_op",
            "evidence_status": "not_applicable_no_op",
            "blocked_actions_preserved": plan["blocked_actions_preserved"],
            "non_claim_lock": NON_CLAIM_LOCK,
        })

    report = {
        "schema": "CMS-SA-v0.4.4-repair-execution-plan-and-closure-ledger",
        "version": VERSION,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_recommendation_hash": recommendation_report.get("recommendation_hash"),
        "source_pressure_state": recommendation_report.get("pressure_state"),
        "source_stability_state": recommendation_report.get("source_stability_state"),
        "source_recommendation_count": recommendation_report.get("recommendation_count", 0),
        "plan_count": len(plans),
        "closure_count": len(closure_ledger),
        "plans": plans,
        "closure_ledger": closure_ledger,
        "passed": len(plans) > 0 and all(p.get("plan_id") and p.get("source_recommendation_id") and p.get("execution_mode") and p.get("touched_surface_boundary") and p.get("required_validation_evidence") and p.get("closure_state") and p.get("blocked_actions_preserved") and p.get("non_claim_lock") for p in plans),
        "primary_lock": PRIMARY_LOCK,
        "non_claim_lock": NON_CLAIM_LOCK,
    }
    report["closure_hash"] = _hash(report)
    return report
