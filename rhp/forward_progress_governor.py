from __future__ import annotations

from dataclasses import dataclass

ORTHOGONAL_ADVANCEMENT_LANES = {
    "documentation",
    "canonization",
    "adapter",
    "tooling",
    "observability",
    "test_contract",
    "operator_experience",
}

BLOCKED_BY_UNRESOLVED_CI = {
    "green_claim",
    "wound_closure",
    "release",
    "promotion",
    "dependency_mutation",
    "destructive_repair",
}

KNOWN_CI_STATES = {"success", "failure", "cancelled", "pending", "unknown"}


@dataclass(frozen=True)
class ProgressDecision:
    lane: str
    ci_state: str
    allowed: bool
    reason: str
    next_state: str

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": "RHP-FORWARD-PROGRESS-DECISION-v0.1",
            "lane": self.lane,
            "ci_state": self.ci_state,
            "allowed": self.allowed,
            "reason": self.reason,
            "next_state": self.next_state,
            "non_claim_lock": "Forward progress permission is not wound closure and is not a green claim.",
        }


def decide_forward_progress(lane: str, ci_state: str) -> ProgressDecision:
    if ci_state not in KNOWN_CI_STATES:
        return ProgressDecision(
            lane=lane,
            ci_state=ci_state,
            allowed=False,
            reason="unknown_ci_state_symbol",
            next_state="stop_with_rhpdiag",
        )

    if lane in BLOCKED_BY_UNRESOLVED_CI:
        if ci_state != "success":
            return ProgressDecision(
                lane=lane,
                ci_state=ci_state,
                allowed=False,
                reason="unresolved_ci_blocks_closure_release_promotion",
                next_state="observe_ci_or_packetize_failure",
            )
        return ProgressDecision(
            lane=lane,
            ci_state=ci_state,
            allowed=True,
            reason="success_surface_required_before_closure_release_promotion",
            next_state="human_authorized_closure_or_release_proposal",
        )

    if lane in ORTHOGONAL_ADVANCEMENT_LANES:
        return ProgressDecision(
            lane=lane,
            ci_state=ci_state,
            allowed=True,
            reason="orthogonal_advancement_allowed_while_ci_unresolved",
            next_state="advance_with_open_wound_preserved",
        )

    return ProgressDecision(
        lane=lane,
        ci_state=ci_state,
        allowed=False,
        reason="unregistered_advancement_lane",
        next_state="stop_with_rhpdiag",
    )


def advancement_policy() -> dict[str, object]:
    return {
        "schema": "RHP-FORWARD-PROGRESS-GOVERNOR-v0.1",
        "orthogonal_advancement_lanes": sorted(ORTHOGONAL_ADVANCEMENT_LANES),
        "blocked_by_unresolved_ci": sorted(BLOCKED_BY_UNRESOLVED_CI),
        "known_ci_states": sorted(KNOWN_CI_STATES),
        "core_rule": "Unknown CI blocks closure, release, promotion, and green claims; it does not block orthogonal system advancement.",
    }