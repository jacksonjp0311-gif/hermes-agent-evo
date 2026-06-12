from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

EXPECTED_SUBJECT_COMMIT = "ddb24363e2fac630e7527a2c9eab31e6df50db52"
GATE_SCHEMA = "RHP-REPLACEMENT-GREEN-OBSERVATION-GATE-v0.1"


@dataclass(frozen=True)
class ReplacementGreenObservationGateReport:
    ok: bool
    subject_ok: bool
    source_ok: bool
    status_ok: bool
    evidence_surface_ok: bool
    authority_ok: bool
    no_closure_inside_gate_ok: bool
    eligible_for_future_closure: bool
    blocking_reasons: tuple[str, ...]


def validate_replacement_green_observation(
    observation: Mapping[str, Any],
    *,
    expected_subject_commit: str = EXPECTED_SUBJECT_COMMIT,
    close_now: bool = False,
) -> ReplacementGreenObservationGateReport:
    reasons: list[str] = []

    subject_ok = observation.get("subject_commit") == expected_subject_commit
    if not subject_ok:
        reasons.append("subject_commit_mismatch")

    source_ok = observation.get("source") == "github-connector"
    if not source_ok:
        reasons.append("source_mismatch")

    status_ok = observation.get("observed_status") == "success"
    if not status_ok:
        reasons.append("observed_status_not_success")

    status_context_count = int(observation.get("status_context_count", 0) or 0)
    workflow_run_count = int(observation.get("workflow_run_count", 0) or 0)
    evidence_surface_ok = status_context_count > 0 or workflow_run_count > 0
    if not evidence_surface_ok:
        reasons.append("no_status_context_or_workflow_run_surface")

    authority_ok = observation.get("authority_granted") is False
    if not authority_ok:
        reasons.append("authority_grant_detected")

    no_closure_inside_gate_ok = close_now is False
    if not no_closure_inside_gate_ok:
        reasons.append("closure_attempted_inside_green_observation_gate")

    eligible_for_future_closure = (
        subject_ok
        and source_ok
        and status_ok
        and evidence_surface_ok
        and authority_ok
        and no_closure_inside_gate_ok
    )

    return ReplacementGreenObservationGateReport(
        ok=not reasons,
        subject_ok=subject_ok,
        source_ok=source_ok,
        status_ok=status_ok,
        evidence_surface_ok=evidence_surface_ok,
        authority_ok=authority_ok,
        no_closure_inside_gate_ok=no_closure_inside_gate_ok,
        eligible_for_future_closure=eligible_for_future_closure,
        blocking_reasons=tuple(reasons),
    )


def make_unresolved_gate_baseline() -> dict[str, Any]:
    return {
        "schema": GATE_SCHEMA,
        "subject_commit": EXPECTED_SUBJECT_COMMIT,
        "gate_state": "installed_waiting_for_replacement_green_observation",
        "requires_observed_status": "success",
        "requires_status_context_or_workflow_run": True,
        "close_wound_inside_gate": False,
        "authority_granted": False,
        "non_claim_lock": "The replacement green observation gate validates future evidence eligibility only; it does not close wounds or authorize repair.",
    }


def report_to_dict(report: ReplacementGreenObservationGateReport) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "subject_ok": report.subject_ok,
        "source_ok": report.source_ok,
        "status_ok": report.status_ok,
        "evidence_surface_ok": report.evidence_surface_ok,
        "authority_ok": report.authority_ok,
        "no_closure_inside_gate_ok": report.no_closure_inside_gate_ok,
        "eligible_for_future_closure": report.eligible_for_future_closure,
        "blocking_reasons": list(report.blocking_reasons),
    }


def render_replacement_green_gate_panel(report: ReplacementGreenObservationGateReport) -> str:
    status = "eligible" if report.eligible_for_future_closure else "waiting"
    reasons = ",".join(report.blocking_reasons) if report.blocking_reasons else "none"
    return "\n".join(
        [
            f"RHPGREEN-GATE [GOLD] status={status}",
            "`- replacement green observation gate",
            f"   +- subject-ok: {str(report.subject_ok).lower()}",
            f"   +- source-ok: {str(report.source_ok).lower()}",
            f"   +- status-ok: {str(report.status_ok).lower()}",
            f"   +- evidence-surface-ok: {str(report.evidence_surface_ok).lower()}",
            f"   +- authority-ok: {str(report.authority_ok).lower()}",
            f"   +- no-closure-inside-gate-ok: {str(report.no_closure_inside_gate_ok).lower()}",
            f"   +- eligible-for-future-closure: {str(report.eligible_for_future_closure).lower()}",
            f"   +- blocking-reasons: {reasons}",
            "   `- authority: no grant [LOCKED]",
        ]
    )
