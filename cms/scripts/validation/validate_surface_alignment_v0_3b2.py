
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
REGISTRY = ROOT / "outputs" / "version_registry" / "cms_version_registry.json"
REPORT_JSON = ROOT / "reports" / "surface_alignment" / "latest_surface_alignment_report.json"
REPORT_MD = ROOT / "reports" / "surface_alignment" / "latest_surface_alignment_report.md"

MINI_README_EXPECTED = {
    "configs/alignment/README.md": "Multi-Level Alignment Contracts",
    "src/cms/alignment/README.md": "Multi-Level Alignment Runtime",
    "scripts/alignment/README.md": "Alignment Emitters",
    "outputs/alignment/README.md": "Alignment Outputs",
    "reports/alignment/README.md": "Alignment Reports",
    "configs/controls/README.md": "Control Contracts",
    "src/cms/controls/README.md": "Control Runtime",
    "scripts/controls/README.md": "Control Emitters",
    "outputs/controls/README.md": "Control Outputs",
    "reports/controls/README.md": "Control Reports",
    "configs/memory/README.md": "Memory Contracts",
    "src/cms/memory/README.md": "CMS Memory Runtime",
    "scripts/memory/README.md": "Memory Emitters",
    "outputs/memory/README.md": "Memory Outputs",
    "reports/memory/README.md": "Memory Reports",
    "configs/loop/README.md": "Loop Contracts",
    "src/cms/loop/README.md": "Loop Runtime",
    "scripts/loop/README.md": "Loop Emitters",
    "outputs/loop/README.md": "Loop Outputs",
    "reports/loop/README.md": "Loop Reports",
}

STATIC_ROOT_TOKENS = [
    "Multi-level alignment report",
    "reports/alignment/latest_multilevel_alignment_report.md",
    "reports/alignment/latest_multilevel_alignment_validation.md",
    "scripts/alignment/emit_multilevel_alignment_v0_3b2.py",
    "scripts/validation/validate_multilevel_alignment_v0_3b2.py",
    "scripts/validation/validate_surface_alignment_v0_3b2.py",
    "Pre-API Transmission Constraint Box",
    "Negative control harness",
    "scripts/controls/emit_negative_control_harness_v0_3b4.py",
    "scripts/validation/validate_negative_control_harness_v0_3b4.py",
    "Memory promotion kernel",
    "scripts/memory/emit_memory_promotion_v0_3b5.py",
    "scripts/validation/validate_memory_promotion_v0_3b5.py",
    "reports/loop/latest_loop_drift_pressure.md",
    "scripts/loop/emit_loop_drift_pressure_v0_4_2.py",
    "scripts/validation/validate_loop_drift_pressure_v0_4_2.py",
    "scripts/validation/validate_loop_repair_recommendations_v0_4_3.py",
    "scripts/loop/emit_loop_repair_recommendations_v0_4_3.py",
    "reports/loop/latest_loop_repair_recommendations.md",
]

STALE_FORBIDDEN_TOKENS = [
    "CMS--SA-v0.3b11",
    "Current checkpoint: **CMS-SA v0.3b1a - Surface Alignment Repair and File-Run Guard**",
    "Current checkpoint: **CMS-SA v0.3b1 - README and Mini README Reflective Feedback Alignment Lock**",
]

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""

def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def main() -> int:
    findings = []
    warnings = []
    readme = read(README)
    registry = load_json(REGISTRY)
    current_version = str(registry.get("current_version") or registry.get("latest_version") or "unknown")
    previous_version = str(registry.get("previous_version") or "unknown")
    current_checkpoint = str(registry.get("current_checkpoint") or "")
    current_badge = "CMS--SA-" + current_version + "-blue"
    current_rcc = "CMS-RCC-N-" + current_version
    dynamic_root_tokens = [
        current_badge,
        "Current checkpoint: **" + current_checkpoint + "**",
        "| Current checkpoint | CMS-SA " + current_version + " |",
        "| Previous seal | CMS-SA " + previous_version + " |",
        current_rcc + " / 180 days",
        "API is not active in " + current_version,
    ]
    for token in dynamic_root_tokens + STATIC_ROOT_TOKENS:
        if token not in readme:
            findings.append("root_missing:" + token)
    for token in STALE_FORBIDDEN_TOKENS:
        if token in readme:
            findings.append("root_stale_token_present:" + token)
    if registry.get("current_version") != current_version:
        findings.append("registry_current_version_mismatch:" + str(registry.get("current_version")))
    if registry.get("latest_version") != current_version:
        findings.append("registry_latest_version_mismatch:" + str(registry.get("latest_version")))
    if current_version not in str(registry.get("current_checkpoint", "")):
        findings.append("registry_current_checkpoint_mismatch")
    if registry.get("previous_version") != previous_version:
        findings.append("registry_previous_version_mismatch:" + str(registry.get("previous_version")))
    for relative, role in MINI_README_EXPECTED.items():
        text = read(ROOT / relative)
        if not text:
            findings.append("missing_mini_readme:" + relative)
            continue
        for token in (current_rcc, role, "Update rule:", "Non-claim lock:"):
            if token not in text:
                findings.append("mini_readme_missing:" + relative + ":" + token)
    report = {
        "schema": "CMS-SA-" + current_version + "-surface-alignment-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "warnings": len(warnings),
        "findings": findings,
        "warning_findings": warnings,
        "current_version": current_version,
        "previous_version": previous_version,
        "root_tokens_checked": len(dynamic_root_tokens) + len(STATIC_ROOT_TOKENS),
        "mini_readmes_checked": len(MINI_README_EXPECTED),
        "stale_tokens_checked": len(STALE_FORBIDDEN_TOKENS),
        "registry_derived": True,
        "preseal_postseal_boundary": "surface alignment does not require release tag existence; public sync validates that after seal",
        "non_claim_lock": "Surface alignment validates README and mini README currentness only. It does not prove code correctness.",
    }
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md = [
        "# CMS-SA " + current_version + " Surface Alignment Validation",
        "",
        "| Field | Value |",
        "|---|---|",
        "| passed | `" + str(report["passed"]).lower() + "` |",
        "| errors | `" + str(report["errors"]) + "` |",
        "| warnings | `" + str(report["warnings"]) + "` |",
        "| current version | `" + current_version + "` |",
        "| previous version | `" + previous_version + "` |",
        "| registry derived | `true` |",
        "",
        "Non-claim lock: surface alignment validates README and mini README currentness only. It does not prove code correctness.",
        "",
    ]
    if findings:
        md += ["## Findings", ""]
        md += ["- `" + finding + "`" for finding in findings]
        md.append("")
    REPORT_MD.write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
