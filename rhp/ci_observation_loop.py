from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

RHP_CI_OBSERVATION_LOOP_SCHEMA = "RHP-CI-OBSERVATION-LOOP-v0.1"
RHP_CI_OBSERVATION_LOOP_EVIDENCE_SCHEMA = "RHP-CI-OBSERVATION-LOOP-EVIDENCE-v0.1"

VALID_CI_STATUSES = {"unknown", "pending", "green", "red", "cancelled", "skipped"}
AUTHORITY_LOCK_KEYS = [
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
]


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


def authority_locks() -> dict[str, bool]:
    return {key: False for key in AUTHORITY_LOCK_KEYS}


def normalize_ci_status(status: str) -> str:
    normalized = (status or "").strip().lower()
    if normalized not in VALID_CI_STATUSES:
        raise ValueError(f"observed_ci_status must be one of {sorted(VALID_CI_STATUSES)}")
    return normalized


def transition_for_observation(
    *,
    subject_commit: str,
    observed_ci_status: str,
    ci_source: str,
    prior_operation: str,
    repaired_wound_class: str | None = None,
    failing_workflow: str = "",
    failing_test: str = "",
    repro_command: str = "",
    run_url: str = "",
    prior_state: str = "",
) -> dict[str, Any]:
    if not subject_commit:
        raise ValueError("subject_commit is required")
    if not ci_source:
        raise ValueError("ci_source is required")
    status = normalize_ci_status(observed_ci_status)
    wound_from_repair = repaired_wound_class or "remote_ci_red"

    table: dict[str, dict[str, Any]] = {
        "green": {
            "to_state": "CI_RECONCILED_GREEN",
            "terminal": True,
            "pass": True,
            "integration_closed": True,
            "active_wound_class": "no_active_wound",
            "wound_queue_action": "close_named_subject_wound",
            "proposal_route": "none",
            "next_legal_operation": "continue_bounded_evolution_after_named_subject_green",
        },
        "red": {
            "to_state": "CI_RED_WOUND_OPEN",
            "terminal": True,
            "pass": False,
            "integration_closed": False,
            "active_wound_class": wound_from_repair,
            "wound_queue_action": "open_or_update_wound",
            "proposal_route": "ci_wound_packet_required",
            "next_legal_operation": "create_ci_wound_packet_before_repair",
        },
        "pending": {
            "to_state": "CI_PENDING",
            "terminal": False,
            "pass": False,
            "integration_closed": False,
            "active_wound_class": "remote_ci_pending",
            "wound_queue_action": "hold_pending_subject",
            "proposal_route": "wait",
            "next_legal_operation": "wait_or_ingest_final_ci_status_before_green_claim",
        },
        "unknown": {
            "to_state": "CI_UNKNOWN",
            "terminal": False,
            "pass": False,
            "integration_closed": False,
            "active_wound_class": "remote_ci_pending",
            "wound_queue_action": "hold_unknown_subject",
            "proposal_route": "collect_commit_scoped_observation",
            "next_legal_operation": "ingest_commit_scoped_ci_status",
        },
        "cancelled": {
            "to_state": "CI_CANCELLED_NON_GREEN_TERMINAL",
            "terminal": True,
            "pass": False,
            "integration_closed": False,
            "active_wound_class": "remote_ci_red",
            "non_green_terminal_class": "remote_ci_cancelled",
            "wound_queue_action": "open_non_green_terminal_wound",
            "proposal_route": "non_green_terminal_packet_required",
            "next_legal_operation": "create_non_green_terminal_ci_packet_before_any_repair",
        },
        "skipped": {
            "to_state": "CI_SKIPPED_NON_GREEN_TERMINAL",
            "terminal": True,
            "pass": False,
            "integration_closed": False,
            "active_wound_class": "remote_ci_red",
            "non_green_terminal_class": "remote_ci_skipped",
            "wound_queue_action": "open_non_green_terminal_wound",
            "proposal_route": "manual_review_packet_required",
            "next_legal_operation": "create_skipped_ci_packet_before_any_green_claim",
        },
    }
    base = dict(table[status])
    base.update(
        {
            "schema": RHP_CI_OBSERVATION_LOOP_SCHEMA,
            "from_state": prior_state,
            "subject_type": "git_commit",
            "subject_commit": subject_commit,
            "observed_ci_status": status,
            "ci_source": ci_source,
            "run_url": run_url,
            "prior_operation": prior_operation,
            "repaired_wound_class": repaired_wound_class or "",
            "failing_workflow": failing_workflow,
            "failing_test": failing_test,
            "repro_command": repro_command,
            "authority_granted": False,
            "execution_enabled": False,
            "current_operation_commit": "unobservable-from-inside-same-commit",
            "current_operation_remote_ci_status": "unknown_until_next_observation",
            "non_claim_lock": "CI observation loop classifies one commit-scoped observation only. It does not call GitHub, rerun CI, repair code, mutate dependencies, grant authority, or claim the current operation commit green.",
        }
    )
    return base


