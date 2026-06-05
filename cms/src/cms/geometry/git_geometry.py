from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]


SURFACE_RULES = [
    ("README.md", "outer", "documentation", "public"),
    ("scripts/validation/", "middle", "validation", "validator"),
    ("scripts/geometry/", "middle", "validation", "emitter"),
    ("scripts/rcc/", "middle", "agent", "rcc"),
    ("outputs/evidence/", "outer", "evidence", "reports"),
    ("reports/", "outer", "evidence", "reports"),
    ("outputs/version_registry/", "center", "memory", "lineage"),
    ("outputs/lineage/", "center", "memory", "lineage"),
    ("outputs/injections/", "center", "memory", "lineage"),
    ("docs/release_seals/", "outer", "release", "seal"),
    ("docs/versions/", "outer", "documentation", "versions"),
    ("docs/injections/", "outer", "documentation", "injections"),
    ("src/cms/", "inner", "runtime", "core"),
    ("configs/", "center", "source", "contract"),
    ("schemas/", "center", "source", "schemas"),
    ("tests/", "middle", "validation", "tests"),
]


REPORT_REFRESH_PREFIXES = (
    "outputs/geometry/",
    "reports/geometry/",
    "reports/readme/",
    "reports/render_hygiene/",
    "reports/public_sync/",
    "reports/release/",
)


def run_git(args: list[str]) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        raise RuntimeError((completed.stderr or completed.stdout).strip())
    return completed.stdout.strip()


def git_ok(args: list[str]) -> bool:
    completed = subprocess.run(["git", *args], cwd=ROOT, check=False, capture_output=True, text=True)
    return completed.returncode == 0


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def current_version(registry: dict[str, Any]) -> str:
    for key in ("current_version", "latest_version", "version"):
        value = registry.get(key)
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


def classify_path(path: str) -> dict[str, str]:
    normalized = path.replace("\\", "/")
    for pattern, shell, meridian, sector in SURFACE_RULES:
        if normalized == pattern.rstrip("/") or normalized.startswith(pattern):
            return {"path": path, "pattern": pattern, "shell": shell, "meridian": meridian, "sector": sector}
    return {"path": path, "pattern": "unclassified", "shell": "middle", "meridian": "documentation", "sector": "unclassified"}


def commit_tags() -> dict[str, str]:
    tags: dict[str, str] = {}
    try:
        raw = run_git(["show-ref", "--tags", "-d"])
    except RuntimeError:
        return tags

    for line in raw.splitlines():
        parts = line.split()
        if len(parts) != 2:
            continue
        commit, ref = parts
        if ref.endswith("^{}"):
            tag = ref.split("/")[-1].replace("^{}", "")
            tags[commit] = tag
    return tags


def changed_files_for_commit(commit: str) -> list[str]:
    raw = run_git(["diff-tree", "--no-commit-id", "--name-only", "-r", commit])
    return [line.strip() for line in raw.splitlines() if line.strip()]


def parents_for_commit(commit: str) -> list[str]:
    raw = run_git(["rev-list", "--parents", "-n", "1", commit])
    parts = raw.split()
    return parts[1:]


def detect_lessons(text: str, changed_files: list[str]) -> list[str]:
    joined = text + "\n" + "\n".join(changed_files)
    return sorted(set(re.findall(r"CMS-L-\d{3}", joined)))


def is_report_refresh_commit(message: str, changed_files: list[str]) -> bool:
    """True when a commit only refreshes volatile report artifacts.

    These commits are real Git points, but excluding them from semantic
    geometry nodes prevents committed latest geometry reports from rewriting
    themselves after every report-refresh commit.
    """

    msg = message.lower().strip()
    if not (
        msg.startswith("chore: refresh")
        or msg.startswith("chore: record")
        or "validation reports" in msg
        or "report refresh" in msg
    ):
        return False

    if not changed_files:
        return False

    normalized = [path.replace("\\", "/") for path in changed_files]
    return all(path.startswith(REPORT_REFRESH_PREFIXES) for path in normalized)


