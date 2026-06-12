from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from rhp.advancement_lane_registry import decide_lane


REQUIRED_DECLARATION_FIELDS = (
    "operation",
    "lane",
    "ci_state",
    "mutation_requested",
    "closure_requested",
)


@dataclass(frozen=True)
class LaneGateResult:
    operation: str
    lane: str
    ci_state: str
    allowed: bool
    lane_kind: str
    mutation_allowed: bool
    closure_allowed: bool
    reason: str
    missing_fields: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": "RHP-LANE-DECLARATION-GATE-RESULT-v0.1",
            "operation": self.operation,
            "lane": self.lane,
            "ci_state": self.ci_state,
            "allowed": self.allowed,
            "lane_kind": self.lane_kind,
            "mutation_allowed": self.mutation_allowed,
            "closure_allowed": self.closure_allowed,
            "reason": self.reason,
            "missing_fields": list(self.missing_fields),
            "non_claim_lock": "Lane gate permission is not wound closure, release, promotion, or green status.",
        }


def required_fields() -> tuple[str, ...]:
    return REQUIRED_DECLARATION_FIELDS


def validate_lane_declaration(declaration: dict[str, Any]) -> LaneGateResult:
    missing = tuple(field for field in REQUIRED_DECLARATION_FIELDS if field not in declaration)
    operation = str(declaration.get("operation", ""))
    lane = str(declaration.get("lane", ""))
    ci_state = str(declaration.get("ci_state", "unknown"))
    mutation_requested = bool(declaration.get("mutation_requested", False))
    closure_requested = bool(declaration.get("closure_requested", False))

    if missing:
        return LaneGateResult(
            operation=operation,
            lane=lane,
            ci_state=ci_state,
            allowed=False,
            lane_kind="unknown",
            mutation_allowed=False,
            closure_allowed=False,
            reason="missing_required_declaration_fields",
            missing_fields=missing,
        )

    decision = decide_lane(lane, ci_state)
    allowed = decision.allowed
    reason = decision.reason

    if mutation_requested and not decision.mutation_allowed:
        allowed = False
        reason = "mutation_requested_but_lane_does_not_allow_mutation"

    if closure_requested:
        allowed = False
        reason = "closure_requested_inside_lane_gate"

    return LaneGateResult(
        operation=operation,
        lane=lane,
        ci_state=ci_state,
        allowed=allowed,
        lane_kind=decision.lane_kind,
        mutation_allowed=decision.mutation_allowed,
        closure_allowed=False,
        reason=reason,
        missing_fields=(),
    )


def make_declaration(operation: str, lane: str, ci_state: str, *, mutation_requested: bool, closure_requested: bool = False) -> dict[str, object]:
    return {
        "schema": "RHP-LANE-DECLARATION-v0.1",
        "operation": operation,
        "lane": lane,
        "ci_state": ci_state,
        "mutation_requested": mutation_requested,
        "closure_requested": closure_requested,
    }