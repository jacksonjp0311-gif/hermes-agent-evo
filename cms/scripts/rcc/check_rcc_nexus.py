from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[2]

major_dirs = [
    "docs", "docs/context", "docs/architecture", "docs/protocols", "docs/versions",
    "docs/injections", "docs/release_seals", "docs/roadmap", "rcc", "rcc/nexus",
    "src", "src/cms", "src/cms/core", "src/cms/observation", "src/cms/metrics",
    "src/cms/comparator", "src/cms/feedback", "src/cms/planning", "src/cms/validation",
    "src/cms/memory", "src/cms/correction", "src/cms/evidence", "src/cms/schemas",
    "configs", "examples", "scripts", "tests", "outputs", "reports"
]

missing = [d for d in major_dirs if not (ROOT / d / "README.md").exists()]
required = [
    "README.md",
    "README_90_SECONDS.md",
    "AGENTS.md",
    "docs/context/repository_context_index.json",
    "docs/context/rcc_nexus_index.json",
    "rcc/nexus/route_map.json",
    "rcc/nexus/task_routing_matrix.md",
]

missing_required = [p for p in required if not (ROOT / p).exists()]
passed = not missing and not missing_required

report = {
    "schema": "CMS-SA-v0.1.2-rcc-nexus-check",
    "passed": passed,
    "errors": len(missing) + len(missing_required),
    "warnings": 0,
    "mini_readme_coverage": 1.0 if not missing else round((len(major_dirs) - len(missing)) / len(major_dirs), 3),
    "major_dirs_checked": len(major_dirs),
    "missing_mini_readmes": missing,
    "missing_required": missing_required,
    "non_claim_lock": "RCC-N navigation is not validation."
}

out_json = ROOT / "reports" / "rcc_nexus" / "latest_rcc_nexus_check.json"
out_md = ROOT / "reports" / "rcc_nexus" / "latest_rcc_nexus_check.md"
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
out_md.write_text(
    "# CMS RCC-N Check\n\n"
    f"- passed: `{passed}`\n"
    f"- errors: `{report['errors']}`\n"
    f"- warnings: `0`\n"
    f"- mini_readme_coverage: `{report['mini_readme_coverage']}`\n"
    f"- major_dirs_checked: `{len(major_dirs)}`\n\n"
    "Non-claim lock: RCC-N navigation is not validation.\n",
    encoding="utf-8",
)

print(json.dumps(report, indent=2))
raise SystemExit(0 if passed else 1)