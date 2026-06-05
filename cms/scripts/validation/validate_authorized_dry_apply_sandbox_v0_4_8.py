from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_JSON = ROOT / "outputs" / "loop" / "latest_authorized_dry_apply_sandbox.json"
REPORT_JSON = ROOT / "reports" / "loop" / "latest_authorized_dry_apply_sandbox.json"
REPORT_MD = ROOT / "reports" / "loop" / "latest_authorized_dry_apply_sandbox.md"
VALIDATION_JSON = ROOT / "reports" / "loop" / "latest_authorized_dry_apply_sandbox_validation.json"
VALIDATION_MD = ROOT / "reports" / "loop" / "latest_authorized_dry_apply_sandbox_validation.md"

REQUIRED_RUN_KEYS = [
    "dry_apply_run_id",
    "source_apply_packet_id",
    "sandbox_state",
    "apply_authority",
    "rollback_simulation_passed",
    "live_target_writes_performed",
    "api_writes_performed",
    "git_commits_performed",
    "git_pushes_performed",
    "release_tags_created",
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
        findings.append("missing_dry_apply_sandbox_report")
    if report != copy:
        findings.append("output_report_copy_mismatch")
    if not REPORT_MD.exists():
        findings.append("missing_markdown_report")
    if report.get("schema") != "CMS-SA-v0.4.8-authorized-apply-executor-dry-apply-sandbox":
        findings.append("schema_mismatch")
    if report.get("version") != "v0.4.8":
        findings.append("version_mismatch")
    if report.get("passed") is not True:
        findings.append("source_report_not_passing")
    for key in ["live_target_writes_performed", "api_writes_performed", "git_commits_performed", "git_pushes_performed", "release_tags_created"]:
        if report.get(key) != 0:
            findings.append(f"{key}_nonzero")
    if not str(report.get("primary_lock", "")).startswith("No dry-apply sandbox may write live target surfaces"):
        findings.append("primary_lock_missing_or_wrong")

    runs = report.get("runs", [])
    if not isinstance(runs, list) or not runs:
        findings.append("no_dry_apply_runs")
        runs = []

    for run in runs:
        if not isinstance(run, dict):
            findings.append("run_not_object")
            continue
        run_id = run.get("dry_apply_run_id", "unknown")
        for key in REQUIRED_RUN_KEYS:
            if key not in run or run.get(key) in ("", None):
                findings.append(f"run_missing:{run_id}:{key}")
        if run.get("apply_authority") is not False:
            findings.append(f"apply_authority_not_false:{run_id}")
        if run.get("rollback_simulation_passed") is not True:
            findings.append(f"rollback_simulation_failed:{run_id}")
        for key in ["live_target_writes_performed", "api_writes_performed", "git_commits_performed", "git_pushes_performed", "release_tags_created"]:
            if run.get(key) != 0:
                findings.append(f"{key}_nonzero:{run_id}")
        blocked = run.get("blocked_actions_preserved", [])
        for action in ["live_target_write", "api_write", "git_commit", "git_push", "release_tag_creation"]:
            if action not in blocked:
                findings.append(f"blocked_action_not_preserved:{run_id}:{action}")

    validation = {
        "schema": "CMS-SA-v0.4.8-authorized-dry-apply-sandbox-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "findings": findings,
        "dry_apply_run_count": report.get("dry_apply_run_count", 0),
        "source_pressure_state": report.get("source_pressure_state"),
        "virtual_target_writes_performed": report.get("virtual_target_writes_performed"),
        "live_target_writes_performed": report.get("live_target_writes_performed"),
        "api_writes_performed": report.get("api_writes_performed"),
        "git_commits_performed": report.get("git_commits_performed"),
        "git_pushes_performed": report.get("git_pushes_performed"),
        "release_tags_created": report.get("release_tags_created"),
        "dry_apply_sandbox_hash": report.get("dry_apply_sandbox_hash"),
        "primary_lock": report.get("primary_lock"),
        "non_claim_lock": "Authorized dry-apply sandbox validation is repository-bound and does not prove code correctness.",
    }

    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    findings_md = "\n".join(f"- `{x}`" for x in findings) if findings else "- none"
    VALIDATION_MD.write_text(
        "# CMS-SA v0.4.8 Authorized Dry-Apply Sandbox Validation\n\n"
        f"- passed: `{str(validation['passed']).lower()}`\n"
        f"- errors: `{validation['errors']}`\n"
        f"- dry-apply run count: `{validation['dry_apply_run_count']}`\n"
        f"- virtual target writes performed: `{validation['virtual_target_writes_performed']}`\n"
        f"- live target writes performed: `{validation['live_target_writes_performed']}`\n"
        f"- api writes performed: `{validation['api_writes_performed']}`\n"
        f"- git commits performed: `{validation['git_commits_performed']}`\n\n"
        "## Primary Lock\n\n"
        + str(validation.get("primary_lock", ""))
        + "\n\n## Findings\n\n"
        + findings_md
        + "\n\n## Non-Claim Lock\n\nAuthorized dry-apply sandbox validation is repository-bound and does not prove code correctness.\n",
        encoding="utf-8",
    )
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())