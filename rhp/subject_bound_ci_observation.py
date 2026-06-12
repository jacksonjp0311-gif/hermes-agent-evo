from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

INGEST_SCHEMA = "RHP-SUBJECT-BOUND-CI-OBSERVATION-INGEST-v0.1"
EXPECTED_SUBJECT_COMMIT = "ddb24363e2fac630e7527a2c9eab31e6df50db52"
EXPECTED_SOURCE = "github-connector"
ALLOWED_RESULT_STATES = ("resolved_green", "resolved_red", "unresolved_unknown", "unresolved_pending")


@dataclass(frozen=True)
class SubjectBoundCiIngestReport:
    ok: bool
    subject_ok: bool
    source_ok: bool
    connector_authority_ok: bool
    status_interpretation_ok: bool
    wound_closure_ok: bool
    result_state: str
    blocking_reasons: tuple[str, ...]


def classify_subject_bound_ci_observation(
    *,
    connector_observation: Mapping[str, Any],
    status_context_count: int,
    workflow_run_count: int,
) -> str:
    observed_status = connector_observation.get("observed_status")
    if observed_status == "success" and (status_context_count > 0 or workflow_run_count > 0):
        return "resolved_green"
    if observed_status in ("failure", "cancelled") and (status_context_count > 0 or workflow_run_count > 0):
        return "resolved_red"
    if observed_status == "pending":
        return "unresolved_pending"
    return "unresolved_unknown"


def validate_subject_bound_ci_ingest(
    *,
    connector_observation: Mapping[str, Any],
    expected_subject_commit: str = EXPECTED_SUBJECT_COMMIT,
    status_context_count: int = 0,
    workflow_run_count: int = 0,
    requested_wound_closure: bool = False,
) -> SubjectBoundCiIngestReport:
    reasons: list[str] = []

    subject_ok = connector_observation.get("subject_commit") == expected_subject_commit
    if not subject_ok:
        reasons.append("subject_commit_mismatch")

    source_ok = connector_observation.get("source") == EXPECTED_SOURCE
    if not source_ok:
        reasons.append("source_mismatch")

    connector_authority_ok = connector_observation.get("authority_granted") is False
    if not connector_authority_ok:
        reasons.append("connector_authority_grant_detected")

    result_state = classify_subject_bound_ci_observation(
        connector_observation=connector_observation,
        status_context_count=status_context_count,
        workflow_run_count=workflow_run_count,
    )
    status_interpretation_ok = result_state in ALLOWED_RESULT_STATES
    if not status_interpretation_ok:
        reasons.append("invalid_result_state")

    wound_closure_ok = not requested_wound_closure
    if requested_wound_closure:
        reasons.append("wound_closure_requested_during_observation_ingest")

    return SubjectBoundCiIngestReport(
        ok=not reasons,
        subject_ok=subject_ok,
        source_ok=source_ok,
        connector_authority_ok=connector_authority_ok,
        status_interpretation_ok=status_interpretation_ok,
        wound_closure_ok=wound_closure_ok,
        result_state=result_state,
        blocking_reasons=tuple(reasons),
    )


def report_to_dict(report: SubjectBoundCiIngestReport) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "subject_ok": report.subject_ok,
        "source_ok": report.source_ok,
        "connector_authority_ok": report.connector_authority_ok,
        "status_interpretation_ok": report.status_interpretation_ok,
        "wound_closure_ok": report.wound_closure_ok,
        "result_state": report.result_state,
        "blocking_reasons": list(report.blocking_reasons),
    }


def make_subject_bound_ci_observation_evidence(
    *,
    connector_observation: Mapping[str, Any],
    status_context_count: int,
    workflow_run_count: int,
    report: SubjectBoundCiIngestReport,
) -> dict[str, Any]:
    return {
        "schema": INGEST_SCHEMA,
        "subject_commit": connector_observation.get("subject_commit"),
        "source": connector_observation.get("source"),
        "observed_status": connector_observation.get("observed_status"),
        "status_context_count": status_context_count,
        "workflow_run_count": workflow_run_count,
        "result_state": report.result_state,
        "can_close_wound": False,
        "can_authorize_repair": False,
        "authority_granted": False,
        "report": report_to_dict(report),
        "non_claim_lock": "Subject-bound CI observation ingestion records evidence only; unknown is not pass and grants no authority.",
    }


def render_subject_bound_ci_ingest_panel(report: SubjectBoundCiIngestReport) -> str:
    status = "ingested" if report.ok else "blocked"
    reasons = ",".join(report.blocking_reasons) if report.blocking_reasons else "none"
    lines = [
        f"RHPCI-INGEST [GOLD] status={status}",
        "`- subject-bound CI observation ingestion",
        f"   +- subject-ok: {str(report.subject_ok).lower()}",
        f"   +- source-ok: {str(report.source_ok).lower()}",
        f"   +- connector-authority-ok: {str(report.connector_authority_ok).lower()}",
        f"   +- status-interpretation-ok: {str(report.status_interpretation_ok).lower()}",
        f"   +- wound-closure-ok: {str(report.wound_closure_ok).lower()}",
        f"   +- result-state: {report.result_state}",
        f"   +- blocking-reasons: {reasons}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
