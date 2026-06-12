from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping
import json

from rhp.loop_geometry import validate_readme_geometry, report_to_dict

ZERO_CONTEXT_SOURCE_ORDER: tuple[str, ...] = (
    "README.md",
    "AGENTS.md",
    "docs/context-layer/latest-rhp.json",
    "<latest_evidence_from_latest_rhp>",
    "docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md",
    "docs/context-layer/hermes-operator-context.json",
    "rhp/loop_geometry.py",
)

REQUIRED_AUTHORITY_FALSE_KEYS: tuple[str, ...] = (
    "provider_call_executed",
    "model_call_executed",
    "tool_use_executed",
    "cms_runtime_execution",
    "cms_write",
    "memory_write",
    "memory_promotion",
    "api_write",
    "dependency_mutation_committed",
    "external_ingestion",
    "autonomous_authority",
    "self_authorization",
)


@dataclass(frozen=True)
class ZeroContextBootstrapReport:
    ok: bool
    readme_loaded: bool
    agents_loaded: bool
    latest_rhp_loaded: bool
    latest_evidence_loaded: bool
    zero_context_rebuild_loaded: bool
    operator_context_loaded: bool
    loop_geometry_loaded: bool
    geometry_ok: bool
    authority_ok: bool
    latest_operation: str
    state: str
    active_wound: str
    subject_commit: str
    next_operation: str
    blocked_actions: tuple[str, ...]
    missing_sources: tuple[str, ...]


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def authority_false_map(data: Mapping[str, Any]) -> dict[str, bool]:
    """Return per-authority false-lock status.

    Evidence files and operator context normally carry full authority_locks.
    latest-rhp.json is a pointer and may carry only authority_ok=true; that is
    acceptable for the pointer only because the latest evidence and operator
    context are still checked separately.
    """
    locks = data.get("authority_locks")
    if isinstance(locks, dict):
        return {key: bool(locks.get(key) is False) for key in REQUIRED_AUTHORITY_FALSE_KEYS}

    if any(key in data for key in REQUIRED_AUTHORITY_FALSE_KEYS):
        return {key: bool(data.get(key) is False) for key in REQUIRED_AUTHORITY_FALSE_KEYS}

    if data.get("schema") == "RHP-LATEST-POINTER-v2.1" and data.get("authority_ok") is True:
        return {key: True for key in REQUIRED_AUTHORITY_FALSE_KEYS}

    return {key: False for key in REQUIRED_AUTHORITY_FALSE_KEYS}


def authority_ok(*evidence_maps: Mapping[str, Any]) -> bool:
    for data in evidence_maps:
        status = authority_false_map(data)
        if not all(status.values()):
            return False
    return True


