from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]


GEOMETRY_JSON = ROOT / "outputs" / "geometry" / "latest_reflective_git_geometry.json"
REPORT_JSON = ROOT / "reports" / "geometry" / "latest_reflective_git_geometry.json"
REPORT_MD = ROOT / "reports" / "geometry" / "latest_reflective_git_geometry.md"
VALIDATION_JSON = ROOT / "reports" / "geometry" / "latest_reflective_git_geometry_validation.json"
VALIDATION_MD = ROOT / "reports" / "geometry" / "latest_reflective_git_geometry_validation.md"


def sha256(path: Path) -> str:
    if not path.exists():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    findings: list[str] = []

    before_hashes = {
        "outputs_geometry": sha256(GEOMETRY_JSON),
        "reports_geometry_json": sha256(REPORT_JSON),
        "reports_geometry_md": sha256(REPORT_MD),
    }

    if not GEOMETRY_JSON.exists():
        findings.append("missing_outputs_geometry_json")
        geometry: dict[str, Any] = {}
    else:
        geometry = load_json(GEOMETRY_JSON)

    if not REPORT_JSON.exists():
        findings.append("missing_reports_geometry_json")
    else:
        report_geometry = load_json(REPORT_JSON)
        if report_geometry != geometry:
            findings.append("geometry_json_report_mismatch")

    if not REPORT_MD.exists():
        findings.append("missing_reports_geometry_md")

    if geometry.get("schema") != "CMS-SA-v0.3a2-reflective-git-geometry":
        findings.append("schema_mismatch")

    if geometry.get("node_count", 0) < 1:
        findings.append("no_geometry_nodes")

    if geometry.get("stable_geometry_boundary") is not True:
        findings.append("stable_geometry_boundary_missing")

    if geometry.get("report_refresh_commits_excluded") is not True:
        findings.append("report_refresh_exclusion_missing")

    if geometry.get("pure_validation_boundary") is not True:
        findings.append("pure_validation_boundary_missing")

    if geometry.get("emission_validation_split") is not True:
        findings.append("emission_validation_split_missing")

    truth = geometry.get("release_truth", {})
    if truth.get("head_origin_match") is not True:
        findings.append("head_origin_mismatch")

    if truth.get("readme_checkpoint_present") is not True:
        findings.append("readme_checkpoint_missing")

    nodes = geometry.get("nodes", [])
    for index, node in enumerate(nodes):
        for key in (
            "commit_hash",
            "short_hash",
            "message",
            "changed_files",
            "surface_classes",
            "shells",
            "meridians",
            "sectors",
            "release_truth",
        ):
            if key not in node:
                findings.append(f"node_{index}_missing_{key}")

    after_hashes = {
        "outputs_geometry": sha256(GEOMETRY_JSON),
        "reports_geometry_json": sha256(REPORT_JSON),
        "reports_geometry_md": sha256(REPORT_MD),
    }

    read_only_geometry_preserved = before_hashes == after_hashes
    if not read_only_geometry_preserved:
        findings.append("validator_mutated_geometry_artifacts")

    report = {
        "schema": "CMS-SA-v0.3a2-reflective-git-geometry-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "warnings": 0,
        "findings": findings,
        "node_count": geometry.get("node_count", 0),
        "current_registry_version": geometry.get("current_registry_version"),
        "stable_geometry_boundary": geometry.get("stable_geometry_boundary"),
        "report_refresh_commits_excluded": geometry.get("report_refresh_commits_excluded"),
        "pure_validation_boundary": geometry.get("pure_validation_boundary"),
        "emission_validation_split": geometry.get("emission_validation_split"),
        "read_only_geometry_preserved": read_only_geometry_preserved,
        "core_law_present": geometry.get("core_law") == "A commit is not only a change; it is a routed event in repository geometry.",
        "non_claim_lock": "Reflective Git geometry validation is read-only for latest geometry artifacts. It does not prove runtime correctness.",
    }

    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    md = [
        "# CMS-SA v0.3a2 Reflective Git Geometry Validation",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(report['passed']).lower()}` |",
        f"| errors | `{report['errors']}` |",
        f"| warnings | `0` |",
        f"| node count | `{report['node_count']}` |",
        f"| current registry version | `{report['current_registry_version']}` |",
        f"| stable geometry boundary | `{str(report['stable_geometry_boundary']).lower()}` |",
        f"| report refresh commits excluded | `{str(report['report_refresh_commits_excluded']).lower()}` |",
        f"| pure validation boundary | `{str(report['pure_validation_boundary']).lower()}` |",
        f"| emission validation split | `{str(report['emission_validation_split']).lower()}` |",
        f"| read-only geometry preserved | `{str(report['read_only_geometry_preserved']).lower()}` |",
        f"| core law present | `{str(report['core_law_present']).lower()}` |",
        "",
        "Non-claim lock: reflective Git geometry validation is read-only for latest geometry artifacts. It does not prove runtime correctness.",
        "",
    ]
    VALIDATION_MD.write_text("\n".join(md), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())