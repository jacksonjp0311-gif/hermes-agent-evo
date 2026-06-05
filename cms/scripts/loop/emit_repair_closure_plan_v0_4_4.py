from __future__ import annotations

import json
from pathlib import Path

from cms.loop.repair_closure import build_repair_closure_plan

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "outputs" / "loop" / "latest_loop_repair_recommendations.json"
OUT_JSON = ROOT / "outputs" / "loop" / "latest_repair_closure_plan.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_repair_closure_plan.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_repair_closure_plan.md"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def join_list(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(x) for x in value)
    return str(value)


def to_markdown(report: dict) -> str:
    rows = [
        "# CMS-SA v0.4.4 Repair Execution Plan and Closure Ledger",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(report.get('passed')).lower()}` |",
        f"| source pressure state | `{report.get('source_pressure_state')}` |",
        f"| source stability state | `{report.get('source_stability_state')}` |",
        f"| plan count | `{report.get('plan_count')}` |",
        f"| closure count | `{report.get('closure_count')}` |",
        f"| closure hash | `{report.get('closure_hash', '')}` |",
        "",
        "## Primary Lock",
        "",
        str(report.get("primary_lock", "")),
        "",
        "## Plans",
        "",
    ]
    for plan in report.get("plans", []):
        rows.extend([
            f"### {plan.get('plan_id', 'unknown')}",
            "",
            f"- source recommendation: `{plan.get('source_recommendation_id', 'unknown')}`",
            f"- pressure source: `{plan.get('pressure_source', 'unknown')}`",
            f"- repair class: `{plan.get('repair_class', 'unknown')}`",
            f"- execution mode: `{plan.get('execution_mode', 'unknown')}`",
            f"- authorization required: `{str(plan.get('authorization_required')).lower()}`",
            f"- touched surfaces: `{join_list(plan.get('touched_surface_boundary', []))}`",
            f"- required validation: `{join_list(plan.get('required_validation_evidence', []))}`",
            f"- closure state: `{plan.get('closure_state', 'unknown')}`",
            f"- blocked actions preserved: `{join_list(plan.get('blocked_actions_preserved', []))}`",
            "",
        ])
    rows.extend(["## Non-Claim Lock", "", str(report.get("non_claim_lock", "")), ""])
    return "\n".join(rows)


def main() -> int:
    source = load_json(SOURCE)
    report = build_repair_closure_plan(source)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_MD.write_text(to_markdown(report) + "\n", encoding="utf-8")

    print(json.dumps({
        "schema": "CMS-SA-v0.4.4-repair-closure-emission",
        "passed": report["passed"],
        "version": report["version"],
        "plan_count": report["plan_count"],
        "closure_count": report["closure_count"],
        "source_pressure_state": report.get("source_pressure_state"),
        "closure_hash": report["closure_hash"],
        "non_claim_lock": "Repair closure emission writes repository evidence artifacts only.",
    }, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())