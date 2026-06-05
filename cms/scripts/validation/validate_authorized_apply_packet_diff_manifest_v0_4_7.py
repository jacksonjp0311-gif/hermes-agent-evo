from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "outputs" / "loop" / "latest_authorized_apply_packet_diff_manifest.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_authorized_apply_packet_diff_manifest.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_authorized_apply_packet_diff_manifest.md"
VALIDATION_JSON = ROOT / "reports" / "loop" / "latest_authorized_apply_packet_diff_manifest_validation.json"
VALIDATION_MD = ROOT / "reports" / "loop" / "latest_authorized_apply_packet_diff_manifest_validation.md"

REQUIRED_PACKET_KEYS = [
    "apply_packet_id",
    "source_apply_gate_id",
    "packet_state",
    "human_authorization_artifact_present",
    "apply_authority",
    "diff_entry_count",
    "rollback_entry_count",
    "rollback_binds_every_diff",
    "target_writes_performed",
    "api_writes_performed",
    "git_commits_performed",
    "blocked_actions_preserved",
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
        findings.append("missing_apply_packet_report")
    if report != copy:
        findings.append("output_report_copy_mismatch")
    if not REPORT_MD.exists():
        findings.append("missing_markdown_report")
    if report.get("schema") != "CMS-SA-v0.4.7-authorized-apply-packet-and-diff-manifest":
        findings.append("schema_mismatch")
    if report.get("version") != "v0.4.7":
        findings.append("version_mismatch")
    if report.get("passed") is not True:
        findings.append("source_report_not_passing")
    for key in ["target_writes_performed", "api_writes_performed", "git_commits_performed", "git_pushes_performed", "release_tags_created"]:
        if report.get(key) != 0:
            findings.append(f"{key}_nonzero")
    if not str(report.get("primary_lock", "")).startswith("No apply packet may authorize"):
        findings.append("primary_lock_missing_or_wrong")

    packets = report.get("packets", [])
    if not isinstance(packets, list) or not packets:
        findings.append("no_apply_packets")
        packets = []

    diff_ledger = report.get("diff_manifest_ledger", [])
    if not isinstance(diff_ledger, list) or len(diff_ledger) != len(packets):
        findings.append("diff_manifest_ledger_count_mismatch")
        diff_ledger = []

    for packet in packets:
        if not isinstance(packet, dict):
            findings.append("packet_not_object")
            continue
        packet_id = packet.get("apply_packet_id", "unknown")
        for key in REQUIRED_PACKET_KEYS:
            if key not in packet or packet.get(key) in ("", None):
                findings.append(f"packet_missing:{packet_id}:{key}")
        if packet.get("apply_authority") is not False:
            findings.append(f"apply_authority_not_false:{packet_id}")
        if packet.get("human_authorization_artifact_present") is not False:
            findings.append(f"authorization_artifact_unexpectedly_present:{packet_id}")
        if packet.get("target_writes_performed") != 0:
            findings.append(f"target_writes_performed_nonzero:{packet_id}")
        if packet.get("rollback_binds_every_diff") is not True:
            findings.append(f"rollback_not_bound_to_diff:{packet_id}")
        if packet.get("diff_entry_count") != packet.get("rollback_entry_count"):
            findings.append(f"diff_rollback_count_mismatch:{packet_id}")
        blocked = packet.get("blocked_actions_preserved", [])
        for action in ["autonomous_patch", "api_write", "silent_target_write", "unreviewed_git_commit", "unreviewed_git_push"]:
            if action not in blocked:
                findings.append(f"blocked_action_not_preserved:{packet_id}:{action}")

    validation = {
        "schema": "CMS-SA-v0.4.7-authorized-apply-packet-diff-manifest-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "findings": findings,
        "apply_packet_count": report.get("apply_packet_count", 0),
        "diff_manifest_count": report.get("diff_manifest_count", 0),
        "source_pressure_state": report.get("source_pressure_state"),
        "target_writes_performed": report.get("target_writes_performed"),
        "api_writes_performed": report.get("api_writes_performed"),
        "git_commits_performed": report.get("git_commits_performed"),
        "git_pushes_performed": report.get("git_pushes_performed"),
        "release_tags_created": report.get("release_tags_created"),
        "apply_packet_manifest_hash": report.get("apply_packet_manifest_hash"),
        "primary_lock": report.get("primary_lock"),
        "non_claim_lock": "Authorized apply packet validation is repository-bound and does not prove code correctness.",
    }

    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    findings_md = "\n".join(f"- `{x}`" for x in findings) if findings else "- none"
    VALIDATION_MD.write_text(
        "# CMS-SA v0.4.7 Authorized Apply Packet Diff Manifest Validation\n\n"
        f"- passed: `{str(validation['passed']).lower()}`\n"
        f"- errors: `{validation['errors']}`\n"
        f"- apply packet count: `{validation['apply_packet_count']}`\n"
        f"- diff manifest count: `{validation['diff_manifest_count']}`\n"
        f"- target writes performed: `{validation['target_writes_performed']}`\n"
        f"- api writes performed: `{validation['api_writes_performed']}`\n"
        f"- git commits performed: `{validation['git_commits_performed']}`\n\n"
        "## Primary Lock\n\n"
        + str(validation.get("primary_lock", ""))
        + "\n\n## Findings\n\n"
        + findings_md
        + "\n\n## Non-Claim Lock\n\nAuthorized apply packet validation is repository-bound and does not prove code correctness.\n",
        encoding="utf-8",
    )
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())