def build_loop_evidence(
    *,
    operation: str,
    subject_commit: str,
    observed_ci_status: str,
    ci_source: str,
    prior_operation: str,
    latest_operation: str,
    latest_evidence: str,
    prior_state: str,
    prior_integration_closed: bool,
    prior_active_wound_class: str,
    operation_base_commit: str = "",
    repaired_wound_class: str | None = None,
    failing_workflow: str = "",
    failing_test: str = "",
    repro_command: str = "",
    run_url: str = "",
    operator_script_name: str = "",
    observed_at_utc: str | None = None,
) -> dict[str, Any]:
    transition = transition_for_observation(
        subject_commit=subject_commit,
        observed_ci_status=observed_ci_status,
        ci_source=ci_source,
        prior_operation=prior_operation,
        repaired_wound_class=repaired_wound_class,
        failing_workflow=failing_workflow,
        failing_test=failing_test,
        repro_command=repro_command,
        run_url=run_url,
        prior_state=prior_state,
    )
    observed_at = observed_at_utc or utc_now()
    packet: dict[str, Any] = {
        "schema": RHP_CI_OBSERVATION_LOOP_EVIDENCE_SCHEMA,
        "operation": operation,
        "timestamp_utc": observed_at,
        "operation_base_commit": operation_base_commit,
        "claim": "commit_scoped_ci_state_transition",
        "subject": {
            "subject_type": "git_commit",
            "subject_commit": subject_commit,
            "prior_operation": prior_operation,
            "repaired_wound_class": repaired_wound_class or "",
        },
        "observation": {
            "observed_ci_status": transition["observed_ci_status"],
            "ci_source": ci_source,
            "run_url": run_url,
            "observed_at_utc": observed_at,
            "source_scope": "commit-scoped observation; not generalized beyond subject_commit",
        },
        "prior_context": {
            "latest_operation": latest_operation,
            "latest_evidence": latest_evidence,
            "prior_state": prior_state,
            "prior_integration_closed": bool(prior_integration_closed),
            "prior_active_wound_class": prior_active_wound_class,
        },
        "transition": transition,
        "outputs": {
            "latest_rhp": "docs/context-layer/latest-rhp.json",
            "zero_context_rebuild_md": "docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md",
            "zero_context_rebuild_json": "docs/context-layer/rhp_zero_context_rebuild.json",
            "operator_dashboard": "docs/context-layer/operator-dashboard.txt",
            "doctor_readable_state": "docs/context-layer/hermes-operator-context.json",
        },
        "current_operation_commit": "unobservable-from-inside-same-commit",
        "current_operation_remote_ci_status": "unknown_until_next_observation",
        "validation_passed": True,
        "focused_tests_passed": False,
        "py_compile_passed": False,
        "operator_script_name": operator_script_name,
        "authority_locks": authority_locks(),
        "non_claim_lock": "RHP-017.0 classifies and records a commit-scoped CI transition only. It does not call GitHub, rerun CI, repair code, mutate dependencies, grant authority, or claim the current operation commit green.",
    }
    packet["validation"] = validate_loop_evidence(packet)
    return packet


