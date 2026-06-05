
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "outputs" / "alignment" / "latest_multilevel_alignment_report.json"
REPORT_COPY = ROOT / "reports" / "alignment" / "latest_multilevel_alignment_report.json"
VALIDATION_JSON = ROOT / "reports" / "alignment" / "latest_multilevel_alignment_validation.json"
VALIDATION_MD = ROOT / "reports" / "alignment" / "latest_multilevel_alignment_validation.md"
REGISTRY = ROOT / "outputs" / "version_registry" / "cms_version_registry.json"

def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))

def main() -> int:
    findings = []
    report = load_json(REPORT)
    report_copy = load_json(REPORT_COPY)
    registry = load_json(REGISTRY)
    current_version = str(registry.get("current_version") or registry.get("latest_version") or "unknown")
    mode = str(report.get("seal_mode") or "preseal")
    if not report:
        findings.append("missing_multilevel_alignment_report")
    if report != report_copy:
        findings.append("alignment_report_copy_mismatch")
    expected_schema = "CMS-SA-" + current_version + "-multilevel-alignment-report"
    if report.get("schema") != expected_schema:
        findings.append("schema_mismatch:" + str(report.get("schema")))
    if report.get("version") != current_version:
        findings.append("version_mismatch:" + str(report.get("version")))
    if report.get("passed") is not True:
        findings.append("alignment_report_not_passing")
    if report.get("current_registry_version") != current_version:
        findings.append("registry_version_mismatch:" + str(report.get("current_registry_version")))
    layers = report.get("layers", {})
    for layer_name in ("root_readme", "mini_readmes", "route_maps", "validators", "reports", "reflective_git_geometry", "feedback_lifecycle", "loop_drift_pressure", "version_registry", "public_sync", "release_seal", "negative_controls", "memory_promotion"):
        layer = layers.get(layer_name)
        if not layer:
            findings.append("missing_layer:" + layer_name)
        elif layer.get("passed") is not True:
            findings.append("layer_not_passing:" + layer_name)
    version_checks = report.get("version_checks", {})
    for key in ("readme_contains_current_version", "readme_contains_previous_version", "surface_alignment_passed", "loop_drift_pressure_report_present", "loop_drift_pressure_under_threshold", "public_sync_report_present", "public_sync_accepted_for_current_phase", "geometry_registry_version_matches", "feedback_report_present"):
        if version_checks.get(key) is not True:
            findings.append("version_check_failed:" + key)
    public_sync_phase = report.get("public_sync_phase", {})
    if mode == "postseal" and public_sync_phase.get("phase_state") != "postseal_passed":
        findings.append("postseal_public_sync_not_passed")
    validation = {
        "schema": "CMS-SA-" + current_version + "-multilevel-alignment-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "warnings": 0,
        "findings": findings,
        "seal_mode": mode,
        "pressure_findings": report.get("pressure_findings", []),
        "feedback_items_checked": report.get("feedback_items_checked", 0),
        "feedback_items_aligned": report.get("feedback_items_aligned", 0),
        "layer_count": len(layers),
        "registry_derived": True,
        "non_claim_lock": "Multi-level alignment validation checks repository-bound alignment only. It does not prove code correctness.",
    }
    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md = [
        "# CMS-SA " + current_version + " Multi-Level Alignment Validation",
        "",
        "| Field | Value |",
        "|---|---|",
        "| passed | `" + str(validation["passed"]).lower() + "` |",
        "| errors | `" + str(validation["errors"]) + "` |",
        "| warnings | `0` |",
        "| seal mode | `" + mode + "` |",
        "| layer count | `" + str(validation["layer_count"]) + "` |",
        "| registry derived | `true` |",
        "",
        "Non-claim lock: multi-level alignment validation checks repository-bound alignment only. It does not prove code correctness.",
        "",
    ]
    if findings:
        md += ["## Findings", ""]
        md += ["- `" + finding + "`" for finding in findings]
        md.append("")
    if validation["pressure_findings"]:
        md += ["## Pressure Findings", ""]
        md += ["- `" + finding + "`" for finding in validation["pressure_findings"]]
        md.append("")
    VALIDATION_MD.write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(validation, indent=2, sort_keys=True))
    return 0 if validation["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
