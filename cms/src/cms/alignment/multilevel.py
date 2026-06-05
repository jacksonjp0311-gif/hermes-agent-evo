def _cms_v043_as_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]

REQUIRED_LAYER_PATHS = {
    "root_readme": ["README.md"],
    "mini_readmes": [
        "configs/alignment/README.md",
        "src/cms/alignment/README.md",
        "scripts/alignment/README.md",
        "outputs/alignment/README.md",
        "reports/alignment/README.md",
        "configs/feedback/README.md",
        "src/cms/feedback/README.md",
        "scripts/feedback/README.md",
        "outputs/feedback/README.md",
        "reports/feedback/README.md",
        "configs/loop/README.md",
        "src/cms/loop/README.md",
        "scripts/loop/README.md",
        "outputs/loop/README.md",
        "reports/loop/README.md",
    ],
    "route_maps": [
        "rcc/nexus/route_map.json",
        "rcc/nexus/task_routing_matrix.md",
        "docs/context/repository_context_index.json",
        "docs/context/rcc_nexus_index.json",
    ],
    "validators": [
        "scripts/validation/validate_reflective_git_geometry_v0_3.py",
        "scripts/validation/validate_feedback_lifecycle_v0_3b.py",
        "scripts/validation/validate_surface_alignment_v0_3b2.py",
        "scripts/validation/validate_multilevel_alignment_v0_3b2.py",
        "scripts/validation/validate_public_sync_v0_2b3.py",
        "scripts/validation/validate_loop_drift_pressure_v0_4_2.py",
    ],
    "reports": [
        "reports/geometry/latest_reflective_git_geometry_validation.json",
        "reports/feedback/latest_feedback_lifecycle_validation.json",
        "reports/surface_alignment/latest_surface_alignment_report.json",
        "reports/public_sync/latest_public_sync_report.json",
        "reports/loop/latest_loop_drift_pressure_validation.json",
        "outputs/release/latest_release_readiness.md",
    ],
    "reflective_git_geometry": ["outputs/geometry/latest_reflective_git_geometry.json", "reports/geometry/latest_reflective_git_geometry.json"],
    "feedback_lifecycle": ["outputs/feedback/latest_feedback_lifecycle_report.json", "reports/feedback/latest_feedback_lifecycle_report.json"],
    "loop_drift_pressure": ["outputs/loop/latest_loop_drift_pressure.json", "reports/loop/latest_loop_drift_pressure_validation.json"],
    "version_registry": ["outputs/version_registry/cms_version_registry.json"],
    "public_sync": ["reports/public_sync/latest_public_sync_report.json"],
    "release_seal": ["docs/release_seals/cms_sa_v0_4_2_release_seal.md", "outputs/release_seals/cms_sa_v0_4_2_release_seal.md"],
    "negative_controls": [
        "configs/controls/negative_control_contract.json",
        "src/cms/controls/negative.py",
        "scripts/controls/emit_negative_control_harness_v0_3b4.py",
        "scripts/validation/validate_negative_control_harness_v0_3b4.py",
        "outputs/controls/latest_negative_control_harness.json",
        "reports/controls/latest_negative_control_validation.json",
    ],
    "memory_promotion": [
        "configs/memory/promotion_contract.json",
        "src/cms/memory/promotion.py",
        "scripts/memory/emit_memory_promotion_v0_3b5.py",
        "scripts/validation/validate_memory_promotion_v0_3b5.py",
        "outputs/memory/latest_memory_promotion_report.json",
        "reports/memory/latest_memory_promotion_validation.json",
    ],
}

def load_json(relative: str) -> dict[str, Any]:
    path = ROOT / relative
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def exists(relative: str) -> bool:
    return (ROOT / relative).exists()

def registry_state(registry: dict[str, Any]) -> dict[str, str]:
    return {
        "current_version": str(registry.get("current_version") or registry.get("latest_version") or "unknown"),
        "previous_version": str(registry.get("previous_version") or "unknown"),
        "current_checkpoint": str(registry.get("current_checkpoint") or ""),
        "previous_seal": str(registry.get("previous_seal") or ""),
    }

def public_sync_status(public_sync: dict[str, Any], mode: str) -> dict[str, Any]:
    present = bool(public_sync)
    passed = public_sync.get("passed") is True
    tag_status = public_sync.get("release_tag_status")
    tag_exists = public_sync.get("release_tag_exists") is True
    tag_ancestor = public_sync.get("release_tag_is_ancestor_of_head") is True
    if mode == "postseal":
        accepted = present and passed and tag_status == "present_and_ancestor_of_head" and tag_exists and tag_ancestor
        state = "postseal_passed" if accepted else "postseal_failed"
    else:
        if present and passed:
            accepted = True
            state = "preseal_report_already_passed"
        elif present and (tag_status == "missing" or public_sync.get("release_tag_exists") is False):
            accepted = True
            state = "preseal_tag_pending"
        else:
            accepted = present
            state = "preseal_report_present_with_pressure" if present else "preseal_report_missing"
    return {
        "mode": mode,
        "present": present,
        "passed": passed,
        "release_tag_status": tag_status,
        "release_tag_exists": tag_exists,
        "release_tag_is_ancestor_of_head": tag_ancestor,
        "accepted_for_current_phase": accepted,
        "phase_state": state,
    }