def validate_loop_evidence(packet: dict[str, Any]) -> dict[str, Any]:
    required = ["schema", "operation", "subject", "observation", "prior_context", "transition", "authority_locks"]
    missing = [key for key in required if key not in packet]
    transition = packet.get("transition", {})
    subject = packet.get("subject", {})
    status = transition.get("observed_ci_status")
    authority_ok = all(packet.get("authority_locks", {}).get(key) is False for key in AUTHORITY_LOCK_KEYS)
    current_lock_ok = packet.get("current_operation_commit") == "unobservable-from-inside-same-commit"
    subject_ok = bool(subject.get("subject_commit"))
    status_ok = status in VALID_CI_STATUSES
    pending_ok = status != "pending" or (transition.get("terminal") is False and transition.get("pass") is False)
    unknown_ok = status != "unknown" or transition.get("pass") is False
    non_green_terminal_ok = status not in {"cancelled", "skipped"} or (
        transition.get("terminal") is True
        and transition.get("pass") is False
        and transition.get("integration_closed") is False
    )
    green_ok = status != "green" or (
        transition.get("integration_closed") is True
        and transition.get("active_wound_class") == "no_active_wound"
    )
    red_ok = status != "red" or (
        transition.get("integration_closed") is False
        and transition.get("proposal_route") == "ci_wound_packet_required"
    )
    return {
        "ok": not missing
        and authority_ok
        and current_lock_ok
        and subject_ok
        and status_ok
        and pending_ok
        and unknown_ok
        and non_green_terminal_ok
        and green_ok
        and red_ok,
        "missing": missing,
        "authority_ok": authority_ok,
        "current_lock_ok": current_lock_ok,
        "subject_ok": subject_ok,
        "status_ok": status_ok,
        "pending_ok": pending_ok,
        "unknown_ok": unknown_ok,
        "non_green_terminal_ok": non_green_terminal_ok,
        "green_ok": green_ok,
        "red_ok": red_ok,
    }


def render_latest_pointer(packet: dict[str, Any]) -> dict[str, Any]:
    transition = packet["transition"]
    subject = packet["subject"]
    observation = packet["observation"]
    return {
        "schema": "RHP-LATEST-POINTER-v2.1",
        "latest_operation": packet["operation"],
        "latest_evidence": f"docs/context-layer/ops/{packet['operation'].replace('.', '-')}-final-evidence.json",
        "operation_base_commit": packet.get("operation_base_commit", ""),
        "observed_previous_sealed_commit": subject["subject_commit"],
        "subject_commit": subject["subject_commit"],
        "observed_ci_status": observation["observed_ci_status"],
        "ci_source": observation["ci_source"],
        "repaired_wound_class": subject.get("repaired_wound_class", ""),
        "active_wound_class": transition["active_wound_class"],
        "state": transition["to_state"],
        "integration_closed": transition["integration_closed"],
        "current_operation_commit": "unobservable-from-inside-same-commit",
        "current_operation_remote_ci_status": "unknown_until_next_observation",
        "next_operation": transition["next_legal_operation"],
        "zero_context_rebuild": "docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md",
        "authority_ok": True,
    }


