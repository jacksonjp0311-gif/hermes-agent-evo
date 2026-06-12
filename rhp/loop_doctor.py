from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable

from rhp.visible_console import ConsoleField, ConsolePanel, render_panel


@dataclass(frozen=True)
class DoctorLoopSummary:
    latest_operation: str
    state: str
    next_operation: str
    can_mutate: bool
    blocked_reasons: tuple[str, ...]
    evidence_api_ok: bool
    replay_ok: bool
    worktree_clean: bool


def summarize_doctor_payload(payload: dict[str, Any]) -> DoctorLoopSummary:
    doctor = payload.get("doctor", payload)
    return DoctorLoopSummary(
        latest_operation=str(doctor.get("latest_operation", "")),
        state=str(doctor.get("state", "")),
        next_operation=str(doctor.get("next_legal_operation", "")),
        can_mutate=bool(doctor.get("can_mutate", False)),
        blocked_reasons=tuple(str(item) for item in doctor.get("blocked_reasons", [])),
        evidence_api_ok=bool(doctor.get("evidence_api_ok", False)),
        replay_ok=bool(doctor.get("replay_ok", False)),
        worktree_clean=bool(doctor.get("worktree_clean", False)),
    )


def render_doctor_panel(payload: dict[str, Any]) -> str:
    summary = summarize_doctor_payload(payload)
    fields = [
        ConsoleField("latest-operation", summary.latest_operation),
        ConsoleField("state", summary.state),
        ConsoleField("evidence-api-ok", str(summary.evidence_api_ok).lower()),
        ConsoleField("replay-ok", str(summary.replay_ok).lower()),
        ConsoleField("worktree-clean", str(summary.worktree_clean).lower()),
        ConsoleField("can-mutate", str(summary.can_mutate).lower()),
        ConsoleField("blocked-reasons", ", ".join(summary.blocked_reasons) or "none"),
        ConsoleField("next", summary.next_operation),
    ]
    return render_panel(ConsolePanel(
        tag="RHPLOOP-DOCTOR [GOLD]",
        title="read-only loop doctor cockpit",
        status="diagnostic",
        tone="gold",
        fields=fields,
        footer="authority: no grant [LOCKED]",
    ))


SELF_LEARNING_REQUIRED_FIELDS = (
    "observed_event",
    "evidence_path",
    "lesson",
    "future_behavior_change",
    "authority_boundary",
)


def validate_self_learning_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
    missing = [field for field in SELF_LEARNING_REQUIRED_FIELDS if not candidate.get(field)]
    authority_boundary = str(candidate.get("authority_boundary", "")).lower()
    grants_authority = any(token in authority_boundary for token in ("self_authorization=true", "autonomous_authority=true", "grant authority"))
    ok = not missing and not grants_authority
    return {
        "schema": "RHPLOOP-SELF-LEARNING-CANDIDATE-VALIDATION-v0.1",
        "ok": ok,
        "missing": missing,
        "grants_authority": grants_authority,
        "classification": "promotable_lesson_candidate" if ok else "blocked_learning_candidate",
        "non_claim_lock": "Self-learning candidates propose future behavior rules only; they do not mutate memory, grant authority, or apply repairs.",
    }


def render_self_learning_panel(candidate: dict[str, Any]) -> str:
    result = validate_self_learning_candidate(candidate)
    fields = [
        ConsoleField("observed-event", str(candidate.get("observed_event", ""))),
        ConsoleField("evidence", str(candidate.get("evidence_path", ""))),
        ConsoleField("lesson", str(candidate.get("lesson", ""))),
        ConsoleField("future-behavior", str(candidate.get("future_behavior_change", ""))),
        ConsoleField("classification", str(result["classification"])),
        ConsoleField("authority", "no grant"),
    ]
    return render_panel(ConsolePanel(
        tag="RHPLOOP-SELF-LEARNING [GOLD]",
        title="validated lesson candidate",
        status="proposed" if result["ok"] else "blocked",
        tone="gold",
        fields=fields,
        footer="promotion: evidence-gated / human-authorized [LOCKED]",
    ))
