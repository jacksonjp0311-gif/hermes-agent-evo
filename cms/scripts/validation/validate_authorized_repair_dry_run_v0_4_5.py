from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "outputs" / "loop" / "latest_authorized_repair_dry_run.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_authorized_repair_dry_run.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_authorized_repair_dry_run.md"
VALIDATION_JSON = ROOT / "reports" / "loop" / "latest_authorized_repair_dry_run_validation.json"
VALIDATION_MD = ROOT / "reports" / "loop" / "latest_authorized_repair_dry_run_validation.md"

REQUIRED_KEYS = [
    "dry_run_id",
    "source_plan_id",
    "repair_class",
    "execution_mode",
    "write_authority",
    "human_authorization_required_for_write",
    "target_surface_writes",
    "touched_surface_boundary",
    "required_validation_evidence",
    "rollback_path",
    "blocked_actions_preserved",
    "dry_run_state",
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
        findings.append("missing_authorized_dry_run_report")
    if report != copy:
        findings.append("output_report_copy_mismatch")
    if not REPORT_MD.exists():
        findings.append("missing_markdown_report")
    if report.get("schema") != "CMS-SA-v0.4.5-authorized-repair-dry-run-executor":
        findings.append("schema_mismatch")
    if report.get("version") != "v0.4.5":
        findings.append("version_mismatch")
    if report.get("passed") is not True:
        findings.append("source_report_not_passing")
    if report.get("target_writes_performed") != 0:
        findings.append("target_writes_performed_nonzero")
    if report.get("api_writes_performed") != 0:
        findings.append("api_writes_performed_nonzero")
    if report.get("commits_performed") != 0:
        findings.append("commits_performed_nonzero")
    if not str(report.get("primary_lock", "")).startswith("No repair dry-run may write target surfaces"):
        findings.append("primary_lock_missing_or_wrong")

    dry_runs = report.get("dry_runs", [])
    if not isinstance(dry_runs, list) or not dry_runs:
        findings.append("no_dry_runs")
        dry_runs = []

    for item in dry_runs:
        if not isinstance(item, dict):
            findings.append("dry_run_not_object")
            continue
        dry_id = item.get("dry_run_id", "unknown")
        for key in REQUIRED_KEYS:
            if key not in item or item.get(key) in ("", None):
                findings.append(f"dry_run_missing:{dry_id}:{key}")
        if item.get("write_authority") is not False:
            findings.append(f"write_authority_not_false:{dry_id}")
        if item.get("target_surface_writes") != []:
            findings.append(f"target_surface_writes_not_empty:{dry_id}")
        if item.get("human_authorization_required_for_write") is not True:
            findings.append(f"human_authorization_not_required:{dry_id}")
        blocked = item.get("blocked_actions_preserved", [])
        for action in ["autonomous_patch", "api_write", "git_commit", "git_push"]:
            if action not in blocked:
                findings.append(f"blocked_action_not_preserved:{dry_id}:{action}")

    validation = {
        "schema": "CMS-SA-v0.4.5-authorized-repair-dry-run-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "findings": findings,
        "dry_run_count": report.get("dry_run_count", 0),
        "source_pressure_state": report.get("source_pressure_state"),
        "target_writes_performed": report.get("target_writes_performed"),
        "api_writes_performed": report.get("api_writes_performed"),
        "commits_performed": report.get("commits_performed"),
        "dry_run_hash": report.get("dry_run_hash"),
        "primary_lock": report.get("primary_lock"),
        "non_claim_lock": "Authorized dry-run validation is repository-bound and does not prove code correctness.",
    }

    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    findings_md = "\n".join(f"- `{x}`" for x in findings) if findings else "- none"
    VALIDATION_MD.write_text(
        "# CMS-SA v0.4.5 Authorized Repair Dry-Run Validation\n\n"
        f"- passed: `{str(validation['passed']).lower()}`\n"
        f"- errors: `{validation['errors']}`\n"
        f"- dry-run count: `{validation['dry_run_count']}`\n"
        f"- target writes performed: `{validation['target_writes_performed']}`\n"
        f"- api writes performed: `{validation['api_writes_performed']}`\n"
        f"- commits performed: `{validation['commits_performed']}`\n\n"
        "## Primary Lock\n\n"
        + str(validation.get("primary_lock", ""))
        + "\n\n## Findings\n\n"
        + findings_md
        + "\n\n## Non-Claim Lock\n\nAuthorized dry-run validation is repository-bound and does not prove code correctness.\n",
        encoding="utf-8",
    )
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())