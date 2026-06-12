from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

CANONICAL_TEMPLATE_NAME = "RHP_CANONICAL_ALL_ONE_TEMPLATE_SKELETON"
CANONICAL_TEMPLATE_VERSION = "v0.1"
CANONICAL_STAGE_ORDER: tuple[str, ...] = (
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

REQUIRED_TEMPLATE_SECTIONS: tuple[str, ...] = (
    "metadata",
    "entrypoint_filename_gate",
    "root_anchor",
    "bounded_residue_manager",
    "preauth_pull",
    "authorization_phrase",
    "runtime_trace_binding",
    "runtime_trace_drift_guard",
    "operation_helper",
    "doctor_loop",
    "self_learning_loop",
    "validation",
    "secret_shape_scan",
    "bounded_git_add",
    "commit_seal",
    "push_seal",
    "post_seal_residue",
    "return_root",
    "human_ui_summary",
    "non_claim_lock",
)

FORBIDDEN_TEMPLATE_ACTIONS: tuple[str, ...] = (
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
class TemplateEmitterReport:
    ok: bool
    stage_order_ok: bool
    sections_ok: bool
    generator_contract_ok: bool
    forbidden_actions_ok: bool
    authority_ok: bool
    blocking_reasons: tuple[str, ...]


def canonical_all_one_template_skeleton() -> str:
    lines = [
        "# RHP Canonical All-One Template Skeleton",
        "",
        "param()",
        "",
        "$ErrorActionPreference = 'Continue'",
        "$Operation = '<RHP-XXX.Y>'",
        "$ExpectedScriptName = '<EXACT_ALL_ONE_FILENAME.ps1>'",
        "$AuthPhrase = '<EXACT HUMAN AUTHORIZATION PHRASE>'",
        "$Root = Join-Path $env:USERPROFILE 'OneDrive\\\\Desktop\\\\hermes-agent-evo'",
        "$TempDir = Join-Path $env:TEMP '<RHP-XXX-Y-python-streams>'",
        "",
        "# STAGE 01 ENTRYPOINT-GATE: exact filename + file invocation only",
        "# STAGE 02 ROOT-ANCHOR: git rev-parse --show-toplevel must equal repo root",
        "# STAGE 03 RESIDUE-MANAGER: clean only bounded failed-run residue",
        "# STAGE 04 PREAUTH-PULL: git pull --rebase origin main before authorization",
        "# STAGE 05 RHPLOOP-RUNTIME: announce bounded operation contract",
        "# STAGE 06 HUMAN-AUTHORIZATION: exact phrase required before mutation",
        "# STAGE 07 RHPREADY: diagnostic evidence only",
        "# STAGE 08 OPERATION-START: generated temp Python helper writes bounded files",
        "# STAGE 09 RHPLOOP-DOCTOR: read/classify/propose only",
        "# STAGE 10 RHPLOOP-SELF-LEARNING: evidence-gated lesson only",
        "# STAGE 11 VALIDATION: py_compile, focused pytest, evidence API gate",
        "# STAGE 12 SECRET-SCAN: secret-shape scan only",
        "# STAGE 13 COMMIT-SEAL: bounded git add + commit",
        "# STAGE 14 PUSH-SEAL: pull --rebase + push",
        "# STAGE 15 RHPDROP: runtime-aware command summary",
        "# STAGE 16 RHPREFLECT: explain happened/meaning/remaining blocker/next",
        "# STAGE 17 POST-SEAL-RESIDUE: git status --short must be clean",
        "# STAGE 18 RETURN-ROOT: restore repo root",
        "# STAGE 19 HUMAN-UI-SUMMARY: final operator-readable state",
        "",
        "# NON-CLAIM LOCK:",
        "# This template grants no authority, closes no wound, repairs no code, mutates no dependencies,",
        "# reruns no CI, and does not claim current-operation CI green.",
    ]
    return "\n".join(lines) + "\n"


def template_metadata() -> dict[str, Any]:
    return {
        "template_name": CANONICAL_TEMPLATE_NAME,
        "template_version": CANONICAL_TEMPLATE_VERSION,
        "stage_count": len(CANONICAL_STAGE_ORDER),
        "stage_order": list(CANONICAL_STAGE_ORDER),
        "required_sections": list(REQUIRED_TEMPLATE_SECTIONS),
        "forbidden_actions": list(FORBIDDEN_TEMPLATE_ACTIONS),
        "emits_executable_without_human_fill": False,
        "grants_authority": False,
        "closes_wound": False,
        "repairs_code": False,
        "claims_current_operation_ci_green": False,
    }


def validate_template_emitter(generator_contract: Mapping[str, Any]) -> TemplateEmitterReport:
    reasons: list[str] = []
    metadata = template_metadata()

    stage_order_ok = tuple(metadata["stage_order"]) == CANONICAL_STAGE_ORDER and len(metadata["stage_order"]) == 19
    if not stage_order_ok:
        reasons.append("stage_order_mismatch")

    sections_ok = all(section in metadata["required_sections"] for section in REQUIRED_TEMPLATE_SECTIONS)
    if not sections_ok:
        reasons.append("required_template_section_missing")

    report = generator_contract.get("report", {})
    generator_contract_ok = (
        generator_contract.get("schema") == "RHP-ALL-ONE-GENERATOR-CONTRACT-v0.1"
        and report.get("ok") is True
        and report.get("stage_contract_ok") is True
        and report.get("rule_contract_ok") is True
        and report.get("forbidden_contract_ok") is True
        and report.get("trace_contract_ok") is True
        and report.get("authority_contract_ok") is True
    )
    if not generator_contract_ok:
        reasons.append("generator_contract_not_ok")

    forbidden_actions_ok = all(action in metadata["forbidden_actions"] for action in FORBIDDEN_TEMPLATE_ACTIONS)
    if not forbidden_actions_ok:
        reasons.append("forbidden_action_missing")

    authority_ok = (
        metadata["grants_authority"] is False
        and metadata["closes_wound"] is False
        and metadata["repairs_code"] is False
        and metadata["claims_current_operation_ci_green"] is False
    )
    if not authority_ok:
        reasons.append("authority_lock_mismatch")

    return TemplateEmitterReport(
        ok=not reasons,
        stage_order_ok=stage_order_ok,
        sections_ok=sections_ok,
        generator_contract_ok=generator_contract_ok,
        forbidden_actions_ok=forbidden_actions_ok,
        authority_ok=authority_ok,
        blocking_reasons=tuple(reasons),
    )


def report_to_dict(report: TemplateEmitterReport) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "stage_order_ok": report.stage_order_ok,
        "sections_ok": report.sections_ok,
        "generator_contract_ok": report.generator_contract_ok,
        "forbidden_actions_ok": report.forbidden_actions_ok,
        "authority_ok": report.authority_ok,
        "blocking_reasons": list(report.blocking_reasons),
    }


def emitter_contract_to_dict(report: TemplateEmitterReport) -> dict[str, Any]:
    return {
        "schema": "RHP-CANONICAL-ALL-ONE-TEMPLATE-EMITTER-v0.1",
        "metadata": template_metadata(),
        "report": report_to_dict(report),
        "skeleton_preview": canonical_all_one_template_skeleton(),
        "non_claim_lock": "The template emitter emits a bounded skeleton only; it grants no authority and executes no repair.",
    }


def render_template_emitter_panel(report: TemplateEmitterReport) -> str:
    status = "emitted" if report.ok else "blocked"
    reasons = ",".join(report.blocking_reasons) if report.blocking_reasons else "none"
    lines = [
        f"RHPTEMPLATE-EMIT [GOLD] status={status}",
        "`- canonical All-One template emitter",
        f"   +- stage-order-ok: {str(report.stage_order_ok).lower()}",
        f"   +- required-sections-ok: {str(report.sections_ok).lower()}",
        f"   +- generator-contract-ok: {str(report.generator_contract_ok).lower()}",
        f"   +- forbidden-actions-ok: {str(report.forbidden_actions_ok).lower()}",
        f"   +- authority-ok: {str(report.authority_ok).lower()}",
        f"   +- blocking-reasons: {reasons}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
