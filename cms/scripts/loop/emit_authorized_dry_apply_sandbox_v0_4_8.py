from __future__ import annotations

import json
from pathlib import Path

from cms.loop.repair_dry_apply_sandbox import build_dry_apply_sandbox

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "outputs" / "loop" / "latest_authorized_apply_packet_diff_manifest.json"
OUT_JSON = ROOT / "outputs" / "loop" / "latest_authorized_dry_apply_sandbox.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_authorized_dry_apply_sandbox.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_authorized_dry_apply_sandbox.md"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def to_markdown(report: dict) -> str:
    rows = [
        "# CMS-SA v0.4.8 Authorized Apply Executor Dry-Apply Sandbox",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(report.get('passed')).lower()}` |",
        f"| source pressure state | `{report.get('source_pressure_state')}` |",
        f"| source apply packet count | `{report.get('source_apply_packet_count')}` |",
        f"| dry-apply run count | `{report.get('dry_apply_run_count')}` |",
        f"| virtual target writes performed | `{report.get('virtual_target_writes_performed')}` |",
        f"| live target writes performed | `{report.get('live_target_writes_performed')}` |",
        f"| api writes performed | `{report.get('api_writes_performed')}` |",
        f"| git commits performed | `{report.get('git_commits_performed')}` |",
        f"| git pushes performed | `{report.get('git_pushes_performed')}` |",
        f"| release tags created | `{report.get('release_tags_created')}` |",
        f"| sandbox hash | `{report.get('dry_apply_sandbox_hash', '')}` |",
        "",
        "## Primary Lock",
        "",
        str(report.get("primary_lock", "")),
        "",
        "## Runs",
        "",
    ]
    for run in report.get("runs", []):
        rows.extend([
            f"### {run.get('dry_apply_run_id', 'unknown')}",
            "",
            f"- source packet: `{run.get('source_apply_packet_id', 'unknown')}`",
            f"- sandbox state: `{run.get('sandbox_state', 'unknown')}`",
            f"- diff entries: `{run.get('diff_entry_count', 0)}`",
            f"- sandbox operations: `{run.get('sandbox_operation_count', 0)}`",
            f"- rollback simulations: `{run.get('rollback_simulation_count', 0)}`",
            f"- rollback simulation passed: `{str(run.get('rollback_simulation_passed')).lower()}`",
            f"- live target writes: `{run.get('live_target_writes_performed', 0)}`",
            "",
        ])
    rows.extend(["## Non-Claim Lock", "", str(report.get("non_claim_lock", "")), ""])
    return "\n".join(rows)


def main() -> int:
    packet_manifest = load_json(SOURCE)
    report = build_dry_apply_sandbox(packet_manifest)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_MD.write_text(to_markdown(report) + "\n", encoding="utf-8")

    print(json.dumps({
        "schema": "CMS-SA-v0.4.8-authorized-dry-apply-sandbox-emission",
        "passed": report["passed"],
        "version": report["version"],
        "dry_apply_run_count": report["dry_apply_run_count"],
        "virtual_target_writes_performed": report["virtual_target_writes_performed"],
        "live_target_writes_performed": report["live_target_writes_performed"],
        "api_writes_performed": report["api_writes_performed"],
        "git_commits_performed": report["git_commits_performed"],
        "dry_apply_sandbox_hash": report["dry_apply_sandbox_hash"],
        "non_claim_lock": "Dry-apply sandbox emission writes evidence artifacts only.",
    }, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())