def release_truth_state(version: str) -> dict[str, Any]:
    head = run_git(["rev-parse", "HEAD"])
    origin = run_git(["rev-parse", "origin/main"])
    tag_exists = False
    tag_is_ancestor = False

    if version != "unknown":
        tag_exists = git_ok(["rev-parse", f"{version}^{{}}"])
        if tag_exists:
            tag_is_ancestor = git_ok(["merge-base", "--is-ancestor", f"{version}^{{}}", "HEAD"])

    readme_text = (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")
    return {
        "registry_current_version": version,
        "head_origin_match": head == origin,
        "readme_checkpoint_present": version != "unknown" and version in readme_text,
        "release_tag_exists": tag_exists,
        "release_tag_is_ancestor_of_head": tag_is_ancestor,
        "stable_geometry_boundary": True,
        "report_refresh_commits_excluded": True,
        "pure_validation_boundary": True,
        "non_claim_lock": "Release truth is repository-bound and does not prove runtime correctness.",
    }


def build_reflective_git_geometry(limit: int = 12) -> dict[str, Any]:
    registry = load_json(ROOT / "outputs" / "version_registry" / "cms_version_registry.json")
    version = current_version(registry)
    truth = release_truth_state(version)

    raw_limit = max(limit * 4, limit)
    log_raw = run_git(["log", f"-{raw_limit}", "--pretty=format:%H%x1f%s"])
    tag_map = commit_tags()

    nodes: list[dict[str, Any]] = []
    skipped_report_refresh_commits: list[str] = []

    for line in log_raw.splitlines():
        if not line.strip():
            continue

        commit, message = line.split("\x1f", 1)
        changed = changed_files_for_commit(commit)

        if is_report_refresh_commit(message, changed):
            skipped_report_refresh_commits.append(commit[:7])
            continue

        classes = [classify_path(path) for path in changed]
        shells = sorted({item["shell"] for item in classes})
        meridians = sorted({item["meridian"] for item in classes})
        sectors = sorted({item["sector"] for item in classes})

        validator_reports = [
            path for path in changed
            if path.startswith("reports/") or path.startswith("scripts/validation/") or path.startswith("scripts/rcc/")
        ]
        evidence_reports = [
            path for path in changed
            if path.startswith("outputs/evidence/")
            or path.startswith("reports/evidence/")
            or path.startswith("reports/public_sync/")
            or path.startswith("reports/readme/")
        ]

        nodes.append({
            "commit_hash": commit,
            "short_hash": commit[:7],
            "parents": parents_for_commit(commit),
            "tag": tag_map.get(commit),
            "message": message,
            "changed_files": changed,
            "surface_classes": classes,
            "shells": shells,
            "meridians": meridians,
            "sectors": sectors,
            "lesson_ids_detected": detect_lessons(message, changed),
            "validator_reports_touched": validator_reports,
            "evidence_reports_touched": evidence_reports,
            "release_truth": truth,
        })

        if len(nodes) >= limit:
            break

    return {
        "schema": "CMS-SA-v0.3a2-reflective-git-geometry",
        "version": "v0.3a2",
        "current_registry_version": version,
        "node_count": len(nodes),
        "core_law": "A commit is not only a change; it is a routed event in repository geometry.",
        "secondary_law": "A repository learns when repeated routed events become constraints, validators, evidence surfaces, and future routing rules.",
        "stable_geometry_boundary": True,
        "report_refresh_commits_excluded": True,
        "pure_validation_boundary": True,
        "emission_validation_split": True,
        "skipped_report_refresh_commits": skipped_report_refresh_commits,
        "release_truth": truth,
        "nodes": nodes,
        "non_claim_lock": "Reflective Git geometry improves repository orientation, routing, and evidence traceability. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.",
    }


def geometry_to_markdown(geometry: dict[str, Any]) -> str:
    rows = [
        "# CMS-SA v0.3a2 Reflective Git Geometry Report",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| schema | `{geometry['schema']}` |",
        f"| node count | `{geometry['node_count']}` |",
        f"| current registry version | `{geometry['current_registry_version']}` |",
        f"| stable geometry boundary | `{str(geometry['stable_geometry_boundary']).lower()}` |",
        f"| report refresh commits excluded | `{str(geometry['report_refresh_commits_excluded']).lower()}` |",
        f"| pure validation boundary | `{str(geometry['pure_validation_boundary']).lower()}` |",
        f"| emission validation split | `{str(geometry['emission_validation_split']).lower()}` |",
        f"| head/origin match | `{str(geometry['release_truth'].get('head_origin_match')).lower()}` |",
        f"| release tag exists | `{str(geometry['release_truth'].get('release_tag_exists')).lower()}` |",
        f"| release tag ancestor | `{str(geometry['release_truth'].get('release_tag_is_ancestor_of_head')).lower()}` |",
        "",
        "## Commit Geometry Nodes",
        "",
        "| Commit | Tag | Shells | Meridians | Sectors | Message |",
        "|---|---|---|---|---|---|",
    ]

    for node in geometry["nodes"]:
        tag = node.get("tag") or ""
        shells = ", ".join(node.get("shells", []))
        meridians = ", ".join(node.get("meridians", []))
        sectors = ", ".join(node.get("sectors", []))
        message = str(node.get("message", "")).replace("|", "/")
        rows.append(f"| `{node['short_hash']}` | `{tag}` | `{shells}` | `{meridians}` | `{sectors}` | {message} |")

    rows.extend([
        "",
        "## Pure Validation Boundary",
        "",
        "Reflective geometry emission writes geometry artifacts. Reflective geometry validation reads existing artifacts and must not rewrite them.",
        "",
        "## Stable Boundary Rule",
        "",
        "Report-only refresh commits are excluded from semantic geometry nodes to prevent latest geometry reports from self-invalidating after report-refresh commits.",
        "",
        "## Core Law",
        "",
        "A commit is not only a change; it is a routed event in repository geometry.",
        "",
        "## Non-claim Lock",
        "",
        "Reflective Git geometry improves repository orientation, routing, and evidence traceability. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.",
        "",
    ])

    return "\n".join(rows)


def write_geometry(limit: int = 12) -> dict[str, Any]:
    """Emit geometry artifacts.

    This function is intentionally write-capable. Validators should not call it.
    """

    geometry = build_reflective_git_geometry(limit=limit)

    out_json = ROOT / "outputs" / "geometry" / "latest_reflective_git_geometry.json"
    report_json = ROOT / "reports" / "geometry" / "latest_reflective_git_geometry.json"
    report_md = ROOT / "reports" / "geometry" / "latest_reflective_git_geometry.md"

    out_json.parent.mkdir(parents=True, exist_ok=True)
    report_json.parent.mkdir(parents=True, exist_ok=True)

    text = json.dumps(geometry, indent=2) + "\n"
    out_json.write_text(text, encoding="utf-8")
    report_json.write_text(text, encoding="utf-8")
    report_md.write_text(geometry_to_markdown(geometry), encoding="utf-8")

    return geometry


if __name__ == "__main__":
    print(json.dumps(write_geometry(), indent=2))