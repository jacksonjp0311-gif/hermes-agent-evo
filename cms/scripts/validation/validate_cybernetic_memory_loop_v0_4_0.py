from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "outputs/loop/latest_cybernetic_memory_loop.json"
VALIDATION_JSON = ROOT / "reports/loop/latest_cybernetic_memory_loop_validation.json"
VALIDATION_MD = ROOT / "reports/loop/latest_cybernetic_memory_loop_validation.md"


def main() -> int:
    findings: list[str] = []
    if not REPORT.exists():
        findings.append("missing_outputs_loop_latest_cybernetic_memory_loop_json")
        obj = {}
    else:
        obj = json.loads(REPORT.read_text(encoding="utf-8"))
    if obj.get("schema") != "CMS-SA-v0.4.0-cybernetic-memory-loop":
        findings.append("schema_mismatch")
    if obj.get("version") != "v0.4.0":
        findings.append("version_mismatch")
    if obj.get("loop_closed") is not True:
        findings.append("loop_not_closed")
    if obj.get("passed") is not True:
        findings.append("loop_report_not_passing")
    if not obj.get("loop_hash"):
        findings.append("missing_loop_hash")
    memory_counts = obj.get("memory_counts", {})
    if int(memory_counts.get("promoted_count", 0)) < 1:
        findings.append("missing_promoted_memory_influence")
    if int(memory_counts.get("downgraded_count", 0)) < 1:
        findings.append("missing_downgraded_memory_visibility")
    if int(memory_counts.get("observe_only_count", 0)) < 1:
        findings.append("missing_observe_only_memory_boundary")
    control = obj.get("control_state", {})
    for key in ["false_promote_rejected", "downgrade_preserved", "observe_only_preserved"]:
        if control.get(key) is not True:
            findings.append(f"control_state_not_true:{key}")
    influence = obj.get("next_cycle_influence", {})
    if influence.get("allowed") is not True:
        findings.append("next_cycle_influence_not_allowed")
    if "no_api_write" not in str(influence.get("hard_boundary", "")):
        findings.append("missing_no_api_write_boundary")
    if "does not prove" not in str(obj.get("non_claim_lock", "")):
        findings.append("missing_non_claim_lock")
    passed = len(findings) == 0
    result = {
        "schema": "CMS-SA-v0.4.0-cybernetic-memory-loop-validation",
        "passed": passed,
        "version": obj.get("version"),
        "errors": len(findings),
        "findings": findings,
        "loop_hash": obj.get("loop_hash"),
        "non_claim_lock": "Cybernetic memory loop validation is repository-bound and does not prove code correctness.",
    }
    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# CMS-SA v0.4.0 Cybernetic Memory Loop Validation", "", f"- passed: `{passed}`", f"- errors: `{len(findings)}`", f"- loop_hash: `{result['loop_hash']}`", "", "## Findings", ""]
    lines.extend([f"- `{x}`" for x in findings] if findings else ["- none"])
    lines.extend(["", "## Non-Claim Lock", "", result["non_claim_lock"], ""])
    VALIDATION_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
