from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

VERSION = "v0.3b3"
ALLOWED_DECISIONS = {"promote", "block", "downgrade", "observe_only"}

REQUIRED_SIGNALS = [
    ("readme_audit", "reports/readme/latest_readme_mini_repo_audit.json"),
    ("readme_render_hygiene", "reports/render_hygiene/latest_readme_render_hygiene.json"),
    ("markdown_structure", "reports/markdown_structure/latest_markdown_structure.json"),
    ("reflective_git_geometry", "reports/geometry/latest_reflective_git_geometry_validation.json"),
    ("feedback_lifecycle", "reports/feedback/latest_feedback_lifecycle_validation.json"),
    ("surface_alignment", "reports/surface_alignment/latest_surface_alignment_report.json"),
    ("multilevel_alignment", "reports/alignment/latest_multilevel_alignment_validation.json"),
]

OPTIONAL_SIGNALS = [
    ("public_sync", "reports/public_sync/latest_public_sync_report.json"),
]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_hash(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _signal(root: Path, name: str, rel: str, required: bool) -> dict[str, Any]:
    path = root / rel
    if not path.exists():
        return {
            "name": name,
            "path": rel,
            "required": required,
            "present": False,
            "passed": False,
            "errors": ["missing_signal_file"],
        }

    try:
        data = load_json(path)
    except Exception as exc:
        return {
            "name": name,
            "path": rel,
            "required": required,
            "present": True,
            "passed": False,
            "errors": [f"unreadable_json:{type(exc).__name__}"],
        }

    passed = data.get("passed")
    return {
        "name": name,
        "path": rel,
        "required": required,
        "present": True,
        "passed": bool(passed is True),
        "schema": data.get("schema"),
        "errors": data.get("findings", []) if passed is not True else [],
    }


def _git_dirty(root: Path) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            ["git", "status", "--short"],
            cwd=str(root),
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return {"available": False, "dirty": True, "unexpected_dirty": ["git_status_failed"]}

    lines = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    unexpected = [
        line for line in lines
        if "_repo_dump/" not in line
    ]
    return {
        "available": True,
        "dirty": bool(unexpected),
        "unexpected_dirty": unexpected,
        "ignored_untracked": [line for line in lines if "_repo_dump/" in line],
    }


def build_decision(root: Path, include_git_state: bool = False) -> dict[str, Any]:
    root = root.resolve()

    signals: list[dict[str, Any]] = []
    for name, rel in REQUIRED_SIGNALS:
        signals.append(_signal(root, name, rel, True))
    for name, rel in OPTIONAL_SIGNALS:
        signals.append(_signal(root, name, rel, False))

    required_failures = [
        item["name"] for item in signals
        if item.get("required") and item.get("passed") is not True
    ]

    git_state = _git_dirty(root) if include_git_state else {
        "available": False,
        "dirty": None,
        "unexpected_dirty": [],
        "ignored_untracked": [],
        "note": "Git dirty state is intentionally handled by final release gates to avoid volatile latest-artifact loops.",
    }

    if required_failures:
        decision = "block"
        reason = "required_validation_surface_failed"
        next_allowed_action = "repair_failed_surfaces_before_promotion"
    else:
        decision = "promote"
        reason = "all_required_repository_bound_validation_surfaces_passed"
        next_allowed_action = "CMS-SA v0.3b4 - Negative Control and Downgrade Harness"

    body: dict[str, Any] = {
        "schema": "CMS-SA-v0.3b3-runtime-decision",
        "version": VERSION,
        "decision": decision,
        "reason": reason,
        "next_allowed_action": next_allowed_action,
        "required_failures": required_failures,
        "signals": signals,
        "release_validator_direct_final_gate": True,
        "git_state": git_state,
        "non_claim_lock": "Runtime decision checks repository-bound validation surfaces only. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.",
    }
    body["decision_hash"] = stable_hash({k: v for k, v in body.items() if k != "decision_hash"})
    return body