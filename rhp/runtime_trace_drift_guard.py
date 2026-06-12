from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

EXPECTED_OPERATION = "RHP-020.1"
EXPECTED_STATE = "EXACT_RUNTIME_SCRIPT_TRACE_MAP_ALIGNED_SUBJECT_UNRESOLVED"
EXPECTED_STAGE_COUNT = 19
EXPECTED_TRACE_MODULE = "rhp/runtime_script_trace_map.py"
EXPECTED_TRACE_EVIDENCE = "docs/context-layer/ops/RHP-020-1-exact-runtime-script-trace-map/runtime-script-trace-map.json"
EXPECTED_TRACE_PANEL = "RHPSCRIPT-TRACE [GOLD]"
EXPECTED_ACTIVE_WOUND = "readiness_gate_install"
EXPECTED_SUBJECT_COMMIT = "ddb24363e2fac630e7527a2c9eab31e6df50db52"
EXPECTED_NEXT = "operator_rerun_or_ingest_replacement_ci_before_repair"


@dataclass(frozen=True)
class RuntimeTraceDriftReport:
    ok: bool
    latest_ok: bool
    final_evidence_ok: bool
    trace_evidence_ok: bool
    module_ok: bool
    readme_ok: bool
    agents_ok: bool
    stage_count_ok: bool
    authority_ok: bool
    blocking_reasons: tuple[str, ...]


def _authority_locks_false(data: Mapping[str, Any]) -> bool:
    locks = data.get("authority_locks")
    if not isinstance(locks, Mapping):
        return data.get("authority_ok") is True
    required = (
        "provider_call_executed",
        "model_call_executed",
        "tool_use_executed",
        "cms_runtime_execution",
        "cms_write",
        "memory_write",
        "memory_promotion",
        "api_write",
        "dependency_mutation_committed",
        "external_ingestion",
        "autonomous_authority",
        "self_authorization",
    )
    return all(locks.get(key) is False for key in required)


