from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from rhp.lane_declaration_gate import validate_lane_declaration


REQUIRED_MANIFEST_FIELDS = (
    "operation",
    "lane",
    "ci_state",
    "story",
    "declared_files",
    "allowed_mutations",
    "forbidden_actions",
    "evidence_outputs",
    "validation_commands",
    "non_claim_locks",
)

FORBIDDEN_ACTIONS_REQUIRED = (
    "claim_green",
    "close_wound",
    "release",
    "promote",
    "dependency_mutation",
    "destructive_repair",
    "grant_authority",
)


@dataclass(frozen=True)
class ManifestValidation:
    operation: str
    lane: str
    ci_state: str
    ok: bool
    missing_fields: tuple[str, ...]
    missing_forbidden_actions: tuple[str, ...]
    lane_gate_allowed: bool
    reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "schema": "RHP-OPERATION-MANIFEST-VALIDATION-v0.1",
            "operation": self.operation,
            "lane": self.lane,
            "ci_state": self.ci_state,
            "ok": self.ok,
            "missing_fields": list(self.missing_fields),
            "missing_forbidden_actions": list(self.missing_forbidden_actions),
            "lane_gate_allowed": self.lane_gate_allowed,
            "reason": self.reason,
            "non_claim_lock": "Manifest validation is pre-mutation structure only; it is not green status, wound closure, release, or authority.",
        }


def required_manifest_fields() -> tuple[str, ...]:
    return REQUIRED_MANIFEST_FIELDS


def required_forbidden_actions() -> tuple[str, ...]:
    return FORBIDDEN_ACTIONS_REQUIRED


def make_manifest(
    *,
    operation: str,
    lane: str,
    ci_state: str,
    story: str,
    declared_files: list[str],
    allowed_mutations: list[str],
    forbidden_actions: list[str],
    evidence_outputs: list[str],
    validation_commands: list[str],
    non_claim_locks: list[str],
) -> dict[str, object]:
    return {
        "schema": "RHP-OPERATION-MANIFEST-v0.1",
        "operation": operation,
        "lane": lane,
        "ci_state": ci_state,
        "story": story,
        "declared_files": declared_files,
        "allowed_mutations": allowed_mutations,
        "forbidden_actions": forbidden_actions,
        "evidence_outputs": evidence_outputs,
        "validation_commands": validation_commands,
        "non_claim_locks": non_claim_locks,
    }


def validate_manifest(manifest: dict[str, Any]) -> ManifestValidation:
    missing_fields = tuple(field for field in REQUIRED_MANIFEST_FIELDS if field not in manifest)
    operation = str(manifest.get("operation", ""))
    lane = str(manifest.get("lane", ""))
    ci_state = str(manifest.get("ci_state", "unknown"))
    forbidden_actions = set(manifest.get("forbidden_actions", []) or [])
    missing_forbidden = tuple(action for action in FORBIDDEN_ACTIONS_REQUIRED if action not in forbidden_actions)

    if missing_fields:
        return ManifestValidation(
            operation=operation,
            lane=lane,
            ci_state=ci_state,
            ok=False,
            missing_fields=missing_fields,
            missing_forbidden_actions=missing_forbidden,
            lane_gate_allowed=False,
            reason="missing_required_manifest_fields",
        )

    lane_declaration = {
        "operation": operation,
        "lane": lane,
        "ci_state": ci_state,
        "mutation_requested": True,
        "closure_requested": False,
    }
    lane_result = validate_lane_declaration(lane_declaration)
    if not lane_result.allowed:
        return ManifestValidation(
            operation=operation,
            lane=lane,
            ci_state=ci_state,
            ok=False,
            missing_fields=(),
            missing_forbidden_actions=missing_forbidden,
            lane_gate_allowed=False,
            reason="lane_gate_rejected_manifest",
        )

    if missing_forbidden:
        return ManifestValidation(
            operation=operation,
            lane=lane,
            ci_state=ci_state,
            ok=False,
            missing_fields=(),
            missing_forbidden_actions=missing_forbidden,
            lane_gate_allowed=True,
            reason="missing_required_forbidden_actions",
        )

    if not manifest.get("story"):
        return ManifestValidation(
            operation=operation,
            lane=lane,
            ci_state=ci_state,
            ok=False,
            missing_fields=(),
            missing_forbidden_actions=(),
            lane_gate_allowed=True,
            reason="story_required",
        )

    return ManifestValidation(
        operation=operation,
        lane=lane,
        ci_state=ci_state,
        ok=True,
        missing_fields=(),
        missing_forbidden_actions=(),
        lane_gate_allowed=True,
        reason="manifest_valid",
    )