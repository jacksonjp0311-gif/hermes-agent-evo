from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

REQUIRED_CANONICAL_STAGES: tuple[str, ...] = (
    "ENTRYPOINT-GATE",
    "ROOT-ANCHOR",
    "RESIDUE-MANAGER",
    "PREAUTH-PULL",
    "RHPLOOP-RUNTIME",
    "HUMAN-AUTHORIZATION",
    "RHPREADY",
    "OPERATION-START",
    "RHPLOOP-DOCTOR",
    "RHPLOOP-SELF-LEARNING",
    "VALIDATION",
    "SECRET-SCAN",
    "COMMIT-SEAL",
    "PUSH-SEAL",
    "RHPDROP",
    "RHPREFLECT",
    "POST-SEAL-RESIDUE",
    "RETURN-ROOT",
    "HUMAN-UI-SUMMARY",
)

REQUIRED_ALL_ONE_RULES: tuple[str, ...] = (
    "exact_filename_gate",
    "root_anchor",
    "bounded_residue_manager",
    "preauth_pull_rebase",
    "exact_human_authorization_phrase",
    "generated_temp_python_helper",
    "repo_module_install",
    "focused_tests_install",
    "readme_agents_update",
    "runtime_trace_map_update",
    "runtime_trace_drift_guard",
    "py_compile",
    "focused_pytest",
    "evidence_api_compatibility_gate",
    "secret_shape_scan",
    "bounded_git_add",
    "commit_seal",
    "post_commit_pull_rebase",
    "push_seal",
    "post_seal_residue_check",
    "return_root",
    "human_ui_summary",
)

FORBIDDEN_CAPABILITIES: tuple[str, ...] = (
    "repair_code_without_evidence",
    "rerun_ci_without_authority",
    "close_active_wound",
    "claim_current_operation_ci_green",
    "mutate_dependencies",
    "grant_provider_authority",
    "grant_model_authority",
    "grant_tool_authority",
    "grant_cms_write_authority",
    "grant_memory_promotion_authority",
    "grant_api_write_authority",
    "grant_autonomous_authority",
    "self_authorize",
)


@dataclass(frozen=True)
class AllOneGeneratorContractReport:
    ok: bool
    stage_contract_ok: bool
    rule_contract_ok: bool
    forbidden_contract_ok: bool
    trace_contract_ok: bool
    authority_contract_ok: bool
    blocking_reasons: tuple[str, ...]


def validate_all_one_generator_contract(
    *,
    trace_map: Mapping[str, Any],
    declared_rules: tuple[str, ...] = REQUIRED_ALL_ONE_RULES,
    forbidden_capabilities: tuple[str, ...] = FORBIDDEN_CAPABILITIES,
) -> AllOneGeneratorContractReport:
    reasons: list[str] = []

    stage_order = tuple(trace_map.get("stage_order", ()))
    stage_contract_ok = stage_order == REQUIRED_CANONICAL_STAGES
    if not stage_contract_ok:
        reasons.append("canonical_stage_order_mismatch")

    rule_contract_ok = all(rule in declared_rules for rule in REQUIRED_ALL_ONE_RULES)
    if not rule_contract_ok:
        reasons.append("required_generation_rule_missing")

    forbidden_contract_ok = all(item in forbidden_capabilities for item in FORBIDDEN_CAPABILITIES)
    if not forbidden_contract_ok:
        reasons.append("forbidden_capability_missing")

    trace_contract_ok = (
        trace_map.get("stage_count") == 19
        and trace_map.get("exact_script_bound") is True
        and trace_map.get("installed_module") == "rhp/runtime_script_trace_map.py"
        and trace_map.get("evidence_location") == "docs/context-layer/ops/RHP-020-1-exact-runtime-script-trace-map/"
    )
    if not trace_contract_ok:
        reasons.append("trace_contract_mismatch")

    authority_contract_ok = True
    for stage in trace_map.get("stages", []):
        if stage.get("grants_authority") is not False:
            authority_contract_ok = False
        if stage.get("closes_wound") is not False:
            authority_contract_ok = False
        if stage.get("repairs_code") is not False:
            authority_contract_ok = False
        if stage.get("claims_current_operation_ci_green") is not False:
            authority_contract_ok = False
    if not authority_contract_ok:
        reasons.append("stage_authority_lock_mismatch")

    return AllOneGeneratorContractReport(
        ok=not reasons,
        stage_contract_ok=stage_contract_ok,
        rule_contract_ok=rule_contract_ok,
        forbidden_contract_ok=forbidden_contract_ok,
        trace_contract_ok=trace_contract_ok,
        authority_contract_ok=authority_contract_ok,
        blocking_reasons=tuple(reasons),
    )


def report_to_dict(report: AllOneGeneratorContractReport) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "stage_contract_ok": report.stage_contract_ok,
        "rule_contract_ok": report.rule_contract_ok,
        "forbidden_contract_ok": report.forbidden_contract_ok,
        "trace_contract_ok": report.trace_contract_ok,
        "authority_contract_ok": report.authority_contract_ok,
        "blocking_reasons": list(report.blocking_reasons),
    }


def generator_contract_to_dict(report: AllOneGeneratorContractReport) -> dict[str, Any]:
    return {
        "schema": "RHP-ALL-ONE-GENERATOR-CONTRACT-v0.1",
        "required_canonical_stages": list(REQUIRED_CANONICAL_STAGES),
        "required_all_one_rules": list(REQUIRED_ALL_ONE_RULES),
        "forbidden_capabilities": list(FORBIDDEN_CAPABILITIES),
        "report": report_to_dict(report),
        "non_claim_lock": "The generator contract grants no authority and does not generate or execute a repair.",
    }


def render_all_one_generator_contract_panel(report: AllOneGeneratorContractReport) -> str:
    status = "accepted" if report.ok else "blocked"
    reasons = ",".join(report.blocking_reasons) if report.blocking_reasons else "none"
    lines = [
        f"RHPGEN-CONTRACT [GOLD] status={status}",
        "`- All-One generator contract",
        f"   +- canonical-stage-order-ok: {str(report.stage_contract_ok).lower()}",
        f"   +- generation-rules-ok: {str(report.rule_contract_ok).lower()}",
        f"   +- forbidden-capabilities-ok: {str(report.forbidden_contract_ok).lower()}",
        f"   +- runtime-trace-contract-ok: {str(report.trace_contract_ok).lower()}",
        f"   +- authority-contract-ok: {str(report.authority_contract_ok).lower()}",
        f"   +- blocking-reasons: {reasons}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
