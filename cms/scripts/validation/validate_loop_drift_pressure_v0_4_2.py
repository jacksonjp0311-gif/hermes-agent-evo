from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "outputs/loop/latest_loop_drift_pressure.json"
OUT_JSON = ROOT / "reports/loop/latest_loop_drift_pressure_validation.json"
OUT_MD = ROOT / "reports/loop/latest_loop_drift_pressure_validation.md"

REQUIRED_COMPONENTS = [
    "memory_action_drift",
    "rehydration_gap_count",
    "rehydration_gap_pressure",
    "registry_status_drift",
    "public_surface_delta",
    "validator_expectation_drift",
    "non_claim_lock_drift",
    "report_surface_lag",
]


def has_non_claim_lock(value: str) -> bool:
    text = str(value)
    return ("does not prove" in text) or ("do not prove" in text)


def main() -> int:
    findings: list[str] = []
    obj = json.loads(REPORT.read_text(encoding="utf-8")) if REPORT.exists() else {}

    if obj.get("schema") != "CMS-SA-v0.4.2-loop-drift-pressure-report":
        findings.append("schema_mismatch")
    if obj.get("version") != "v0.4.2":
        findings.append("version_mismatch")

    pressure = obj.get("loop_drift_pressure")
    threshold = obj.get("threshold")
    if not isinstance(pressure, (int, float)):
        findings.append("missing_loop_drift_pressure")
        pressure = 1.0
    if not isinstance(threshold, (int, float)):
        findings.append("missing_threshold")
        threshold = 0.25

    components = obj.get("components", {})
    if not isinstance(components, dict):
        findings.append("missing_components")
        components = {}

    for key in REQUIRED_COMPONENTS:
        if key not in components:
            findings.append(f"missing_component:{key}")

    if pressure > threshold and obj.get("stability_state") != "pressure_exceeds_threshold":
        findings.append("pressure_above_threshold_without_pressure_state")

    if pressure <= threshold and obj.get("recommended_action") not in {
        "continue_to_next_layer_after_validation",
        "repair_pressure_findings_before_release_seal",
    }:
        findings.append("unexpected_recommended_action_for_bounded_pressure")

    if not obj.get("pressure_hash"):
        findings.append("missing_pressure_hash")

    primary_lock = obj.get("primary_lock")
    if not primary_lock or "No green loop is considered stable" not in str(primary_lock):
        findings.append("missing_primary_lock")

    if not has_non_claim_lock(str(obj.get("non_claim_lock", ""))):
        findings.append("missing_non_claim_lock")

    passed = len(findings) == 0
    result = {
        "schema": "CMS-SA-v0.4.2-loop-drift-pressure-validation",
        "passed": passed,
        "version": "v0.4.2",
        "errors": len(findings),
        "findings": findings,
        "loop_drift_pressure": pressure,
        "threshold": threshold,
        "stability_state": obj.get("stability_state"),
        "non_claim_lock": "Loop drift pressure validation is repository-bound and does not prove code correctness.",
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# CMS-SA v0.4.2 Loop Drift Pressure Validation",
        "",
        f"- passed: `{passed}`",
        f"- errors: `{len(findings)}`",
        f"- loop_drift_pressure: `{pressure}`",
        f"- threshold: `{threshold}`",
        f"- stability_state: `{obj.get('stability_state')}`",
        "",
        "## Findings",
        "",
    ]
    lines.extend([f"- `{x}`" for x in findings] if findings else ["- none"])
    lines.extend(["", "## Non-Claim Lock", "", result["non_claim_lock"], ""])
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
