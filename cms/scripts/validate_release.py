from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

required = [
    "README.md",
    "README_90_SECONDS.md",
    "AGENTS.md",
    "pyproject.toml",
    "docs/architecture/cms_sa_v0_1_software_architecture.tex",
    "rcc/nexus/route_map.json",
    "docs/context/repository_context_index.json",
    "src/cms/core/runtime.py",
    "src/cms/cli.py",
]

missing = [p for p in required if not (ROOT / p).exists()]

report = {
    "schema": "CMS-SA-v0.1-release-validation",
    "passed": len(missing) == 0,
    "missing": missing,
    "non_claim_lock": "validation is repository-bound and does not prove code correctness"
}

out_json = ROOT / "outputs" / "validation" / "latest_release_validation.json"
out_md = ROOT / "outputs" / "release" / "latest_release_readiness.md"
out_json.parent.mkdir(parents=True, exist_ok=True)
out_md.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
out_md.write_text(
    "# CMS-SA Release Readiness\n\n"
    f"- Passed: `{report['passed']}`\n"
    f"- Missing: `{missing}`\n"
    "- Non-claim lock: validation is repository-bound.\n",
    encoding="utf-8",
)

print(json.dumps(report, indent=2))
sys.exit(0 if report["passed"] else 1)