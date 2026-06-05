from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REPORT_JSON = ROOT / "reports" / "public_sync" / "latest_public_sync_report.json"
REPORT_MD = ROOT / "reports" / "public_sync" / "latest_public_sync_report.md"
REGISTRY = ROOT / "outputs" / "version_registry" / "cms_version_registry.json"
README = ROOT / "README.md"


def run_git(args: list[str]) -> tuple[bool, str]:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0, (completed.stdout or completed.stderr).strip()


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
    findings: list[str] = []
    warnings: list[str] = []

    registry = load_json(REGISTRY)
    version = current_version(registry)

    ok_head, head = run_git(["rev-parse", "HEAD"])
    ok_origin, origin = run_git(["rev-parse", "origin/main"])
    head_origin_match = bool(ok_head and ok_origin and head == origin)
    if not head_origin_match:
        findings.append("head_not_equal_origin_main")

    readme = README.read_text(encoding="utf-8", errors="replace") if README.exists() else ""
    readme_checkpoint_present = version != "unknown" and version in readme
    if not readme_checkpoint_present:
        findings.append("readme_checkpoint_missing_current_version")

    tag_exists = False
    tag_is_ancestor = False
    tag_status = "not_checked"

    if version == "unknown":
        findings.append("registry_current_version_unknown")
        tag_status = "unknown_current_version"
    else:
        ok_tag, _ = run_git(["rev-parse", f"{version}^{{}}"])
        tag_exists = ok_tag
        if not tag_exists:
            findings.append("release_tag_missing")
            tag_status = "missing"
        else:
            ok_ancestor, _ = run_git(["merge-base", "--is-ancestor", f"{version}^{{}}", "HEAD"])
            tag_is_ancestor = ok_ancestor
            if tag_is_ancestor:
                tag_status = "present_and_ancestor_of_head"
            else:
                findings.append("release_tag_not_ancestor_of_head")
                tag_status = "present_but_not_ancestor_of_head"

    report = {
        "schema": "CMS-SA-v0.2b3c-public-sync-stable",
        "passed": len(findings) == 0,
        "errors": len(findings),
        "warnings": len(warnings),
        "findings": findings,
        "warning_findings": warnings,
        "registry_current_version": version,
        "head_origin_match": head_origin_match,
        "readme_checkpoint_present": readme_checkpoint_present,
        "release_tag": version,
        "release_tag_status": tag_status,
        "release_tag_exists": tag_exists,
        "release_tag_is_ancestor_of_head": tag_is_ancestor,
        "stable_evidence_boundary": True,
        "volatile_commit_hashes_omitted": True,
        "policy": "Committed public-sync reports omit volatile commit hashes. Runtime validation still checks HEAD/origin agreement and release-tag ancestry.",
        "non_claim_lock": "Public sync validation checks repository-state agreement but does not prove runtime correctness, truth, AGI, consciousness, production readiness, security, or external validation."
    }

    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    md = [
        "# CMS-SA v0.2b3c Public Sync Report",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| schema | `{report['schema']}` |",
        f"| passed | `{str(report['passed']).lower()}` |",
        f"| errors | `{report['errors']}` |",
        f"| warnings | `{report['warnings']}` |",
        f"| registry current version | `{version}` |",
        f"| HEAD equals origin/main | `{str(head_origin_match).lower()}` |",
        f"| README checkpoint present | `{str(readme_checkpoint_present).lower()}` |",
        f"| release tag | `{version}` |",
        f"| release tag status | `{tag_status}` |",
        f"| stable evidence boundary | `true` |",
        f"| volatile commit hashes omitted | `true` |",
        "",
        "Non-claim lock: public sync validation checks repository-state agreement only. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.",
        "",
    ]
    REPORT_MD.write_text("\n".join(md), encoding="utf-8")

    print(json.dumps(report, indent=2))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())