def validate_runtime_trace_drift(
    *,
    latest_rhp: Mapping[str, Any],
    final_evidence: Mapping[str, Any],
    trace_evidence: Mapping[str, Any],
    module_trace: Mapping[str, Any],
    readme_text: str,
    agents_text: str,
) -> RuntimeTraceDriftReport:
    reasons: list[str] = []

    latest_ok = (
        latest_rhp.get("latest_operation") == EXPECTED_OPERATION
        and latest_rhp.get("state") == EXPECTED_STATE
        and latest_rhp.get("active_wound_class") == EXPECTED_ACTIVE_WOUND
        and latest_rhp.get("subject_commit") == EXPECTED_SUBJECT_COMMIT
        and latest_rhp.get("observed_ci_status") == "unknown"
        and latest_rhp.get("integration_closed") is False
        and latest_rhp.get("next_operation") == EXPECTED_NEXT
    )
    if not latest_ok:
        reasons.append("latest_rhp_mismatch")

    final_evidence_ok = (
        final_evidence.get("operation") == EXPECTED_OPERATION
        and final_evidence.get("state_after_alignment") == EXPECTED_STATE
        and final_evidence.get("runtime_script_trace_map_module") == EXPECTED_TRACE_MODULE
        and final_evidence.get("runtime_script_trace_map_evidence") == EXPECTED_TRACE_EVIDENCE
        and final_evidence.get("active_wound_preserved") is True
        and final_evidence.get("active_subject_closed") is False
        and final_evidence.get("repair_execution_enabled") is False
        and final_evidence.get("current_operation_remote_ci_status") == "unknown_until_next_observation"
    )
    if not final_evidence_ok:
        reasons.append("final_evidence_mismatch")

    trace_evidence_ok = (
        trace_evidence.get("operation") == EXPECTED_OPERATION
        and trace_evidence.get("installed_module") == EXPECTED_TRACE_MODULE
        and trace_evidence.get("stage_count") == EXPECTED_STAGE_COUNT
        and trace_evidence.get("exact_script_bound") is True
        and isinstance(trace_evidence.get("stages"), list)
        and len(trace_evidence.get("stages", [])) == EXPECTED_STAGE_COUNT
    )
    if not trace_evidence_ok:
        reasons.append("trace_evidence_mismatch")

    module_ok = (
        module_trace.get("operation") == EXPECTED_OPERATION
        and module_trace.get("installed_module") == EXPECTED_TRACE_MODULE
        and module_trace.get("stage_count") == EXPECTED_STAGE_COUNT
        and module_trace.get("exact_script_bound") is True
        and module_trace.get("stage_order") == trace_evidence.get("stage_order")
    )
    if not module_ok:
        reasons.append("module_trace_mismatch")

    readme_ok = (
        "<!-- RHP_EXACT_RUNTIME_SCRIPT_TRACE_MAP_START -->" in readme_text
        and "<!-- RHP_EXACT_RUNTIME_SCRIPT_TRACE_MAP_END -->" in readme_text
        and EXPECTED_TRACE_PANEL in readme_text
        and EXPECTED_TRACE_MODULE in readme_text
        and EXPECTED_TRACE_EVIDENCE in readme_text
    )
    if not readme_ok:
        reasons.append("readme_trace_block_mismatch")

    agents_ok = (
        "<!-- HERMES_AGENT_EXACT_RUNTIME_SCRIPT_TRACE_MAP_START -->" in agents_text
        and "<!-- HERMES_AGENT_EXACT_RUNTIME_SCRIPT_TRACE_MAP_END -->" in agents_text
        and "exact stage-to-script trace" in agents_text
        and "script-trace preservation grants no authority" in agents_text
    )
    if not agents_ok:
        reasons.append("agents_trace_rule_mismatch")

    stage_count_ok = (
        trace_evidence.get("stage_count") == EXPECTED_STAGE_COUNT
        and module_trace.get("stage_count") == EXPECTED_STAGE_COUNT
        and len(trace_evidence.get("stage_order", [])) == EXPECTED_STAGE_COUNT
        and len(module_trace.get("stage_order", [])) == EXPECTED_STAGE_COUNT
    )
    if not stage_count_ok:
        reasons.append("stage_count_mismatch")

    authority_ok = (
        latest_rhp.get("authority_ok") is True
        and _authority_locks_false(final_evidence)
    )
    if not authority_ok:
        reasons.append("authority_lock_mismatch")

    return RuntimeTraceDriftReport(
        ok=not reasons,
        latest_ok=latest_ok,
        final_evidence_ok=final_evidence_ok,
        trace_evidence_ok=trace_evidence_ok,
        module_ok=module_ok,
        readme_ok=readme_ok,
        agents_ok=agents_ok,
        stage_count_ok=stage_count_ok,
        authority_ok=authority_ok,
        blocking_reasons=tuple(reasons),
    )


def report_to_dict(report: RuntimeTraceDriftReport) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "latest_ok": report.latest_ok,
        "final_evidence_ok": report.final_evidence_ok,
        "trace_evidence_ok": report.trace_evidence_ok,
        "module_ok": report.module_ok,
        "readme_ok": report.readme_ok,
        "agents_ok": report.agents_ok,
        "stage_count_ok": report.stage_count_ok,
        "authority_ok": report.authority_ok,
        "blocking_reasons": list(report.blocking_reasons),
    }


def render_runtime_trace_drift_guard_panel(report: RuntimeTraceDriftReport) -> str:
    status = "aligned" if report.ok else "blocked"
    reasons = ",".join(report.blocking_reasons) if report.blocking_reasons else "none"
    lines = [
        f"RHPTRACE-GUARD [GOLD] status={status}",
        "`- runtime trace drift guard",
        f"   +- latest-ok: {str(report.latest_ok).lower()}",
        f"   +- final-evidence-ok: {str(report.final_evidence_ok).lower()}",
        f"   +- trace-evidence-ok: {str(report.trace_evidence_ok).lower()}",
        f"   +- module-ok: {str(report.module_ok).lower()}",
        f"   +- readme-ok: {str(report.readme_ok).lower()}",
        f"   +- agents-ok: {str(report.agents_ok).lower()}",
        f"   +- stage-count-ok: {str(report.stage_count_ok).lower()}",
        f"   +- authority-ok: {str(report.authority_ok).lower()}",
        f"   +- blocking-reasons: {reasons}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
