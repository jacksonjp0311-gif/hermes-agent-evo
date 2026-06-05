from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "outputs" / "loop" / "latest_repair_closure_plan.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_repair_closure_plan.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_repair_closure_plan.md"
VALIDATION_JSON = ROOT / "reports" / "loop" / "latest_repair_closure_validation.json"
VALIDATION_MD = ROOT / "reports" / "loop" / "latest_repair_closure_validation.md"

REQUIRED_PLAN_KEYS = [
    "plan_id",
    "source_recommendation_id",
    "repair_class",
    "execution_mode",
    "authorization_required",
    "blocked_actions_preserved",
    "touched_surface_boundary",
    "required_validation_evidence",
    "closure_state",
    "non_claim_lock",
]


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    findings: list[str] = []
    report = load_json(OUT_JSON)
    copy = load_json(REPORT_JSON)

    if not report:
        findings.append("missing_repair_closure_report")
    if report != copy:
        findings.append("output_report_copy_mismatch")
    if not REPORT_MD.exists():
        findings.append("missing_markdown_report")
    if report.get("schema") != "CMS-SA-v0.4.4-repair-execution-plan-and-closure-ledger":
        findings.append("schema_mismatch")
    if report.get("version") != "v0.4.4":
        findings.append("version_mismatch")
    if report.get("passed") is not True:
        findings.append("source_report_not_passing")
    if not report.get("primary_lock", "").startswith("No repair recommendation may be marked closed"):
        findings.append("primary_lock_missing_or_wrong")

    plans = report.get("plans", [])
    if not isinstance(plans, list) or not plans:
        findings.append("no_plans")
        plans = []

    for plan in plans:
        if not isinstance(plan, dict):
            findings.append("plan_not_object")
            continue
        for key in REQUIRED_PLAN_KEYS:
            if key not in plan or plan.get(key) in ("", [], None):
                findings.append(f"plan_missing:{plan.get('plan_id', 'unknown')}:{key}")
        if plan.get("repair_class") != "NO_REPAIR" and plan.get("authorization_required") is not True:
            findings.append(f"non_noop_plan_missing_authorization:{plan.get('plan_id', 'unknown')}")
        if plan.get("repair_class") == "NO_REPAIR" and plan.get("closure_state") != "closed_no_op":
            findings.append(f"noop_plan_not_closed_noop:{plan.get('plan_id', 'unknown')}")

    validation = {
        "schema": "CMS-SA-v0.4.4-repair-closure-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "findings": findings,
        "plan_count": report.get("plan_count", 0),
        "closure_count": report.get("closure_count", 0),
        "source_pressure_state": report.get("source_pressure_state"),
        "closure_hash": report.get("closure_hash"),
        "primary_lock": report.get("primary_lock"),
        "non_claim_lock": "Repair closure validation is repository-bound and does not prove code correctness.",
    }

    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    findings_md = "\n".join(f"- `{x}`" for x in findings) if findings else "- none"
    VALIDATION_MD.write_text(
        "# CMS-SA v0.4.4 Repair Closure Validation\n\n"
        f"- passed: `{str(validation['passed']).lower()}`\n"
        f"- errors: `{validation['errors']}`\n"
        f"- plan count: `{validation['plan_count']}`\n"
        f"- closure count: `{validation['closure_count']}`\n"
        f"- source pressure state: `{validation['source_pressure_state']}`\n\n"
        "## Primary Lock\n\n"
        + str(validation.get("primary_lock", ""))
        + "\n\n## Findings\n\n"
        + findings_md
        + "\n\n## Non-Claim Lock\n\nRepair closure validation is repository-bound and does not prove code correctness.\n",
        encoding="utf-8",
    )

    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())