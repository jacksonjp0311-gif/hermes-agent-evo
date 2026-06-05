from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]

REPORT = ROOT / "outputs" / "feedback" / "latest_feedback_lifecycle_report.json"
REPORT_COPY = ROOT / "reports" / "feedback" / "latest_feedback_lifecycle_report.json"
VALIDATION_JSON = ROOT / "reports" / "feedback" / "latest_feedback_lifecycle_validation.json"
VALIDATION_MD = ROOT / "reports" / "feedback" / "latest_feedback_lifecycle_validation.md"

OBSERVABLE_KEYS = ["R", "E", "V", "L", "D", "F", "N", "S", "C", "A"]
ALLOWED_CLASSES = {"CMS-FB-A", "CMS-FB-B", "CMS-FB-C", "CMS-FB-D", "CMS-FB-E"}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    findings: list[str] = []

    report = load_json(REPORT)
    report_copy = load_json(REPORT_COPY)

    if not report:
        findings.append("missing_feedback_lifecycle_report")

    if report != report_copy:
        findings.append("feedback_report_copy_mismatch")

    if report.get("schema") != "CMS-SA-v0.3b-feedback-lifecycle-report":
        findings.append("schema_mismatch")

    if report.get("version") != "v0.3b":
        findings.append("version_mismatch")

    items = report.get("items", [])
    if not items:
        findings.append("no_feedback_items")

    for index, item in enumerate(items):
        for key in (
            "id",
            "source",
            "summary",
            "route",
            "observables",
            "score",
            "classification",
            "lifecycle_state",
            "evidence",
            "validator_binding",
            "downgrade_path",
            "falsification_condition",
            "non_claim_lock",
        ):
            if key not in item:
                findings.append(f"item_{index}_missing_{key}")

        route = item.get("route", {})
        for key in ("shell", "meridian", "sector"):
            if key not in route:
                findings.append(f"item_{index}_route_missing_{key}")

        observables = item.get("observables", {})
        for key in OBSERVABLE_KEYS:
            if observables.get(key) != 1:
                findings.append(f"item_{index}_observable_{key}_not_passing")

        if item.get("classification") not in ALLOWED_CLASSES:
            findings.append(f"item_{index}_invalid_classification")

        if not item.get("downgrade_path"):
            findings.append(f"item_{index}_missing_downgrade_path")

        if not item.get("negative_control"):
            findings.append(f"item_{index}_missing_negative_control")

        if not item.get("surrogate_or_dry_run"):
            findings.append(f"item_{index}_missing_surrogate_or_dry_run")

        if not item.get("falsification_condition"):
            findings.append(f"item_{index}_missing_falsification_condition")

        if not item.get("non_claim_lock"):
            findings.append(f"item_{index}_missing_non_claim_lock")

    api_boundary = report.get("api_boundary", {})
    for phase in ("observe", "classify", "propose", "validate", "authorize", "write", "seal"):
        if phase not in api_boundary:
            findings.append(f"api_boundary_missing_{phase}")

    validation = {
        "schema": "CMS-SA-v0.3b-feedback-lifecycle-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "warnings": 0,
        "findings": findings,
        "item_count": len(items),
        "class_counts": report.get("class_counts", {}),
        "observables": OBSERVABLE_KEYS,
        "api_boundary_present": all(phase in api_boundary for phase in ("observe", "classify", "propose", "validate", "authorize", "write", "seal")),
        "non_claim_lock": "Feedback lifecycle validation checks repository-bound feedback governance only. It does not prove code correctness."
    }

    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2) + "\n", encoding="utf-8")

    md = [
        "# CMS-SA v0.3b Feedback Lifecycle Validation",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(validation['passed']).lower()}` |",
        f"| errors | `{validation['errors']}` |",
        f"| warnings | `0` |",
        f"| item count | `{validation['item_count']}` |",
        f"| class counts | `{json.dumps(validation['class_counts'], sort_keys=True)}` |",
        f"| API boundary present | `{str(validation['api_boundary_present']).lower()}` |",
        "",
        "Non-claim lock: feedback lifecycle validation checks repository-bound feedback governance only. It does not prove code correctness.",
        "",
    ]
    VALIDATION_MD.write_text("\n".join(md), encoding="utf-8")

    print(json.dumps(validation, indent=2))
    return 0 if validation["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())