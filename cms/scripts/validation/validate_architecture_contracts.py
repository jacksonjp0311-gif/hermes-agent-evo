from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

required = [
    "docs/architecture/cms_sa_v0_1_software_architecture.tex",
    "docs/context/repository_context_index.json",
    "docs/context/rcc_nexus_index.json",
    "docs/versions/VERSION_REGISTRY.md",
    "docs/roadmap/CMS_ROADMAP.md",
    "rcc/nexus/route_map.json",
    "AGENTS.md",
]

missing = [p for p in required if not (ROOT / p).exists()]
passed = len(missing) == 0

report = {
    "schema": "CMS-SA-v0.1.2-architecture-contract-validation",
    "passed": passed,
    "missing": missing,
    "non_claim_lock": "Architecture validation is not code correctness."
}

out_json = ROOT / "reports" / "architecture" / "latest_architecture_contract_validation.json"
out_md = ROOT / "reports" / "architecture" / "latest_architecture_contract_validation.md"
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
out_md.write_text(
    "# CMS Architecture Contract Validation\n\n"
    f"- passed: `{passed}`\n"
    f"- missing: `{missing}`\n\n"
    "Non-claim lock: architecture validation is not code correctness.\n",
    encoding="utf-8",
)

print(json.dumps(report, indent=2))
raise SystemExit(0 if passed else 1)