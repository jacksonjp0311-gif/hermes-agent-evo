
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any, Dict, List

VERSION = "v0.3b4"
SCHEMA = "CMS-SA-v0.3b4-negative-control-harness"
VALID_DECISIONS = {"promote", "block", "downgrade", "observe_only"}
NON_CLAIM_LOCK = (
    "Negative control validation is repository-bound and does not prove code "
    "correctness, truth, AGI, consciousness, production readiness, security, "
    "external validation, or real-world correctness."
)

@dataclass(frozen=True)
class ControlCase:
    control_id: str
    control_class: str
    description: str
    input_signals: Dict[str, Any]
    expected_decision: str
    downgrade_path: str
    falsification_condition: str
    non_claim_lock: str = NON_CLAIM_LOCK

def evaluate_control(case: ControlCase) -> str:
    signals = case.input_signals
    if signals.get("false_promote_attempt") is True:
        return "block"
    if signals.get("required_validator_failed") is True:
        return "block"
    if signals.get("downgrade_required") is True:
        return "downgrade"
    if signals.get("evidence_incomplete") is True:
        return "observe_only"
    if signals.get("all_required_surfaces_passed") is True:
        return "promote"
    return "observe_only"

def _cases() -> List[ControlCase]:
    return [
        ControlCase(
            control_id="NC-001-positive-promote",
            control_class="positive_control",
            description="A clean validator-bound state may promote.",
            input_signals={"all_required_surfaces_passed": True, "required_validator_failed": False, "false_promote_attempt": False, "downgrade_required": False, "evidence_incomplete": False},
            expected_decision="promote",
            downgrade_path="none",
            falsification_condition="Fails if a clean positive control cannot promote.",
        ),
        ControlCase(
            control_id="NC-002-required-validator-block",
            control_class="negative_control",
            description="A missing or failed required validator must block promotion.",
            input_signals={"all_required_surfaces_passed": False, "required_validator_failed": True, "false_promote_attempt": False, "downgrade_required": False, "evidence_incomplete": False},
            expected_decision="block",
            downgrade_path="repair_required_validator_surface",
            falsification_condition="Fails if a required validator failure can still promote.",
        ),
        ControlCase(
            control_id="NC-003-false-promote-rejected",
            control_class="false_promote_control",
            description="False promote attempts must be rejected even if other surface language looks confident.",
            input_signals={"all_required_surfaces_passed": True, "required_validator_failed": False, "false_promote_attempt": True, "downgrade_required": False, "evidence_incomplete": False},
            expected_decision="block",
            downgrade_path="reject_false_promote_and_require_replay",
            falsification_condition="Fails if false_promote_attempt yields promote.",
        ),
        ControlCase(
            control_id="NC-004-downgrade-preserved",
            control_class="downgrade_control",
            description="Weak but useful cases must downgrade instead of being erased or promoted.",
            input_signals={"all_required_surfaces_passed": False, "required_validator_failed": False, "false_promote_attempt": False, "downgrade_required": True, "evidence_incomplete": False},
            expected_decision="downgrade",
            downgrade_path="preserve_as_downgraded_feedback_item",
            falsification_condition="Fails if downgrade-required case promotes or disappears.",
        ),
        ControlCase(
            control_id="NC-005-observe-only",
            control_class="observe_only_control",
            description="Incomplete evidence should remain observable but non-promotional.",
            input_signals={"all_required_surfaces_passed": False, "required_validator_failed": False, "false_promote_attempt": False, "downgrade_required": False, "evidence_incomplete": True},
            expected_decision="observe_only",
            downgrade_path="hold_for_more_evidence",
            falsification_condition="Fails if incomplete evidence promotes.",
        ),
    ]

def build_negative_control_harness() -> Dict[str, Any]:
    controls: List[Dict[str, Any]] = []
    for case in _cases():
        observed = evaluate_control(case)
        item = asdict(case)
        item["observed_decision"] = observed
        item["passed"] = observed == case.expected_decision
        controls.append(item)

    required_classes = {"positive_control", "negative_control", "false_promote_control", "downgrade_control", "observe_only_control"}
    observed_classes = {item["control_class"] for item in controls}
    false_promote_rejected = all(item["observed_decision"] != "promote" for item in controls if item["control_class"] == "false_promote_control")
    downgrade_preserved = any(item["control_class"] == "downgrade_control" and item["observed_decision"] == "downgrade" for item in controls)
    observe_only_preserved = any(item["control_class"] == "observe_only_control" and item["observed_decision"] == "observe_only" for item in controls)
    passed = all(item["passed"] for item in controls) and required_classes.issubset(observed_classes) and false_promote_rejected and downgrade_preserved and observe_only_preserved

    body: Dict[str, Any] = {
        "schema": SCHEMA,
        "version": VERSION,
        "passed": passed,
        "control_count": len(controls),
        "required_classes": sorted(required_classes),
        "observed_classes": sorted(observed_classes),
        "false_promote_rejected": false_promote_rejected,
        "downgrade_preserved": downgrade_preserved,
        "observe_only_preserved": observe_only_preserved,
        "controls": controls,
        "non_claim_lock": NON_CLAIM_LOCK,
    }
    stable = json.dumps(body, sort_keys=True, separators=(",", ":"))
    body["harness_hash"] = sha256(stable.encode("utf-8")).hexdigest()
    return body