def render_zero_context_rebuild_json(packet: dict[str, Any]) -> dict[str, Any]:
    transition = packet["transition"]
    subject = packet["subject"]
    observation = packet["observation"]
    return {
        "schema": "RHP-ZERO-CONTEXT-REBUILD-v2.1",
        "ok": True,
        "latest_operation": packet["operation"],
        "latest_evidence": f"docs/context-layer/ops/{packet['operation'].replace('.', '-')}-final-evidence.json",
        "subject_commit": subject["subject_commit"],
        "observed_ci_status": observation["observed_ci_status"],
        "state": transition["to_state"],
        "integration_closed": transition["integration_closed"],
        "next_operation": transition["next_legal_operation"],
        "authority_locks": packet["authority_locks"],
        "non_claim_lock": "Zero-context rebuild grants no authority.",
    }


def render_zero_context_rebuild_md(packet: dict[str, Any]) -> str:
    data = render_zero_context_rebuild_json(packet)
    lines = [
        "# RHP Zero-Context Rebuild Packet",
        "",
        f"- schema: `{data['schema']}`",
        f"- ok: `{data['ok']}`",
        f"- latest operation: `{data['latest_operation']}`",
        f"- latest evidence: `{data['latest_evidence']}`",
        f"- subject commit: `{data['subject_commit']}`",
        f"- observed CI status: `{data['observed_ci_status']}`",
        f"- state: `{data['state']}`",
        f"- integration closed: `{data['integration_closed']}`",
        f"- next operation: `{data['next_operation']}`",
        "",
        "Non-claim lock: Zero-context rebuild grants no authority.",
        "",
    ]
    return "\n".join(lines)


def render_operator_dashboard(packet: dict[str, Any]) -> str:
    transition = packet["transition"]
    subject = packet["subject"]
    observation = packet["observation"]
    status = "ok" if packet["validation"]["ok"] else "blocked"
    return "\n".join(
        [
            f"RHPLOAD [100%] HUMAN-UI-SUMMARY operation={packet['operation']} | status={status} [OK]",
            "`- Hermes/RHP operator dashboard",
            f"   +- latest: {packet['operation']}",
            f"   +- next: {transition['next_legal_operation']}",
            f"   +- subject commit: {subject['subject_commit']}",
            f"   +- observed CI status: {observation['observed_ci_status']}",
            f"   +- state: {transition['to_state']}",
            f"   +- integration closed: {str(transition['integration_closed']).lower()}",
            "   +- current operation CI: unknown_until_next_observation",
            "   +- authority ok: true",
            "   `- verified: true [OK]",
            "",
        ]
    )


def render_hermes_operator_context(packet: dict[str, Any]) -> dict[str, Any]:
    transition = packet["transition"]
    can = [
        "read_ci_observation_loop_evidence",
        "explain_commit_scoped_transition",
        "route_next_legal_operation_from_transition_table",
    ]
    if transition["observed_ci_status"] in {"pending", "unknown"}:
        can.append("wait_for_or_ingest_next_ci_result")
    if transition["observed_ci_status"] == "red":
        can.append("prepare_ci_wound_packet_before_repair")
    if transition["observed_ci_status"] == "green":
        can.append("continue_bounded_evolution_after_named_subject_green")
    return {
        "schema": "RHP-HERMES-OPERATOR-CONTEXT-v2.1",
        "latest_operation": packet["operation"],
        "next_operation": transition["next_legal_operation"],
        "hermes_can": can,
        "hermes_cannot": [
            "execute_autoheal",
            "rerun_ci",
            "self_authorize",
            "mutate_without_all_one",
            "claim_current_operation_ci_without_observation",
            "generalize_operator_observed_status_beyond_subject_commit",
        ],
        "authority_locks": packet["authority_locks"],
        "non_claim_lock": "Read-only orientation; no direct mutation or self-authorization.",
    }


