from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class LineageFinding:
    code: str
    severity: str
    message: str
    expected: object
    actual: object

    def to_dict(self) -> dict[str, object]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "expected": self.expected,
            "actual": self.actual,
        }


def _get(data: dict[str, Any], field: str) -> Any:
    return data.get(field)


def audit_lineage(pointer: dict[str, Any], evidence: dict[str, Any], head_commit: str | None = None) -> dict[str, Any]:
    findings: list[LineageFinding] = []

    pointer_latest = _get(pointer, "latest_operation")
    evidence_operation = _get(evidence, "operation")
    if pointer_latest != evidence_operation:
        findings.append(LineageFinding(
            code="latest_operation_mismatch",
            severity="error",
            message="latest-rhp latest_operation must match final evidence operation.",
            expected=pointer_latest,
            actual=evidence_operation,
        ))

    pointer_evidence = _get(pointer, "latest_evidence")
    if not pointer_evidence:
        findings.append(LineageFinding(
            code="latest_evidence_missing",
            severity="error",
            message="latest-rhp must name latest evidence path.",
            expected="non-empty latest_evidence",
            actual=pointer_evidence,
        ))

    pointer_subject = _get(pointer, "subject_commit")
    evidence_subject = _get(evidence, "subject_commit")
    if pointer_subject != evidence_subject:
        findings.append(LineageFinding(
            code="subject_commit_mismatch",
            severity="error",
            message="Pointer subject_commit must match final evidence subject_commit.",
            expected=pointer_subject,
            actual=evidence_subject,
        ))

    pointer_state = _get(pointer, "state")
    evidence_state = _get(evidence, "state_after_alignment")
    if pointer_state != evidence_state:
        findings.append(LineageFinding(
            code="state_mismatch",
            severity="error",
            message="Pointer state must match final evidence state_after_alignment.",
            expected=pointer_state,
            actual=evidence_state,
        ))

    pointer_ci = _get(pointer, "observed_ci_status")
    evidence_ci = _get(evidence, "observed_ci_status")
    if pointer_ci != evidence_ci:
        findings.append(LineageFinding(
            code="observed_ci_status_mismatch",
            severity="error",
            message="Pointer observed_ci_status must match final evidence observed_ci_status.",
            expected=pointer_ci,
            actual=evidence_ci,
        ))

    pointer_base = _get(pointer, "operation_base_commit")
    evidence_base = _get(evidence, "operation_base_commit")
    if pointer_base and evidence_base and pointer_base != evidence_base:
        findings.append(LineageFinding(
            code="operation_base_commit_divergence",
            severity="warning",
            message="Pointer operation_base_commit diverges from final evidence operation_base_commit; pointer may be retaining inherited root rather than operation-local base.",
            expected=evidence_base,
            actual=pointer_base,
        ))

    pointer_current = _get(pointer, "current_operation_commit")
    evidence_repair = _get(evidence, "repair_commit")
    if pointer_current and evidence_repair and pointer_current != evidence_repair:
        findings.append(LineageFinding(
            code="current_operation_vs_repair_commit_divergence",
            severity="warning",
            message="Pointer current_operation_commit diverges from final evidence repair_commit.",
            expected=evidence_repair,
            actual=pointer_current,
        ))

    if head_commit and pointer_current and pointer_current != head_commit:
        findings.append(LineageFinding(
            code="head_commit_not_pointer_current_operation_commit",
            severity="info",
            message="HEAD is newer than pointer current_operation_commit; this can be expected when pointer tracks unresolved repair subject rather than latest repo HEAD.",
            expected=head_commit,
            actual=pointer_current,
        ))

    errors = [f for f in findings if f.severity == "error"]
    warnings = [f for f in findings if f.severity == "warning"]
    infos = [f for f in findings if f.severity == "info"]

    return {
        "schema": "RHP-POINTER-EVIDENCE-LINEAGE-AUDIT-v0.1",
        "ok": len(errors) == 0,
        "finding_count": len(findings),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "info_count": len(infos),
        "findings": [f.to_dict() for f in findings],
        "non_claim_lock": "Lineage audit is observability only. It does not repair, close wounds, claim green, or grant authority.",
    }