from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "outputs/memory/latest_candidate_memory_actions.json"
OUT_JSON = ROOT / "reports/memory/latest_candidate_memory_actions_validation.json"
OUT_MD = ROOT / "reports/memory/latest_candidate_memory_actions_validation.md"

REQUIRED = [
    "candidate_id",
    "memory_decision",
    "allowed_next_action",
    "blocked_actions",
    "required_evidence_next",
    "downgrade_visibility_required",
    "observe_only_recheck_condition",
    "rehydration_visible",
    "non_claim_lock",
]


def has_non_claim_lock(value: str) -> bool:
    text = str(value)
    return ("does not prove" in text) or ("do not prove" in text)


def main() -> int:
    findings: list[str] = []
    obj = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else {}
    if obj.get("schema") != "CMS-SA-v0.4.1-candidate-memory-action-report":
        findings.append("schema_mismatch")
    if obj.get("version") != "v0.4.1":
        findings.append("version_mismatch")
    actions = obj.get("actions", [])
    if not isinstance(actions, list) or not actions:
        findings.append("missing_actions")
        actions = []
    for action in actions:
        cid = action.get("candidate_id", "unknown")
        for key in REQUIRED:
            if key not in action:
                findings.append(f"{cid}:missing_{key}")
        if action.get("memory_decision") == "promote_memory" and action.get("rehydration_visible") is not True:
            findings.append(f"{cid}:promoted_not_rehydration_visible")
        if not has_non_claim_lock(str(action.get("non_claim_lock", ""))):
            findings.append(f"{cid}:missing_non_claim_lock")
    if obj.get("candidate_action_count") != len(actions):
        findings.append("candidate_action_count_mismatch")
    if not obj.get("action_hash"):
        findings.append("missing_action_hash")
    if not has_non_claim_lock(str(obj.get("non_claim_lock", ""))):
        findings.append("report_missing_non_claim_lock")

    passed = len(findings) == 0
    result = {
        "schema": "CMS-SA-v0.4.1-candidate-memory-action-validation",
        "passed": passed,
        "version": "v0.4.1",
        "errors": len(findings),
        "findings": findings,
        "candidate_action_count": len(actions),
        "non_claim_lock": "Candidate memory action validation is repository-bound and does not prove code correctness.",
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# CMS-SA v0.4.1 Candidate Memory Action Validation", "", f"- passed: `{passed}`", f"- errors: `{len(findings)}`", "", "## Findings", ""]
    lines.extend([f"- `{x}`" for x in findings] if findings else ["- none"])
    lines.extend(["", "## Non-Claim Lock", "", result["non_claim_lock"], ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