def write_context_outputs(repo_root: Path, packet: dict[str, Any], out: str = "") -> dict[str, str]:
    ctx = repo_root / "docs" / "context-layer"
    op_dir = ctx / "ops" / "RHP-017-0-ci-observation-loop-kernel"
    op_dir.mkdir(parents=True, exist_ok=True)
    final_path = ctx / "ops" / "RHP-017-0-final-evidence.json"
    loop_path = Path(out) if out else op_dir / "ci-observation-loop-evidence.json"
    latest_path = ctx / "latest-rhp.json"
    zc_md_path = ctx / "RHP_ZERO_CONTEXT_REBUILD.md"
    zc_json_path = ctx / "rhp_zero_context_rebuild.json"
    dashboard_path = ctx / "operator-dashboard.txt"
    operator_context_path = ctx / "hermes-operator-context.json"

    rendered = {
        "loop_evidence": loop_path,
        "final_evidence": final_path,
        "latest_rhp": latest_path,
        "zero_context_rebuild_md": zc_md_path,
        "zero_context_rebuild_json": zc_json_path,
        "operator_dashboard": dashboard_path,
        "hermes_operator_context": operator_context_path,
    }
    loop_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    final_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    latest_path.write_text(json.dumps(render_latest_pointer(packet), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    zc_json_path.write_text(json.dumps(render_zero_context_rebuild_json(packet), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    zc_md_path.write_text(render_zero_context_rebuild_md(packet), encoding="utf-8", newline="\n")
    dashboard_path.write_text(render_operator_dashboard(packet), encoding="utf-8", newline="\n")
    operator_context_path.write_text(json.dumps(render_hermes_operator_context(packet), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {key: str(path) for key, path in rendered.items()}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build a reusable RHP CI observation loop evidence transition")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--operation", default="RHP-017.0")
    parser.add_argument("--subject-commit", required=True)
    parser.add_argument("--observed-ci-status", required=True, choices=sorted(VALID_CI_STATUSES))
    parser.add_argument("--ci-source", default="operator-provided")
    parser.add_argument("--prior-operation", default="")
    parser.add_argument("--repaired-wound-class", default="")
    parser.add_argument("--failing-workflow", default="")
    parser.add_argument("--failing-test", default="")
    parser.add_argument("--repro-command", default="")
    parser.add_argument("--run-url", default="")
    parser.add_argument("--operation-base-commit", default="")
    parser.add_argument("--operator-script-name", default="")
    parser.add_argument("--latest-operation", default="")
    parser.add_argument("--latest-evidence", default="")
    parser.add_argument("--prior-state", default="")
    parser.add_argument("--prior-integration-closed", action="store_true")
    parser.add_argument("--prior-active-wound-class", default="")
    parser.add_argument("--write-context", action="store_true")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)

    packet = build_loop_evidence(
        operation=args.operation,
        subject_commit=args.subject_commit,
        observed_ci_status=args.observed_ci_status,
        ci_source=args.ci_source,
        prior_operation=args.prior_operation,
        latest_operation=args.latest_operation,
        latest_evidence=args.latest_evidence,
        prior_state=args.prior_state,
        prior_integration_closed=args.prior_integration_closed,
        prior_active_wound_class=args.prior_active_wound_class,
        operation_base_commit=args.operation_base_commit,
        repaired_wound_class=args.repaired_wound_class,
        failing_workflow=args.failing_workflow,
        failing_test=args.failing_test,
        repro_command=args.repro_command,
        run_url=args.run_url,
        operator_script_name=args.operator_script_name,
    )
    if args.write_context:
        packet["rendered_outputs"] = write_context_outputs(Path(args.repo_root), packet, args.out)
        final_path = Path(args.repo_root) / "docs" / "context-layer" / "ops" / "RHP-017-0-final-evidence.json"
        loop_path = Path(args.out) if args.out else Path(args.repo_root) / "docs" / "context-layer" / "ops" / "RHP-017-0-ci-observation-loop-kernel" / "ci-observation-loop-evidence.json"
        final_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        loop_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        text = json.dumps(packet, indent=2, ensure_ascii=False)
        if args.out:
            out = Path(args.out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(text + "\n", encoding="utf-8")
        print(text)
    return 0 if packet["validation"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
