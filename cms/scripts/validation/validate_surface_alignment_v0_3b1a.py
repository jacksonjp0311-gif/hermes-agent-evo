from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

README = ROOT / "README.md"
REGISTRY = ROOT / "outputs" / "version_registry" / "cms_version_registry.json"
REPORT_JSON = ROOT / "reports" / "surface_alignment" / "latest_surface_alignment_report.json"
REPORT_MD = ROOT / "reports" / "surface_alignment" / "latest_surface_alignment_report.md"

CURRENT_VERSION = "v0.3b1a"
CURRENT_CHECKPOINT = "CMS-SA v0.3b1a"
PREVIOUS_VERSION = "v0.3b1"

ROOT_REQUIRED_TOKENS = [
    "CMS--SA-v0.3b1a-blue",
    "Current checkpoint: **CMS-SA v0.3b1a - Surface Alignment Repair and File-Run Guard**",
    "Previous seal: **CMS-SA v0.3b1 - README and Mini README Reflective Feedback Alignment Lock**",
    "| Current checkpoint | CMS-SA v0.3b1a |",
    "| Previous seal | CMS-SA v0.3b1 |",
    "Feedback lifecycle report",
    "reports/feedback/latest_feedback_lifecycle_report.md",
    "reports/feedback/latest_feedback_lifecycle_validation.md",
    "reports/surface_alignment/latest_surface_alignment_report.md",
    "scripts/feedback/emit_feedback_lifecycle_v0_3b.py",
    "scripts/validation/validate_feedback_lifecycle_v0_3b.py",
    "scripts/validation/validate_surface_alignment_v0_3b1a.py",
    "CMS-RCC-N-v0.3b1a / 180 days",
    "Pre-API Transmission Constraint Box",
    "API is not active in v0.3b1a",
    "Stale-section lock rule",
    "CMS-L-018",
    "| `configs/feedback/` | Feedback lifecycle contracts and promotion/downgrade rules. |",
    "| `outputs/evidence/` | Latest evidence packages emitted by the runtime. |",
    "| `reports/release/` | Release readiness reports and checkpoint validation outputs. |",
    "| `reports/feedback/` | Feedback lifecycle reports and validation outputs. |",
    "| `reports/surface_alignment/` | Root README and mini README alignment validation reports. |",
]

STALE_FORBIDDEN_TOKENS = [
    "CMS--SA-v0.3b11",
    "missing_badge:CMS--SA-v0.3b11",
    "Previous seal: **CMS-SA v0.2b3 - README Structure, Public Sync Guard, and Tau Lesson Embedding**",
    "CMS-RCC-N-v0.3a1 / 180 days",
    "Current checkpoint: **CMS-SA v0.3b - Feedback Quality and Lifecycle Engine**",
    "API is not active in v0.3b1. API work begins",
]

MINI_README_EXPECTED = {
    "configs/feedback/README.md": ["CMS-RCC-N-v0.3b1a", "Feedback Lifecycle Contracts"],
    "src/cms/feedback/README.md": ["CMS-RCC-N-v0.3b1a", "Feedback Lifecycle Runtime"],
    "scripts/feedback/README.md": ["CMS-RCC-N-v0.3b1a", "Feedback Emitters"],
    "outputs/feedback/README.md": ["CMS-RCC-N-v0.3b1a", "Feedback Outputs"],
    "reports/feedback/README.md": ["CMS-RCC-N-v0.3b1a", "Feedback Reports"],
    "schemas/README.md": ["CMS-RCC-N-v0.3b1a", "CMS Schemas"],
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def main() -> int:
    findings: list[str] = []
    warnings: list[str] = []

    readme = read(README)
    for token in ROOT_REQUIRED_TOKENS:
        if token not in readme:
            findings.append(f"root_missing:{token}")

    for token in STALE_FORBIDDEN_TOKENS:
        if token in readme:
            findings.append(f"root_stale_token_present:{token}")

    if not REGISTRY.exists():
        findings.append("missing_version_registry")
        registry = {}
    else:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))

    if registry.get("current_version") != CURRENT_VERSION:
        findings.append(f"registry_current_version_mismatch:{registry.get('current_version')}")

    if registry.get("latest_version") != CURRENT_VERSION:
        findings.append(f"registry_latest_version_mismatch:{registry.get('latest_version')}")

    if CURRENT_CHECKPOINT not in str(registry.get("current_checkpoint", "")):
        findings.append("registry_current_checkpoint_mismatch")

    for relative, tokens in MINI_README_EXPECTED.items():
        path = ROOT / relative
        text = read(path)
        if not text:
            findings.append(f"missing_mini_readme:{relative}")
            continue
        for token in tokens:
            if token not in text:
                findings.append(f"mini_readme_missing:{relative}:{token}")

    report = {
        "schema": "CMS-SA-v0.3b1a-surface-alignment-validation",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "warnings": len(warnings),
        "findings": findings,
        "warning_findings": warnings,
        "current_version": CURRENT_VERSION,
        "previous_version": PREVIOUS_VERSION,
        "root_tokens_checked": len(ROOT_REQUIRED_TOKENS),
        "mini_readmes_checked": len(MINI_README_EXPECTED),
        "stale_tokens_checked": len(STALE_FORBIDDEN_TOKENS),
        "non_claim_lock": "Surface alignment validates README and mini README currentness only. It does not prove code correctness.",
    }

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    md = [
        "# CMS-SA v0.3b1a Surface Alignment Validation",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(report['passed']).lower()}` |",
        f"| errors | `{report['errors']}` |",
        f"| warnings | `{report['warnings']}` |",
        f"| current version | `{report['current_version']}` |",
        f"| previous version | `{report['previous_version']}` |",
        f"| root tokens checked | `{report['root_tokens_checked']}` |",
        f"| mini READMEs checked | `{report['mini_readmes_checked']}` |",
        f"| stale tokens checked | `{report['stale_tokens_checked']}` |",
        "",
        "Non-claim lock: surface alignment validates README and mini README currentness only. It does not prove code correctness.",
        "",
    ]

    if findings:
        md.extend(["## Findings", ""])
        for finding in findings:
            md.append(f"- `{finding}`")
        md.append("")

    REPORT_MD.write_text("\n".join(md), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())