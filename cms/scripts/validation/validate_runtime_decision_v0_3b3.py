
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path.cwd(); VERSION = "v0.3b3"
DECISION = ROOT / "outputs/decision/latest_runtime_decision.json"
LEDGER = ROOT / "outputs/replay/runtime_decision_replay_ledger.jsonl"
REPORT_JSON = ROOT / "reports/decision/latest_runtime_decision_validation.json"
REPORT_MD = ROOT / "reports/decision/latest_runtime_decision_validation.md"
ALLOWED = {"promote", "block", "downgrade", "observe_only"}


def write_reports(result: dict) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    findings = result.get("findings") or []
    lines = ["# Runtime Decision Validation", "", f"- Passed: `{result['passed']}`", f"- Errors: `{result['errors']}`", "", "## Findings", ""]
    lines += [f"- `{x}`" for x in findings] if findings else ["- none"]
    lines += ["", result["non_claim_lock"], ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    findings = []
    if not DECISION.exists():
        findings.append("missing_runtime_decision")
        data = {}
    else:
        data = json.loads(DECISION.read_text(encoding="utf-8"))
    if data:
        if data.get("schema") != "CMS-SA-v0.3b3-runtime-decision": findings.append("schema_mismatch")
        if data.get("version") != VERSION: findings.append(f"version_mismatch:{data.get('version')}")
        if data.get("decision") not in ALLOWED: findings.append(f"invalid_decision:{data.get('decision')}")
        if not data.get("decision_hash"): findings.append("missing_decision_hash")
        for item in data.get("signals", []):
            if item.get("required") and item.get("passed") is not True:
                findings.append(f"required_signal_failed:{item.get('name')}")
        if data.get("decision") == "promote" and data.get("required_failures"):
            findings.append("promote_with_required_failures")
        if not LEDGER.exists() or data.get("decision_hash") not in LEDGER.read_text(encoding="utf-8", errors="replace"):
            findings.append("decision_hash_missing_from_replay_ledger")
    result = {"schema": "CMS-SA-v0.3b3-runtime-decision-validation", "passed": len(findings) == 0, "version": VERSION, "errors": len(findings), "findings": findings, "decision": data.get("decision"), "decision_hash": data.get("decision_hash"), "non_claim_lock": "Runtime decision validation is repository-bound and does not prove code correctness."}
    write_reports(result)
    print(json.dumps(result, indent=2))
    if findings: raise SystemExit(1)

if __name__ == "__main__": main()
