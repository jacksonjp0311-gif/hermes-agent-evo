from __future__ import annotations

import json
from pathlib import Path

from cms.loop.repair_apply_packet import build_apply_packet_manifest

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "outputs" / "loop" / "latest_authorized_repair_apply_gate.json"
OUT_JSON = ROOT / "outputs" / "loop" / "latest_authorized_apply_packet_diff_manifest.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_authorized_apply_packet_diff_manifest.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_authorized_apply_packet_diff_manifest.md"


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
        "# CMS-SA v0.4.7 Authorized Apply Packet Schema and Diff Manifest",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(report.get('passed')).lower()}` |",
        f"| source pressure state | `{report.get('source_pressure_state')}` |",
        f"| source apply gate count | `{report.get('source_apply_gate_count')}` |",
        f"| apply packet count | `{report.get('apply_packet_count')}` |",
        f"| diff manifest count | `{report.get('diff_manifest_count')}` |",
        f"| target writes performed | `{report.get('target_writes_performed')}` |",
        f"| api writes performed | `{report.get('api_writes_performed')}` |",
        f"| git commits performed | `{report.get('git_commits_performed')}` |",
        f"| git pushes performed | `{report.get('git_pushes_performed')}` |",
        f"| release tags created | `{report.get('release_tags_created')}` |",
        f"| manifest hash | `{report.get('apply_packet_manifest_hash', '')}` |",
        "",
        "## Primary Lock",
        "",
        str(report.get("primary_lock", "")),
        "",
        "## Packets",
        "",
    ]
    for packet in report.get("packets", []):
        rows.extend([
            f"### {packet.get('apply_packet_id', 'unknown')}",
            "",
            f"- source apply gate: `{packet.get('source_apply_gate_id', 'unknown')}`",
            f"- packet state: `{packet.get('packet_state', 'unknown')}`",
            f"- apply authority: `{str(packet.get('apply_authority')).lower()}`",
            f"- human authorization artifact present: `{str(packet.get('human_authorization_artifact_present')).lower()}`",
            f"- diff entries: `{packet.get('diff_entry_count', 0)}`",
            f"- rollback entries: `{packet.get('rollback_entry_count', 0)}`",
            f"- rollback binds every diff: `{str(packet.get('rollback_binds_every_diff')).lower()}`",
            f"- target writes requested: `{as_list(packet.get('target_writes_requested', []))}`",
            "",
        ])
    rows.extend(["## Non-Claim Lock", "", str(report.get("non_claim_lock", "")), ""])
    return "\n".join(rows)


def main() -> int:
    apply_gate = load_json(SOURCE)
    report = build_apply_packet_manifest(apply_gate)

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)

    OUT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_MD.write_text(to_markdown(report) + "\n", encoding="utf-8")

    print(json.dumps({
        "schema": "CMS-SA-v0.4.7-authorized-apply-packet-diff-manifest-emission",
        "passed": report["passed"],
        "version": report["version"],
        "apply_packet_count": report["apply_packet_count"],
        "diff_manifest_count": report["diff_manifest_count"],
        "target_writes_performed": report["target_writes_performed"],
        "api_writes_performed": report["api_writes_performed"],
        "git_commits_performed": report["git_commits_performed"],
        "apply_packet_manifest_hash": report["apply_packet_manifest_hash"],
        "non_claim_lock": "Authorized apply packet emission writes evidence artifacts only.",
    }, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())