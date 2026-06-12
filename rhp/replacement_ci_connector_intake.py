from __future__ import annotations

from dataclasses import dataclass
from typing import Any

SUBJECT_COMMIT = "ddb24363e2fac630e7527a2c9eab31e6df50db52"


@dataclass(frozen=True)
class ConnectorCIIntakeDecision:
    subject_commit: str
    combined_status_count: int
    workflow_run_count: int
    connector_observed_status: str
    source_scope: str
    subject_scoped: bool
    replacement_ci_established: bool
    wound_closure_allowed_next: bool
    failed_log_ingestion_required: bool
    repair_allowed_next: bool
    state_after_intake: str
    next_operation: str
    classification: str


def classify_connector_ci_intake(
    *,
    subject_commit: str,
    combined_status_count: int,
    workflow_run_count: int,
    connector_observed_status: str,
) -> ConnectorCIIntakeDecision:
    status = connector_observed_status.strip().lower()
    if status not in {"green", "red", "pending", "unknown"}:
        status = "unknown"

    subject_scoped = subject_commit == SUBJECT_COMMIT
    has_connector_surface = combined_status_count > 0 or workflow_run_count > 0

    if subject_scoped and has_connector_surface and status == "green":
        classification = "connector_subject_green_replacement_ci_intake"
        state = "REPLACEMENT_CI_CONNECTOR_INTAKE_GREEN_CLOSURE_READY"
        next_operation = "close_active_subject_wound_after_subject_scoped_green_ci"
        established = True
        closure_next = True
        logs_required = False
    elif subject_scoped and has_connector_surface and status == "red":
        classification = "connector_subject_red_replacement_ci_logs_required"
        state = "REPLACEMENT_CI_CONNECTOR_INTAKE_RED_LOGS_REQUIRED"
        next_operation = "ingest_failed_replacement_ci_logs_before_repair"
        established = True
        closure_next = False
        logs_required = True
    elif subject_scoped and has_connector_surface and status == "pending":
        classification = "connector_subject_pending_replacement_ci"
        state = "REPLACEMENT_CI_CONNECTOR_INTAKE_PENDING"
        next_operation = "wait_or_ingest_final_replacement_ci_result"
        established = True
        closure_next = False
        logs_required = False
    else:
        classification = "connector_replacement_ci_evidence_not_established"
        state = "REPLACEMENT_CI_CONNECTOR_INTAKE_UNRESOLVED"
        next_operation = "operator_rerun_or_ingest_replacement_ci_before_repair"
        established = False
        closure_next = False
        logs_required = False

    return ConnectorCIIntakeDecision(
        subject_commit=subject_commit,
        combined_status_count=combined_status_count,
        workflow_run_count=workflow_run_count,
        connector_observed_status=status,
        source_scope="github_connector_subject_commit",
        subject_scoped=subject_scoped,
        replacement_ci_established=established,
        wound_closure_allowed_next=closure_next,
        failed_log_ingestion_required=logs_required,
        repair_allowed_next=False,
        state_after_intake=state,
        next_operation=next_operation,
        classification=classification,
    )


def decision_to_dict(decision: ConnectorCIIntakeDecision) -> dict[str, Any]:
    return {
        "subject_commit": decision.subject_commit,
        "combined_status_count": decision.combined_status_count,
        "workflow_run_count": decision.workflow_run_count,
        "connector_observed_status": decision.connector_observed_status,
        "source_scope": decision.source_scope,
        "subject_scoped": decision.subject_scoped,
        "replacement_ci_established": decision.replacement_ci_established,
        "wound_closure_allowed_next": decision.wound_closure_allowed_next,
        "failed_log_ingestion_required": decision.failed_log_ingestion_required,
        "repair_allowed_next": decision.repair_allowed_next,
        "state_after_intake": decision.state_after_intake,
        "next_operation": decision.next_operation,
        "classification": decision.classification,
    }


def render_connector_intake_panel(decision: ConnectorCIIntakeDecision) -> str:
    status = "accepted" if decision.replacement_ci_established else "unresolved"
    lines = [
        f"RHPCI-CONNECTOR [GOLD] status={status}",
        "`- GitHub connector CI evidence intake",
        f"   +- subject-commit: {decision.subject_commit}",
        f"   +- combined-status-count: {decision.combined_status_count}",
        f"   +- workflow-run-count: {decision.workflow_run_count}",
        f"   +- connector-observed-status: {decision.connector_observed_status}",
        f"   +- source-scope: {decision.source_scope}",
        f"   +- subject-scoped: {str(decision.subject_scoped).lower()}",
        f"   +- replacement-ci-established: {str(decision.replacement_ci_established).lower()}",
        f"   +- wound-closure-allowed-next: {str(decision.wound_closure_allowed_next).lower()}",
        f"   +- repair-allowed-next: {str(decision.repair_allowed_next).lower()}",
        f"   +- classification: {decision.classification}",
        f"   +- next: {decision.next_operation}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
