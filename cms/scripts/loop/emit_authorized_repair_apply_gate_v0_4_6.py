from __future__ import annotations

import json
from pathlib import Path

from cms.loop.repair_apply_gate import build_apply_gate

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "outputs" / "loop" / "latest_authorized_repair_dry_run.json"
OUT_JSON = ROOT / "outputs" / "loop" / "latest_authorized_repair_apply_gate.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_authorized_repair_apply_gate.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_authorized_repair_apply_gate.md"


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
        "# CMS-SA v0.4.6 Authorized Repair Apply Gate and Rollback Ledger",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(report.get('passed')).lower()}` |",
        f"| source pressure state | `{report.get('source_pressure_state')}` |",
        f"| source dry-run count | `{report.get('source_dry_run_count')}` |",
        f"| apply gate count | `{report.get('apply_gate_count')}` |",
        f"| rollback ledger count | `{report.get('rollback_ledger_count')}` |",
        f"| target writes performed | `{report.get('target_writes_performed')}` |",
        f"| api writes performed | `{report.get('api_writes_performed')}` |",
        f"| git commits performed | `{report.get('git_commits_performed')}` |",
        f"| git pushes performed | `{report.get('git_pushes_performed')}` |",
        f"| release tags created | `{report.get('release_tags_created')}` |",
        f"| apply gate hash | `{report.get('apply_gate_hash', '')}` |",
        "",
        "## Primary Lock",
        "",
        str(report.get("primary_lock", "")),
        "",
        "## Gates",
        "",
    ]
    for gate in report.get("gates", []):
        rows.extend([
            f"### {gate.get('apply_gate_id', 'unknown')}",
            "",
            f"- source dry-run: `{gate.get('source_dry_run_id', 'unknown')}`",
            f"- repair class: `{gate.get('repair_class', 'unknown')}`",
            f"- gate state: `{gate.get('gate_state', 'unknown')}`",
            f"- apply authority: `{str(gate.get('apply_authority')).lower()}`",
            f"- human authorization present: `{str(gate.get('human_authorization_present')).lower()}`",
            f"- rollback required: `{str(gate.get('rollback_required')).lower()}`",
            f"- rollback ready: `{str(gate.get('rollback_ready')).lower()}`",
            f"- touched surfaces: `{as_list(gate.get('touched_surface_boundary', []))}`",
            f"- pre-apply validation: `{as_list(gate.get('pre_apply_validation_required', []))}`",
            "",
        ])
    rows.extend(["## Non-Claim Lock", "", str(report.get("non_claim_lock", "")), ""])
    return "\n".join(rows)


def main() -> int:
    dry_run = load_json(SOURCE)
    report = build_apply_gate(dry_run)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_MD.write_text(to_markdown(report) + "\n", encoding="utf-8")

    print(json.dumps({
        "schema": "CMS-SA-v0.4.6-authorized-repair-apply-gate-emission",
        "passed": report["passed"],
        "version": report["version"],
        "apply_gate_count": report["apply_gate_count"],
        "rollback_ledger_count": report["rollback_ledger_count"],
        "target_writes_performed": report["target_writes_performed"],
        "api_writes_performed": report["api_writes_performed"],
        "git_commits_performed": report["git_commits_performed"],
        "apply_gate_hash": report["apply_gate_hash"],
        "non_claim_lock": "Authorized apply gate emission writes evidence artifacts only.",
    }, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())