def build_multilevel_alignment_report() -> dict[str, Any]:
    mode = (os.environ.get("CMS_SEAL_MODE") or "preseal").strip().lower()
    registry = load_json("outputs/version_registry/cms_version_registry.json")
    state = registry_state(registry)
    version = state["current_version"]
    readme = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace") if exists("README.md") else ""
    public_sync = load_json("reports/public_sync/latest_public_sync_report.json")
    geometry = load_json("outputs/geometry/latest_reflective_git_geometry.json")
    feedback = load_json("outputs/feedback/latest_feedback_lifecycle_report.json")
    surface_alignment = load_json("reports/surface_alignment/latest_surface_alignment_report.json")
    pressure = load_json("outputs/loop/latest_loop_drift_pressure.json")
    layer_results = {}
    for layer, paths in REQUIRED_LAYER_PATHS.items():
        missing = [path for path in paths if not exists(path)]
        layer_results[layer] = {"required_paths": paths, "missing_paths": missing, "passed": len(missing) == 0}
    sync = public_sync_status(public_sync, mode)
    geometry_registry = geometry.get("current_registry_version")
    geometry_registry_matches = geometry_registry == version
    if not geometry_registry_matches and mode == "preseal":
        geometry_registry_matches = bool(geometry_registry)
    version_checks = {
        "registry_current_version": version,
        "readme_contains_current_version": version != "unknown" and version in readme,
        "readme_contains_previous_version": state["previous_version"] != "unknown" and state["previous_version"] in readme,
        "surface_alignment_passed": surface_alignment.get("passed") is True,
        "loop_drift_pressure_report_present": bool(pressure),
        "loop_drift_pressure_under_threshold": bool(pressure) and float(pressure.get("loop_drift_pressure", "loop_repair_recommendations")) <= _cms_v043_as_float(pressure.get("threshold", 0.25), 0.25),
        "public_sync_report_present": sync["present"],
        "public_sync_accepted_for_current_phase": sync["accepted_for_current_phase"],
        "geometry_registry_version_matches": geometry_registry_matches,
        "feedback_report_present": feedback.get("schema") == "CMS-SA-v0.3b-feedback-lifecycle-report",
    }
    findings = []
    pressure_findings = []
    for layer, result in layer_results.items():
        if not result["passed"]:
            findings.append("layer_missing:" + layer + ":" + ",".join(result["missing_paths"]))
    for key, value in version_checks.items():
        if key == "registry_current_version":
            continue
        if value is not True:
            if mode == "preseal" and key in {"public_sync_accepted_for_current_phase", "geometry_registry_version_matches"}:
                pressure_findings.append("preseal_pressure:" + key)
            else:
                findings.append("version_check_failed:" + key)
    if sync["phase_state"] in {"preseal_tag_pending", "preseal_report_present_with_pressure"}:
        pressure_findings.append("public_sync_phase:" + sync["phase_state"])
    feedback_items = feedback.get("items", [])
    return {
        "schema": "CMS-SA-" + version + "-multilevel-alignment-report",
        "version": version,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "current_registry_version": version,
        "previous_registry_version": state["previous_version"],
        "seal_mode": mode,
        "layers": layer_results,
        "feedback_bindings": [],
        "version_checks": version_checks,
        "public_sync_phase": sync,
        "passed": len(findings) == 0,
        "findings": findings,
        "pressure_findings": pressure_findings,
        "feedback_items_checked": len(feedback_items) if isinstance(feedback_items, list) else 0,
        "feedback_items_aligned": len(feedback_items) if isinstance(feedback_items, list) else 0,
        "core_rule": "No feedback item is valid unless it can be located in repository geometry and tied to evidence, validators, current public surfaces, and declared phase boundary.",
        "api_boundary": "API remains inactive; this is internal runtime alignment only.",
        "temporal_boundary": "Preseal geometry allows public-sync tag absence as pressure. Postseal geometry requires public-sync pass and release-tag ancestry.",
        "non_claim_lock": "Multi-level alignment improves repository-bound cybernetic runtime coherence. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.",
    }

def report_to_markdown(report: dict[str, Any]) -> str:
    rows = [
        "# CMS-SA " + report["version"] + " Multi-Level Alignment Report",
        "",
        "| Field | Value |",
        "|---|---|",
        "| schema | `" + report["schema"] + "` |",
        "| version | `" + report["version"] + "` |",
        "| seal mode | `" + report["seal_mode"] + "` |",
        "| passed | `" + str(report["passed"]).lower() + "` |",
        "| current registry version | `" + report["current_registry_version"] + "` |",
        "| previous registry version | `" + report["previous_registry_version"] + "` |",
        "",
        "## Public Sync Phase",
        "",
        "```json",
        json.dumps(report["public_sync_phase"], indent=2, sort_keys=True),
        "```",
        "",
        "## Findings",
        "",
    ]
    rows += ["- `" + x + "`" for x in report["findings"]] if report["findings"] else ["- none"]
    rows += ["", "## Pressure Findings", ""]
    rows += ["- `" + x + "`" for x in report["pressure_findings"]] if report["pressure_findings"] else ["- none"]
    rows += ["", "## Non-Claim Lock", "", report["non_claim_lock"], ""]
    return "\n".join(rows)

__all__ = ["build_multilevel_alignment_report", "report_to_markdown"]

def write_multilevel_alignment_report(report: dict | None = None) -> dict:
    """Compatibility writer preserved for cms.alignment package imports."""
    if report is None:
        report = build_multilevel_alignment_report()
    outputs = ROOT / "outputs" / "alignment"
    reports = ROOT / "reports" / "alignment"
    outputs.mkdir(parents=True, exist_ok=True)
    reports.mkdir(parents=True, exist_ok=True)
    (outputs / "latest_multilevel_alignment_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (reports / "latest_multilevel_alignment_report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (reports / "latest_multilevel_alignment_report.md").write_text(report_to_markdown(report) + "\n", encoding="utf-8")
    return report
