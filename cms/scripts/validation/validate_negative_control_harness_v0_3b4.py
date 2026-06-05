
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "outputs" / "controls" / "latest_negative_control_harness.json"
VALIDATION_JSON = ROOT / "reports" / "controls" / "latest_negative_control_validation.json"
VALIDATION_MD = ROOT / "reports" / "controls" / "latest_negative_control_validation.md"
REQUIRED_CLASSES = {"positive_control", "negative_control", "false_promote_control", "downgrade_control", "observe_only_control"}
VALID_DECISIONS = {"promote", "block", "downgrade", "observe_only"}

def main() -> int:
    findings: list[str] = []
    obj: dict = {}
    if not REPORT.exists():
        findings.append("missing_outputs_controls_latest_negative_control_harness_json")
    else:
        obj = json.loads(REPORT.read_text(encoding="utf-8"))
    if obj.get("schema") != "CMS-SA-v0.3b4-negative-control-harness":
        findings.append("schema_mismatch")
    if obj.get("version") != "v0.3b4":
        findings.append("version_mismatch")
    controls = obj.get("controls", [])
    if not isinstance(controls, list) or not controls:
        findings.append("missing_controls")
        controls = []
    observed_classes = {item.get("control_class") for item in controls if isinstance(item, dict)}
    for control_class in sorted(REQUIRED_CLASSES - observed_classes):
        findings.append(f"missing_control_class:{control_class}")
    for item in controls:
        if not isinstance(item, dict):
            findings.append("control_not_object")
            continue
        cid = item.get("control_id", "unknown_control")
        if item.get("expected_decision") not in VALID_DECISIONS:
            findings.append(f"{cid}:invalid_expected_decision")
        if item.get("observed_decision") not in VALID_DECISIONS:
            findings.append(f"{cid}:invalid_observed_decision")
        if item.get("passed") is not True:
            findings.append(f"{cid}:control_failed")
        if item.get("control_class") == "false_promote_control" and item.get("observed_decision") == "promote":
            findings.append(f"{cid}:false_promote_not_rejected")
        if not item.get("downgrade_path"):
            findings.append(f"{cid}:missing_downgrade_path")
        if not item.get("falsification_condition"):
            findings.append(f"{cid}:missing_falsification_condition")
        if "does not prove" not in str(item.get("non_claim_lock", "")):
            findings.append(f"{cid}:missing_non_claim_lock")
    if obj.get("false_promote_rejected") is not True:
        findings.append("false_promote_rejected_not_true")
    if obj.get("downgrade_preserved") is not True:
        findings.append("downgrade_preserved_not_true")
    if obj.get("observe_only_preserved") is not True:
        findings.append("observe_only_preserved_not_true")
    if not obj.get("harness_hash"):
        findings.append("missing_harness_hash")
    passed = len(findings) == 0 and obj.get("passed") is True
    result = {
        "schema": "CMS-SA-v0.3b4-negative-control-validation",
        "passed": passed,
        "version": obj.get("version"),
        "errors": len(findings),
        "findings": findings,
        "control_count": len(controls),
        "false_promote_rejected": obj.get("false_promote_rejected"),
        "downgrade_preserved": obj.get("downgrade_preserved"),
        "observe_only_preserved": obj.get("observe_only_preserved"),
        "harness_hash": obj.get("harness_hash"),
        "non_claim_lock": "Negative control validation is repository-bound and does not prove code correctness.",
    }
    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# CMS-SA v0.3b4 Negative Control Validation",
        "",
        f"- passed: `{passed}`",
        f"- errors: `{len(findings)}`",
        f"- control_count: `{result['control_count']}`",
        f"- false_promote_rejected: `{result['false_promote_rejected']}`",
        f"- downgrade_preserved: `{result['downgrade_preserved']}`",
        f"- observe_only_preserved: `{result['observe_only_preserved']}`",
        f"- harness_hash: `{result['harness_hash']}`",
        "",
        "## Findings",
        "",
    ]
    lines.extend([f"- `{finding}`" for finding in findings] if findings else ["- none"])
    lines.extend(["", "## Non-Claim Lock", "", result["non_claim_lock"], ""])
    VALIDATION_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 1

if __name__ == "__main__":
    raise SystemExit(main())
