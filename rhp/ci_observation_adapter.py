from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Any

ALLOWED_CI_STATES = ("success", "failure", "cancelled", "pending", "unknown")
FAILURE_CONCLUSIONS = {"failure", "cancelled", "timed_out", "action_required", "startup_failure"}
PENDING_STATUSES = {"queued", "requested", "waiting", "pending", "in_progress"}


@dataclass(frozen=True)
class CIObservation:
    commit: str
    observed_status: str
    status_context_count: int
    workflow_run_count: int
    source: str
    raw_reference: str
    green_eligible: bool
    authority_granted: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": "RHP-CI-OBSERVATION-v0.1",
            "commit": self.commit,
            "observed_status": self.observed_status,
            "status_context_count": self.status_context_count,
            "workflow_run_count": self.workflow_run_count,
            "source": self.source,
            "raw_reference": self.raw_reference,
            "green_eligible": self.green_eligible,
            "authority_granted": self.authority_granted,
            "non_claim_lock": "CI observation is evidence only. It does not rerun CI, close wounds, or grant authority.",
        }


def classify_workflow_runs(commit: str, runs: Iterable[Mapping[str, Any]], *, source: str = "workflow_runs") -> CIObservation:
    run_list = list(runs)
    count = len(run_list)
    if count == 0:
        status = "unknown"
    else:
        any_pending = False
        any_failure = False
        all_success_or_skipped = True
        for run in run_list:
            run_status = str(run.get("status", "") or "").lower()
            conclusion = str(run.get("conclusion", "") or "").lower()
            if run_status != "completed" or run_status in PENDING_STATUSES:
                any_pending = True
            if conclusion in FAILURE_CONCLUSIONS:
                any_failure = True
            if conclusion not in {"success", "skipped"}:
                all_success_or_skipped = False
        if any_failure:
            status = "failure"
        elif any_pending:
            status = "pending"
        elif all_success_or_skipped:
            status = "success"
        else:
            status = "unknown"
    return CIObservation(
        commit=commit,
        observed_status=status,
        status_context_count=0,
        workflow_run_count=count,
        source=source,
        raw_reference=source,
        green_eligible=status == "success" and count > 0,
    )


def classify_status_contexts(commit: str, statuses: Iterable[Mapping[str, Any]], *, source: str = "status_contexts") -> CIObservation:
    status_list = list(statuses)
    count = len(status_list)
    if count == 0:
        status = "unknown"
    else:
        states = {str(item.get("state", "") or "").lower() for item in status_list}
        if states & {"failure", "error"}:
            status = "failure"
        elif states & {"pending", "queued", "in_progress"}:
            status = "pending"
        elif states and states <= {"success"}:
            status = "success"
        else:
            status = "unknown"
    return CIObservation(
        commit=commit,
        observed_status=status,
        status_context_count=count,
        workflow_run_count=0,
        source=source,
        raw_reference=source,
        green_eligible=status == "success" and count > 0,
    )


def merge_observations(primary: CIObservation, secondary: CIObservation) -> CIObservation:
    precedence = {"failure": 4, "pending": 3, "success": 2, "cancelled": 2, "unknown": 1}
    chosen = primary if precedence[primary.observed_status] >= precedence[secondary.observed_status] else secondary
    status_context_count = primary.status_context_count + secondary.status_context_count
    workflow_run_count = primary.workflow_run_count + secondary.workflow_run_count
    green_eligible = chosen.observed_status == "success" and (status_context_count > 0 or workflow_run_count > 0)
    return CIObservation(
        commit=chosen.commit,
        observed_status=chosen.observed_status,
        status_context_count=status_context_count,
        workflow_run_count=workflow_run_count,
        source=f"{primary.source}+{secondary.source}",
        raw_reference=f"{primary.raw_reference};{secondary.raw_reference}",
        green_eligible=green_eligible,
    )