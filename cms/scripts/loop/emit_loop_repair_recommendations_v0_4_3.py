from __future__ import annotations

import json
from pathlib import Path

from cms.loop.repair_recommendation import build_loop_repair_recommendations

ROOT = Path(__file__).resolve().parents[2]
PRESSURE = ROOT / "outputs" / "loop" / "latest_loop_drift_pressure.json"
OUT_JSON = ROOT / "outputs" / "loop" / "latest_loop_repair_recommendations.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_loop_repair_recommendations.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_loop_repair_recommendations.md"

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def join_list(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value)
    if value is None:
        return ""
    return str(value)

def to_markdown(report: dict) -> str:
    lines = [
        "# CMS-SA v0.4.3 Loop Pressure Repair Recommendations",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(report.get('passed')).lower()}` |",
        f"| pressure state | `{report.get('pressure_state', 'unknown')}` |",
        f"| pressure | `{report.get('loop_drift_pressure', 'unknown')}` |",
        f"| threshold | `{report.get('threshold', 'unknown')}` |",
        f"| source stability | `{report.get('source_stability_state', 'unknown')}` |",
        f"| dominant pressure source | `{report.get('dominant_pressure_source', 'unknown')}` |",
        f"| dominant repair class | `{report.get('dominant_repair_class', 'unknown')}` |",
        f"| recommendation count | `{report.get('recommendation_count', 0)}` |",
        f"| recommendation hash | `{report.get('recommendation_hash', 'unknown')}` |",
        "",
        "## Primary Lock",
        "",
        str(report.get("primary_lock", "")),
        "",
        "## Recommendations",
        "",
    ]

    for rec in report.get("recommendations", []):
        pressure_source = rec.get("pressure_source", rec.get("finding", "unknown"))
        repair_class = rec.get("repair_class", "unknown")
        allowed_action = rec.get("allowed_repair_action", rec.get("action", "unknown"))
        required_validation = rec.get("required_validation_stack", rec.get("validators", []))
        lines.extend([
            f"### {rec.get('id', 'unknown')}",
            "",
            f"- pressure source: `{pressure_source}`",
            f"- source kind: `{rec.get('source_kind', 'unknown')}`",
            f"- source value: `{rec.get('source_value', 'unknown')}`",
            f"- repair class: `{repair_class}`",
            f"- pressure state: `{rec.get('pressure_state', 'unknown')}`",
            f"- severity: `{rec.get('severity', 'unknown')}`",
            f"- allowed repair action: `{allowed_action}`",
            f"- blocked actions: `{join_list(rec.get('blocked_actions', []))}`",
            f"- required files: `{join_list(rec.get('required_files', []))}`",
            f"- required validation: `{join_list(required_validation)}`",
            f"- status: `{rec.get('status', 'unknown')}`",
            f"- downgrade path: `{rec.get('downgrade_path', 'unknown')}`",
            "",
        ])

    if report.get("unknown_findings"):
        lines.extend(["## Unknown Findings", ""])
        lines.extend(f"- `{item}`" for item in report["unknown_findings"])
        lines.append("")

    lines.extend(["## Non-Claim Lock", "", str(report.get("non_claim_lock", "")), ""])
    return "\n".join(lines)

def main() -> int:
    pressure = load_json(PRESSURE)
    report = build_loop_repair_recommendations(pressure)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_MD.write_text(to_markdown(report) + "\n", encoding="utf-8")

    print(json.dumps({
        "schema": "CMS-SA-v0.4.3-loop-pressure-repair-recommendation-emission",
        "passed": report["passed"],
        "version": report["version"],
        "pressure_state": report.get("pressure_state"),
        "dominant_pressure_source": report.get("dominant_pressure_source"),
        "dominant_repair_class": report.get("dominant_repair_class"),
        "recommendation_count": report["recommendation_count"],
        "unknown_findings": report["unknown_findings"],
        "recommendation_hash": report["recommendation_hash"],
        "non_claim_lock": "Recommendation emission writes repository evidence artifacts only.",
    }, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
