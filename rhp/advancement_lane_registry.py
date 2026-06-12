from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

LaneKind = Literal["orthogonal", "blocked_when_ci_unresolved", "unknown"]

LANES: dict[str, dict[str, object]] = {
    "documentation": {
        "kind": "orthogonal",
        "description": "Human/AI readability, README/AGENTS/context updates.",
    },
    "canonization": {
        "kind": "orthogonal",
        "description": "Promote validated learned rules into canonical geometry.",
    },
    "adapter": {
        "kind": "orthogonal",
        "description": "Reusable observation or classification adapter.",
    },
    "tooling": {
        "kind": "orthogonal",
        "description": "Non-destructive helper tooling with tests.",
    },
    "observability": {
        "kind": "orthogonal",
        "description": "Evidence capture, diagnostics, dashboards, or reports.",
    },
    "test_contract": {
        "kind": "orthogonal",
        "description": "Tests that lock known contracts without closing wounds.",
    },
    "operator_experience": {
        "kind": "orthogonal",
        "description": "Operator ergonomics, no-prompt flow, readable panels.",
    },
    "green_claim": {
        "kind": "blocked_when_ci_unresolved",
        "description": "Claim that a subject or operation is green.",
    },
    "wound_closure": {
        "kind": "blocked_when_ci_unresolved",
        "description": "Close a named wound.",
    },
    "release": {
        "kind": "blocked_when_ci_unresolved",
        "description": "Promote a version or release milestone.",
    },
    "promotion": {
        "kind": "blocked_when_ci_unresolved",
        "description": "Promote memory/evidence/status to higher authority.",
    },
    "dependency_mutation": {
        "kind": "blocked_when_ci_unresolved",
        "description": "Change dependencies or external execution contract.",
    },
    "destructive_repair": {
        "kind": "blocked_when_ci_unresolved",
        "description": "Delete, rewrite, reset, or destructive code repair.",
    },
}

CI_UNRESOLVED_STATES = {"unknown", "pending", "failure", "cancelled"}


@dataclass(frozen=True)
class LaneDecision:
    lane: str
    ci_state: str
    allowed: bool
    lane_kind: LaneKind
    reason: str
    mutation_allowed: bool
    closure_allowed: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": "RHP-ADVANCEMENT-LANE-DECISION-v0.1",
            "lane": self.lane,
            "ci_state": self.ci_state,
            "allowed": self.allowed,
            "lane_kind": self.lane_kind,
            "reason": self.reason,
            "mutation_allowed": self.mutation_allowed,
            "closure_allowed": self.closure_allowed,
            "non_claim_lock": "Lane permission is not wound closure, release, or green status.",
        }


def lane_kind(lane: str) -> LaneKind:
    data = LANES.get(lane)
    if not data:
        return "unknown"
    return str(data["kind"])  # type: ignore[return-value]


def decide_lane(lane: str, ci_state: str) -> LaneDecision:
    kind = lane_kind(lane)
    if kind == "unknown":
        return LaneDecision(
            lane=lane,
            ci_state=ci_state,
            allowed=False,
            lane_kind="unknown",
            reason="lane_not_registered",
            mutation_allowed=False,
            closure_allowed=False,
        )

    if kind == "orthogonal":
        return LaneDecision(
            lane=lane,
            ci_state=ci_state,
            allowed=True,
            lane_kind="orthogonal",
            reason="orthogonal_lane_allowed_with_open_wound_preserved",
            mutation_allowed=True,
            closure_allowed=False,
        )

    if kind == "blocked_when_ci_unresolved" and ci_state in CI_UNRESOLVED_STATES:
        return LaneDecision(
            lane=lane,
            ci_state=ci_state,
            allowed=False,
            lane_kind="blocked_when_ci_unresolved",
            reason="ci_unresolved_blocks_this_lane",
            mutation_allowed=False,
            closure_allowed=False,
        )

    return LaneDecision(
        lane=lane,
        ci_state=ci_state,
        allowed=True,
        lane_kind="blocked_when_ci_unresolved",
        reason="ci_resolved_success_routes_to_human_authorized_proposal",
        mutation_allowed=False,
        closure_allowed=False,
    )


def registry() -> dict[str, object]:
    return {
        "schema": "RHP-ORTHOGONAL-ADVANCEMENT-LANE-REGISTRY-v0.1",
        "lanes": LANES,
        "ci_unresolved_states": sorted(CI_UNRESOLVED_STATES),
        "rule": "Every operation must declare its lane before mutation.",
    }