from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

VALID_REPLACEMENT_CI_STATUSES = ("green", "red", "pending", "unknown")
SUBJECT_COMMIT = "ddb24363e2fac630e7527a2c9eab31e6df50db52"


@dataclass(frozen=True)
class ReplacementCIObservation:
    subject_commit: str
    observed_status: str
    source: str
    source_scope: str
    evidence_note: str
    subject_scoped: bool
    replacement_ci_established: bool
    wound_closure_allowed_next: bool
    repair_allowed_next: bool
    next_operation: str
    classification: str


def normalize_status(value: str) -> str:
    normalized = value.strip().lower()
    if normalized in VALID_REPLACEMENT_CI_STATUSES:
        return normalized
    return "unknown"


def classify_replacement_ci_observation(
    *,
    subject_commit: str,
    observed_status: str,
    source: str,
    source_scope: str,
    evidence_note: str,
) -> ReplacementCIObservation:
    status = normalize_status(observed_status)
    scoped = subject_commit == SUBJECT_COMMIT and source_scope.strip().lower() == "subject_commit"
    replacement_established = scoped and status in {"green", "red", "pending"}
    green_subject = scoped and status == "green"
    red_subject = scoped and status == "red"
    pending_subject = scoped and status == "pending"

    if green_subject:
        next_operation = "close_active_subject_wound_after_subject_scoped_green_ci"
        classification = "replacement_ci_subject_green_ready_for_wound_closure"
    elif red_subject:
        next_operation = "ingest_failed_replacement_ci_logs_before_repair"
        classification = "replacement_ci_subject_red_logs_required"
    elif pending_subject:
        next_operation = "wait_or_ingest_final_replacement_ci_result"
        classification = "replacement_ci_subject_pending"
    else:
        next_operation = "operator_rerun_or_ingest_replacement_ci_before_repair"
        classification = "replacement_ci_not_established"

    return ReplacementCIObservation(
        subject_commit=subject_commit,
        observed_status=status,
        source=source,
        source_scope=source_scope,
        evidence_note=evidence_note,
        subject_scoped=scoped,
        replacement_ci_established=replacement_established,
        wound_closure_allowed_next=green_subject,
        repair_allowed_next=False,
        next_operation=next_operation,
        classification=classification,
    )


def observation_to_dict(obs: ReplacementCIObservation) -> dict[str, Any]:
    return {
        "subject_commit": obs.subject_commit,
        "observed_status": obs.observed_status,
        "source": obs.source,
        "source_scope": obs.source_scope,
        "evidence_note": obs.evidence_note,
        "subject_scoped": obs.subject_scoped,
        "replacement_ci_established": obs.replacement_ci_established,
        "wound_closure_allowed_next": obs.wound_closure_allowed_next,
        "repair_allowed_next": obs.repair_allowed_next,
        "next_operation": obs.next_operation,
        "classification": obs.classification,
    }


def render_replacement_ci_panel(obs: ReplacementCIObservation) -> str:
    status = "observed" if obs.replacement_ci_established else "unresolved"
    lines = [
        f"RHPCI [GOLD] status={status}",
        "`- replacement CI observation",
        f"   +- subject-commit: {obs.subject_commit}",
        f"   +- observed-status: {obs.observed_status}",
        f"   +- source-scope: {obs.source_scope}",
        f"   +- subject-scoped: {str(obs.subject_scoped).lower()}",
        f"   +- replacement-ci-established: {str(obs.replacement_ci_established).lower()}",
        f"   +- wound-closure-allowed-next: {str(obs.wound_closure_allowed_next).lower()}",
        f"   +- repair-allowed-next: {str(obs.repair_allowed_next).lower()}",
        f"   +- classification: {obs.classification}",
        f"   +- next: {obs.next_operation}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
