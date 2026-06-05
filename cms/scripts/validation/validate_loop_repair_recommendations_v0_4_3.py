from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "outputs" / "loop" / "latest_loop_repair_recommendations.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_loop_repair_recommendations.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_loop_repair_recommendations.md"
VALIDATION_JSON = ROOT / "reports" / "loop" / "latest_loop_repair_recommendations_validation.json"
VALIDATION_MD = ROOT / "reports" / "loop" / "latest_loop_repair_recommendations_validation.md"

REQUIRED_KEYS = (
    "id",
    "pressure_source",
    "repair_class",
    "pressure_state",
    "severity",
    "allowed_repair_action",
    "blocked_actions",
    "required_validation_stack",
    "downgrade_path",
    "non_claim_lock",
    "status",
)

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    findings: list[str] = []
    report = load_json(OUT_JSON)
    copy = load_json(REPORT_JSON)

    if not report:
        findings.append("missing_recommendation_report")
    if report != copy:
        findings.append("recommendation_report_copy_mismatch")
    if not REPORT_MD.exists():
        findings.append("missing_recommendation_markdown")
    if report.get("schema") != "CMS-SA-v0.4.3-loop-pressure-repair-recommendation":
        findings.append("schema_mismatch")
    if report.get("version") != "v0.4.3":
        findings.append("version_mismatch")
    if report.get("passed") is not True:
        findings.append("source_report_not_passing")
    if not report.get("recommendations"):
        findings.append("no_recommendations")
    if not report.get("primary_lock", "").startswith("No repair recommendation may"):
        findings.append("primary_lock_missing_or_wrong")

    for rec in report.get("recommendations", []):
        for key in REQUIRED_KEYS:
            if key not in rec:
                findings.append(f"recommendation_missing:{rec.get('id')}:{key}")
        if not rec.get("allowed_repair_action"):
            findings.append(f"recommendation_missing_allowed_action:{rec.get('id')}")
        if not rec.get("blocked_actions"):
            findings.append(f"recommendation_missing_blocked_actions:{rec.get('id')}")
        if not rec.get("required_validation_stack"):
            findings.append(f"recommendation_missing_required_validation:{rec.get('id')}")
        if not rec.get("non_claim_lock"):
            findings.append(f"recommendation_missing_non_claim_lock:{rec.get('id')}")

    pressure = float(report.get("loop_drift_pressure", 1.0) or 1.0)
    threshold = float(report.get("threshold", 0.25) or 0.25)
    if pressure > threshold:
        findings.append("pressure_exceeds_threshold_blocks_release")

    validation = {
        "schema": "CMS-SA-v0.4.3-loop-repair-recommendation-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "findings": findings,
        "recommendation_count": report.get("recommendation_count", 0),
        "loop_drift_pressure": report.get("loop_drift_pressure"),
        "pressure_state": report.get("pressure_state"),
        "dominant_pressure_source": report.get("dominant_pressure_source"),
        "dominant_repair_class": report.get("dominant_repair_class"),
        "source_stability_state": report.get("source_stability_state"),
        "recommendation_hash": report.get("recommendation_hash"),
        "primary_lock": report.get("primary_lock"),
        "non_claim_lock": "Loop repair recommendation validation is repository-bound and does not prove code correctness.",
    }

    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    md = [
        "# CMS-SA v0.4.3 Loop Repair Recommendation Validation",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(validation['passed']).lower()}` |",
        f"| errors | `{validation['errors']}` |",
        f"| recommendation count | `{validation['recommendation_count']}` |",
        f"| pressure state | `{validation['pressure_state']}` |",
        f"| dominant pressure source | `{validation['dominant_pressure_source']}` |",
        f"| dominant repair class | `{validation['dominant_repair_class']}` |",
        f"| loop drift pressure | `{validation['loop_drift_pressure']}` |",
        "",
        "## Primary Lock",
        "",
        str(validation.get("primary_lock", "")),
        "",
        "Non-claim lock: loop repair recommendation validation is repository-bound and does not prove code correctness.",
        "",
    ]
    if findings:
        md.extend(["## Findings", ""])
        md.extend(f"- `{finding}`" for finding in findings)
        md.append("")
    VALIDATION_MD.write_text("\n".join(md), encoding="utf-8")

    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
