from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "outputs" / "loop" / "latest_authorized_repair_apply_gate.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_authorized_repair_apply_gate.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_authorized_repair_apply_gate.md"
VALIDATION_JSON = ROOT / "reports" / "loop" / "latest_authorized_repair_apply_gate_validation.json"
VALIDATION_MD = ROOT / "reports" / "loop" / "latest_authorized_repair_apply_gate_validation.md"

REQUIRED_GATE_KEYS = [
    "apply_gate_id",
    "source_dry_run_id",
    "gate_state",
    "apply_authority",
    "human_authorization_present",
    "target_writes_performed",
    "api_writes_performed",
    "git_commits_performed",
    "rollback_required",
    "rollback_ready",
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
        findings.append("missing_apply_gate_report")
    if report != copy:
        findings.append("output_report_copy_mismatch")
    if not REPORT_MD.exists():
        findings.append("missing_markdown_report")
    if report.get("schema") != "CMS-SA-v0.4.6-authorized-repair-apply-gate-and-rollback-ledger":
        findings.append("schema_mismatch")
    if report.get("version") != "v0.4.6":
        findings.append("version_mismatch")
    if report.get("passed") is not True:
        findings.append("source_report_not_passing")
    for key in ["target_writes_performed", "api_writes_performed", "git_commits_performed", "git_pushes_performed", "release_tags_created"]:
        if report.get(key) != 0:
            findings.append(f"{key}_nonzero")
    if not str(report.get("primary_lock", "")).startswith("No repair apply may execute"):
        findings.append("primary_lock_missing_or_wrong")

    gates = report.get("gates", [])
    if not isinstance(gates, list) or not gates:
        findings.append("no_apply_gates")
        gates = []

    rollbacks = report.get("rollback_ledger", [])
    if not isinstance(rollbacks, list) or len(rollbacks) != len(gates):
        findings.append("rollback_ledger_count_mismatch")
        rollbacks = []

    for gate in gates:
        if not isinstance(gate, dict):
            findings.append("gate_not_object")
            continue
        gate_id = gate.get("apply_gate_id", "unknown")
        for key in REQUIRED_GATE_KEYS:
            if key not in gate or gate.get(key) in ("", None):
                findings.append(f"gate_missing:{gate_id}:{key}")
        if gate.get("apply_authority") is not False:
            findings.append(f"apply_authority_not_false:{gate_id}")
        if gate.get("human_authorization_present") is not False:
            findings.append(f"authorization_unexpectedly_present:{gate_id}")
        if gate.get("target_writes_performed") != 0:
            findings.append(f"target_writes_performed_nonzero:{gate_id}")
        if gate.get("rollback_required") is not True:
            findings.append(f"rollback_not_required:{gate_id}")
        if gate.get("rollback_ready") is not False:
            findings.append(f"rollback_ready_without_apply:{gate_id}")
        blocked = gate.get("blocked_actions_preserved", [])
        for action in ["autonomous_patch", "api_write", "silent_target_write", "unreviewed_git_commit", "unreviewed_git_push"]:
            if action not in blocked:
                findings.append(f"blocked_action_not_preserved:{gate_id}:{action}")

    validation = {
        "schema": "CMS-SA-v0.4.6-authorized-repair-apply-gate-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "findings": findings,
        "apply_gate_count": report.get("apply_gate_count", 0),
        "rollback_ledger_count": report.get("rollback_ledger_count", 0),
        "source_pressure_state": report.get("source_pressure_state"),
        "target_writes_performed": report.get("target_writes_performed"),
        "api_writes_performed": report.get("api_writes_performed"),
        "git_commits_performed": report.get("git_commits_performed"),
        "git_pushes_performed": report.get("git_pushes_performed"),
        "release_tags_created": report.get("release_tags_created"),
        "apply_gate_hash": report.get("apply_gate_hash"),
        "primary_lock": report.get("primary_lock"),
        "non_claim_lock": "Authorized apply gate validation is repository-bound and does not prove code correctness.",
    }

    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    findings_md = "\n".join(f"- `{x}`" for x in findings) if findings else "- none"
    VALIDATION_MD.write_text(
        "# CMS-SA v0.4.6 Authorized Repair Apply Gate Validation\n\n"
        f"- passed: `{str(validation['passed']).lower()}`\n"
        f"- errors: `{validation['errors']}`\n"
        f"- apply gate count: `{validation['apply_gate_count']}`\n"
        f"- rollback ledger count: `{validation['rollback_ledger_count']}`\n"
        f"- target writes performed: `{validation['target_writes_performed']}`\n"
        f"- api writes performed: `{validation['api_writes_performed']}`\n"
        f"- git commits performed: `{validation['git_commits_performed']}`\n\n"
        "## Primary Lock\n\n"
        + str(validation.get("primary_lock", ""))
        + "\n\n## Findings\n\n"
        + findings_md
        + "\n\n## Non-Claim Lock\n\nAuthorized apply gate validation is repository-bound and does not prove code correctness.\n",
        encoding="utf-8",
    )
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())