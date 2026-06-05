from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "outputs/rehydration/latest_thread_rehydration_score.json"
OUT_JSON = ROOT / "reports/rehydration/latest_thread_rehydration_score_validation.json"
OUT_MD = ROOT / "reports/rehydration/latest_thread_rehydration_score_validation.md"


def main() -> int:
    findings: list[str] = []
    obj = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else {}
    if obj.get("schema") != "CMS-SA-v0.4.1-thread-rehydration-score":
        findings.append("schema_mismatch")
    if obj.get("version") != "v0.4.1":
        findings.append("version_mismatch")
    for key in ["origin_scan_complete", "architecture_scan_complete", "runtime_scan_complete", "version_ready"]:
        if obj.get(key) is not True:
            findings.append(f"{key}_not_true")
    if obj.get("missing_surfaces"):
        findings.append("missing_surfaces_present")
    if float(obj.get("rehydration_score", 0.0)) < 1.0:
        findings.append("rehydration_score_below_1")
    if "does not prove" not in str(obj.get("non_claim_lock", "")):
        findings.append("missing_non_claim_lock")

    passed = len(findings) == 0
    result = {
        "schema": "CMS-SA-v0.4.1-thread-rehydration-score-validation",
        "passed": passed,
        "version": "v0.4.1",
        "errors": len(findings),
        "findings": findings,
        "non_claim_lock": "Thread rehydration score validation is repository-bound and does not prove code correctness.",
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = ["# CMS-SA v0.4.1 Thread Rehydration Score Validation", "", f"- passed: `{passed}`", f"- errors: `{len(findings)}`", "", "## Findings", ""]
    lines.extend([f"- `{x}`" for x in findings] if findings else ["- none"])
    lines.extend(["", "## Non-Claim Lock", "", result["non_claim_lock"], ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
