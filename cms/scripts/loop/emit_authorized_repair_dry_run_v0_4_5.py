from __future__ import annotations

import json
from pathlib import Path

from cms.loop.repair_dry_run import build_authorized_dry_run

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "outputs" / "loop" / "latest_repair_closure_plan.json"
OUT_JSON = ROOT / "outputs" / "loop" / "latest_authorized_repair_dry_run.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_authorized_repair_dry_run.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_authorized_repair_dry_run.md"

def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def as_list(value: object) -> str:
    if isinstance(value, list):
        return ", ".join(str(v) for v in value)
    return str(value)

def to_markdown(report: dict) -> str:
    rows = [
        "# CMS-SA v0.4.5 Authorized Repair Dry-Run Executor",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(report.get('passed')).lower()}` |",
        f"| source pressure state | `{report.get('source_pressure_state')}` |",
        f"| source plan count | `{report.get('source_plan_count')}` |",
        f"| dry-run count | `{report.get('dry_run_count')}` |",
        f"| target writes performed | `{report.get('target_writes_performed')}` |",
        f"| api writes performed | `{report.get('api_writes_performed')}` |",
        f"| commits performed | `{report.get('commits_performed')}` |",
        f"| dry-run hash | `{report.get('dry_run_hash', '')}` |",
        "",
        "## Primary Lock",
        "",
        str(report.get("primary_lock", "")),
        "",
        "## Dry Runs",
        "",
    ]
    for item in report.get("dry_runs", []):
        rows.extend([
            f"### {item.get('dry_run_id', 'unknown')}",
            "",
            f"- source plan: `{item.get('source_plan_id', 'unknown')}`",
            f"- repair class: `{item.get('repair_class', 'unknown')}`",
            f"- execution mode: `{item.get('execution_mode', 'unknown')}`",
            f"- write authority: `{str(item.get('write_authority')).lower()}`",
            f"- target writes: `{len(item.get('target_surface_writes', []))}`",
            f"- touched surfaces: `{as_list(item.get('touched_surface_boundary', []))}`",
            f"- required validation: `{as_list(item.get('required_validation_evidence', []))}`",
            f"- rollback path: `{item.get('rollback_path', '')}`",
            "",
        ])
    rows.extend(["## Non-Claim Lock", "", str(report.get("non_claim_lock", "")), ""])
    return "\n".join(rows)

def main() -> int:
    closure = load_json(SOURCE)
    report = build_authorized_dry_run(closure)
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_MD.write_text(to_markdown(report) + "\n", encoding="utf-8")
    print(json.dumps({
        "schema": "CMS-SA-v0.4.5-authorized-repair-dry-run-emission",
        "passed": report["passed"],
        "version": report["version"],
        "dry_run_count": report["dry_run_count"],
        "target_writes_performed": report["target_writes_performed"],
        "api_writes_performed": report["api_writes_performed"],
        "dry_run_hash": report["dry_run_hash"],
        "non_claim_lock": "Authorized dry-run emission writes evidence artifacts only.",
    }, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())