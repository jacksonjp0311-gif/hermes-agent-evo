from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
DOC = ROOT / "docs/context/THREAD_REHYDRATION_PROTOCOL.md"
CONTRACT = ROOT / "configs/rehydration/thread_rehydration_contract.json"
SCHEMA = ROOT / "schemas/thread_rehydration_scan.schema.json"
REGISTRY = ROOT / "outputs/version_registry/cms_version_registry.json"
OUT_JSON = ROOT / "reports/rehydration/latest_thread_rehydration_validation.json"
OUT_MD = ROOT / "reports/rehydration/latest_thread_rehydration_validation.md"

REQUIRED_README = [
    "Thread Rehydration Protocol Box",
    "theory tells why",
    "architecture tells how",
    "runtime tells now",
    "No fresh-thread versioning without Origin Scan, Architecture Scan, and Runtime State Scan.",
]
REQUIRED_DOC = [
    "Origin Theory Scan",
    "Software Architecture Scan",
    "Runtime State Scan",
    "Version-Readiness Lock",
    "Thread rehydration improves agent orientation",
]


def load(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def main() -> int:
    findings: list[str] = []
    readme = load(README)
    doc = load(DOC)

    for token in REQUIRED_README:
        if token not in readme:
            findings.append(f"readme_missing:{token}")

    if not DOC.exists():
        findings.append("missing_docs_context_THREAD_REHYDRATION_PROTOCOL_md")
    else:
        for token in REQUIRED_DOC:
            if token not in doc:
                findings.append(f"protocol_doc_missing:{token}")

    if not CONTRACT.exists():
        findings.append("missing_configs_rehydration_thread_rehydration_contract_json")
        contract = {}
    else:
        contract = json.loads(CONTRACT.read_text(encoding="utf-8"))

    if not SCHEMA.exists():
        findings.append("missing_schemas_thread_rehydration_scan_schema_json")

    for key in ["origin_scan_targets", "architecture_scan_targets", "runtime_scan_targets", "version_readiness_checks"]:
        value = contract.get(key)
        if not isinstance(value, list) or not value:
            findings.append(f"contract_missing_or_empty:{key}")

    if "does not prove" not in str(contract.get("non_claim_lock", "")):
        findings.append("contract_missing_non_claim_lock")

    if REGISTRY.exists():
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        current = str(registry.get("current_version", ""))
        checkpoint = str(registry.get("current_checkpoint", ""))
        if not current.startswith("v0.4."):
            findings.append(f"registry_current_version_not_v0.4_series:{current}")
        if "CMS-SA v0.4." not in checkpoint:
            findings.append("registry_checkpoint_not_v0.4_series")
        if "CMS-SA v0.4." not in str(registry.get("next_anchor", "")):
            findings.append("registry_next_anchor_not_v0.4_series")
    else:
        findings.append("missing_version_registry")

    passed = len(findings) == 0
    result = {
        "schema": "CMS-SA-v0.4.x-thread-rehydration-validation",
        "passed": passed,
        "version": "v0.4.x",
        "errors": len(findings),
        "findings": findings,
        "non_claim_lock": "Thread rehydration validation is repository-bound and does not prove code correctness.",
    }

    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# CMS-SA v0.4.x Thread Rehydration Validation",
        "",
        f"- passed: `{passed}`",
        f"- errors: `{len(findings)}`",
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
