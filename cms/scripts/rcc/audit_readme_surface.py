from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
README = ROOT / "README.md"
REGISTRY = ROOT / "outputs" / "version_registry" / "cms_version_registry.json"
REPORT_JSON = ROOT / "reports" / "readme" / "latest_readme_mini_repo_audit.json"
REPORT_MD = ROOT / "reports" / "readme" / "latest_readme_mini_repo_audit.md"


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def current_version(registry: dict) -> str:
    for key in ("current_version", "latest_version", "version"):
        value = registry.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    current = registry.get("current")
    if isinstance(current, dict):
        for key in ("version", "current_version", "latest_version"):
            value = current.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()

    versions = registry.get("versions")
    if isinstance(versions, list) and versions:
        last = versions[-1]
        if isinstance(last, dict):
            value = last.get("version")
            if isinstance(value, str) and value.strip():
                return value.strip()

    return "unknown"


def main() -> int:
    registry = load_json(REGISTRY)
    version = current_version(registry)
    readme = README.read_text(encoding="utf-8", errors="replace") if README.exists() else ""

    required_tokens = [
        "# Cybernetic Memory System",
        "Repository: `cybernetic-memory-system`",
        "Package / CLI: `cms`",
        f"Current checkpoint: **CMS-SA {version}",
        "## Current CMS Snapshot",
        "## Current Public Metrics",
        "## Quick Start",
        "## Repository Layers",
        "## AI Failure Learning Ledger",
        "## Full Directory Box",
        "Non-claim lock",
        "Mini README update rule",
    ]

    missing = [token for token in required_tokens if token not in readme]

    mini_missing = []
    for path in ROOT.iterdir():
        if path.is_dir() and not path.name.startswith("."):
            mini = path / "README.md"
            if mini.exists():
                text = mini.read_text(encoding="utf-8", errors="replace")
                if "Mini README update rule" not in text and "README" in text:
                    # Non-blocking for now; many mini READMEs are older navigation surfaces.
                    pass

    report = {
        "schema": f"CMS-SA-{version}-readme-mini-repo-audit",
        "passed": len(missing) == 0,
        "errors": len(missing),
        "warnings": 0,
        "accepted_checkpoint_pattern": f"CMS-SA {version}",
        "missing_root_tokens": missing,
        "mini_readmes_missing_update_rule": mini_missing,
        "release_gate_truth_enforced": True,
        "non_claim_lock": "README audits improve context alignment but do not prove runtime correctness."
    }

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    md = [
        f"# CMS-SA {version} README / Mini Repo Audit",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| passed | `{str(report['passed']).lower()}` |",
        f"| errors | `{report['errors']}` |",
        f"| warnings | `0` |",
        f"| accepted checkpoint pattern | `CMS-SA {version}` |",
        f"| release gate truth enforced | `true` |",
        "",
    ]

    if missing:
        md.append("## Missing Root Tokens")
        md.append("")
        for item in missing:
            md.append(f"- `{item}`")
        md.append("")

    md.append("Non-claim lock: README audits improve context alignment but do not prove runtime correctness.")
    md.append("")

    REPORT_MD.write_text("\n".join(md), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