def validate_zero_context_bootstrap(repo_root: str | Path) -> ZeroContextBootstrapReport:
    root = Path(repo_root)
    readme_path = root / "README.md"
    agents_path = root / "AGENTS.md"
    latest_path = root / "docs/context-layer/latest-rhp.json"
    zero_context_path = root / "docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md"
    operator_context_path = root / "docs/context-layer/hermes-operator-context.json"
    loop_geometry_path = root / "rhp/loop_geometry.py"

    missing: list[str] = []
    for label, path in [
        ("README.md", readme_path),
        ("AGENTS.md", agents_path),
        ("docs/context-layer/latest-rhp.json", latest_path),
        ("docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md", zero_context_path),
        ("docs/context-layer/hermes-operator-context.json", operator_context_path),
        ("rhp/loop_geometry.py", loop_geometry_path),
    ]:
        if not path.exists():
            missing.append(label)

    latest: dict[str, Any] = {}
    evidence: dict[str, Any] = {}
    operator_context: dict[str, Any] = {}
    latest_evidence_loaded = False

    if latest_path.exists():
        latest = _read_json(latest_path)
        latest_evidence_rel = latest.get("latest_evidence", "")
        latest_evidence_path = root / latest_evidence_rel
        if latest_evidence_rel and latest_evidence_path.exists():
            evidence = _read_json(latest_evidence_path)
            latest_evidence_loaded = True
        else:
            missing.append("<latest_evidence_from_latest_rhp>")

    if operator_context_path.exists():
        operator_context = _read_json(operator_context_path)

    geometry_ok = False
    if readme_path.exists() and loop_geometry_path.exists():
        geometry_ok = validate_readme_geometry(readme_path.read_text(encoding="utf-8")).ok

    auth_ok = authority_ok(latest, evidence, operator_context) if latest and evidence and operator_context else False

    blocked = (
        "repair",
        "wound_closure",
        "autonomous_authority",
        "current_operation_green_claim",
        "dependency_mutation",
        "external_ingestion",
    )

    report = ZeroContextBootstrapReport(
        ok=(
            not missing
            and readme_path.exists()
            and agents_path.exists()
            and bool(latest)
            and latest_evidence_loaded
            and zero_context_path.exists()
            and bool(operator_context)
            and loop_geometry_path.exists()
            and geometry_ok
            and auth_ok
        ),
        readme_loaded=readme_path.exists(),
        agents_loaded=agents_path.exists(),
        latest_rhp_loaded=bool(latest),
        latest_evidence_loaded=latest_evidence_loaded,
        zero_context_rebuild_loaded=zero_context_path.exists(),
        operator_context_loaded=bool(operator_context),
        loop_geometry_loaded=loop_geometry_path.exists(),
        geometry_ok=geometry_ok,
        authority_ok=auth_ok,
        latest_operation=str(latest.get("latest_operation", "")),
        state=str(latest.get("state", "")),
        active_wound=str(latest.get("active_wound_class", "")),
        subject_commit=str(latest.get("subject_commit", "")),
        next_operation=str(latest.get("next_operation", "")),
        blocked_actions=blocked,
        missing_sources=tuple(missing),
    )
    return report


def report_to_dict(report: ZeroContextBootstrapReport) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "readme_loaded": report.readme_loaded,
        "agents_loaded": report.agents_loaded,
        "latest_rhp_loaded": report.latest_rhp_loaded,
        "latest_evidence_loaded": report.latest_evidence_loaded,
        "zero_context_rebuild_loaded": report.zero_context_rebuild_loaded,
        "operator_context_loaded": report.operator_context_loaded,
        "loop_geometry_loaded": report.loop_geometry_loaded,
        "geometry_ok": report.geometry_ok,
        "authority_ok": report.authority_ok,
        "latest_operation": report.latest_operation,
        "state": report.state,
        "active_wound": report.active_wound,
        "subject_commit": report.subject_commit,
        "next_operation": report.next_operation,
        "blocked_actions": list(report.blocked_actions),
        "missing_sources": list(report.missing_sources),
    }


def render_zero_context_panel(report: ZeroContextBootstrapReport) -> str:
    status = "rehydrated" if report.ok else "blocked"
    lines = [
        f"RHPZERO [GOLD] status={status}",
        "`- zero-context bootstrap report",
        f"   +- readme-loaded: {str(report.readme_loaded).lower()}",
        f"   +- agents-loaded: {str(report.agents_loaded).lower()}",
        f"   +- latest-rhp-loaded: {str(report.latest_rhp_loaded).lower()}",
        f"   +- latest-evidence-loaded: {str(report.latest_evidence_loaded).lower()}",
        f"   +- zero-context-rebuild-loaded: {str(report.zero_context_rebuild_loaded).lower()}",
        f"   +- operator-context-loaded: {str(report.operator_context_loaded).lower()}",
        f"   +- geometry-ok: {str(report.geometry_ok).lower()}",
        f"   +- authority-ok: {str(report.authority_ok).lower()}",
        f"   +- active-wound: {report.active_wound or 'unknown'}",
        f"   +- next: {report.next_operation or 'unknown'}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
