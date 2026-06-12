from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

SCHEMA = "RHP-CURRENT-OPERATION-CI-WOUND-PACKET-v0.1"

KNOWN_WOUNDS: tuple[str, ...] = (
    "zero_context_next_operation_contract_drift",
    "loop_geometry_legacy_api_drift",
)

CURRENT_OPERATION_COMMIT = "099264be31f0a329375a38fe49e8d0267016f045"
INHERITED_SUBJECT_COMMIT = "ddb24363e2fac630e7527a2c9eab31e6df50db52"


@dataclass(frozen=True)
class CurrentOperationCiWoundReport:
    ok: bool
    current_operation_commit_ok: bool
    inherited_subject_preserved: bool
    ci_red_or_unresolved: bool
    wound_classes_ok: bool
    repair_not_executed: bool
    blocking_reasons: tuple[str, ...]


def classify_current_operation_ci_wounds(failures: Iterable[str]) -> tuple[str, ...]:
    text = "\n".join(failures)
    wounds: list[str] = []

    if (
        "operator_rerun_or_ingest_replacement_ci_before_repair" in text
        and "operator_rerun_ci_or_provide_replacement_green_subject_observation" in text
    ):
        wounds.append("zero_context_next_operation_contract_drift")

    if "from rhp.loop_geometry import geometry" in text or "ImportError" in text and "loop_geometry" in text:
        wounds.append("loop_geometry_legacy_api_drift")

    return tuple(dict.fromkeys(wounds))


def validate_current_operation_ci_wound_packet(packet: Mapping[str, Any]) -> CurrentOperationCiWoundReport:
    reasons: list[str] = []

    current_operation_commit_ok = packet.get("current_operation_commit") == CURRENT_OPERATION_COMMIT
    if not current_operation_commit_ok:
        reasons.append("current_operation_commit_mismatch")

    inherited_subject_preserved = packet.get("inherited_subject_commit") == INHERITED_SUBJECT_COMMIT
    if not inherited_subject_preserved:
        reasons.append("inherited_subject_commit_mismatch")

    ci_red_or_unresolved = packet.get("current_operation_ci_status") in ("failure", "red", "unresolved_red")
    if not ci_red_or_unresolved:
        reasons.append("current_operation_ci_not_red_or_unresolved")

    wound_classes = tuple(packet.get("wound_classes", ()))
    wound_classes_ok = all(wound in wound_classes for wound in KNOWN_WOUNDS)
    if not wound_classes_ok:
        reasons.append("expected_wound_class_missing")

    repair_not_executed = packet.get("repair_execution_enabled") is False and packet.get("repair_executed") is False
    if not repair_not_executed:
        reasons.append("repair_execution_detected")

    return CurrentOperationCiWoundReport(
        ok=not reasons,
        current_operation_commit_ok=current_operation_commit_ok,
        inherited_subject_preserved=inherited_subject_preserved,
        ci_red_or_unresolved=ci_red_or_unresolved,
        wound_classes_ok=wound_classes_ok,
        repair_not_executed=repair_not_executed,
        blocking_reasons=tuple(reasons),
    )


def report_to_dict(report: CurrentOperationCiWoundReport) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "current_operation_commit_ok": report.current_operation_commit_ok,
        "inherited_subject_preserved": report.inherited_subject_preserved,
        "ci_red_or_unresolved": report.ci_red_or_unresolved,
        "wound_classes_ok": report.wound_classes_ok,
        "repair_not_executed": report.repair_not_executed,
        "blocking_reasons": list(report.blocking_reasons),
    }


def render_current_operation_ci_wound_panel(report: CurrentOperationCiWoundReport, wound_classes: Iterable[str]) -> str:
    status = "packetized" if report.ok else "blocked"
    reasons = ",".join(report.blocking_reasons) if report.blocking_reasons else "none"
    wounds = ",".join(wound_classes)
    return "\n".join(
        [
            f"RHPCI-WOUND [GOLD] status={status}",
            "`- current operation CI wound packet",
            f"   +- current-operation-commit-ok: {str(report.current_operation_commit_ok).lower()}",
            f"   +- inherited-subject-preserved: {str(report.inherited_subject_preserved).lower()}",
            f"   +- ci-red-or-unresolved: {str(report.ci_red_or_unresolved).lower()}",
            f"   +- wound-classes-ok: {str(report.wound_classes_ok).lower()}",
            f"   +- repair-not-executed: {str(report.repair_not_executed).lower()}",
            f"   +- wound-classes: {wounds}",
            f"   +- blocking-reasons: {reasons}",
            "   `- authority: no grant [LOCKED]",
        ]
    )
