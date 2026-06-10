# RHP-013.5 operator-visible startup status wired to RuntimeBootState.
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

LOCK_LABELS = [
    ("repo_root", "repo root found"),
    ("rhp_evidence", "RHP evidence green"),
    ("hrcn_boundary", "HRCN boundary green"),
    ("alignment_guard", "alignment guard green"),
    ("startup_packet", "startup packet created"),
    ("authority_false", "authority=false"),
    ("external_ingestion_false", "external_ingestion=false"),
    ("provider_model_tool_false", "provider/model/tool execution=false"),
    ("cms_memory_api_false", "CMS/memory/API write=false"),
]

AUTHORITY_KEYS = [
    "provider_call_executed", "model_call_executed", "tool_use_executed",
    "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
    "api_write", "dependency_mutation_committed", "external_ingestion",
    "self_authorization", "autonomous_authority",
]

@dataclass(frozen=True)
class OperatorStartupStatus:
    ok: bool
    phase: str
    evidence: str
    locks: dict[str, bool]
    lines: list[str]
    non_claim_lock: str
    status: str = "ok"
    degraded: bool = False
    degraded_reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def _ascii_bool(value: bool) -> str:
    return "OK" if value else "DEGRADED"

def _data(packet: Any) -> dict[str, Any]:
    return packet.as_dict() if hasattr(packet, "as_dict") else dict(packet)

def _authority(data: dict[str, Any]) -> dict[str, bool]:
    nested = data.get("authority")
    if isinstance(nested, dict):
        return {key: bool(nested.get(key, False)) for key in AUTHORITY_KEYS}
    return {key: bool(data.get(key, False)) for key in AUTHORITY_KEYS}

def build_operator_startup_status(packet: Any, *, evidence: str = "RHP-013.5") -> OperatorStartupStatus:
    data = _data(packet)
    checks = data.get("checks") if isinstance(data.get("checks"), dict) else {}
    runtime_locks = data.get("locks") if isinstance(data.get("locks"), dict) else {}
    authority = _authority(data)
    authority_false = all(value is False for value in authority.values())
    boot_green = bool(data.get("boot_preflight_ok") or data.get("ok"))

    locks = {
        "repo_root": bool(data.get("repo_root") or runtime_locks.get("repo_root_found")),
        "rhp_evidence": bool(checks.get("rhp_evidence_green", data.get("rhp_evidence_green", runtime_locks.get("boot_preflight_ok", boot_green)))),
        "hrcn_boundary": bool(checks.get("hrcn_boundary_green", data.get("hrcn_boundary_green", runtime_locks.get("boot_preflight_ok", boot_green)))),
        "alignment_guard": bool(checks.get("alignment_guard_green", data.get("alignment_guard_green", runtime_locks.get("boot_preflight_ok", boot_green)))),
        "startup_packet": bool(data.get("startup_context_packet_created") or data.get("startup_packet_ok") or runtime_locks.get("startup_context_packet_created")),
        "authority_false": authority_false,
        "external_ingestion_false": authority.get("external_ingestion") is False,
        "provider_model_tool_false": (
            authority.get("provider_call_executed") is False
            and authority.get("model_call_executed") is False
            and authority.get("tool_use_executed") is False
        ),
        "cms_memory_api_false": (
            authority.get("cms_runtime_execution") is False
            and authority.get("cms_write") is False
            and authority.get("memory_write") is False
            and authority.get("memory_promotion") is False
            and authority.get("api_write") is False
        ),
    }

    ok = all(locks.values()) and boot_green
    degraded = bool(data.get("degraded")) or not ok
    status = "ok" if ok else "degraded"
    phase = str(data.get("phase") or "pre-interaction")
    degraded_reason = str(data.get("degraded_reason") or "")

    lines = ["RHP rehydration sequence:"]
    for key, label in LOCK_LABELS:
        lines.append(f"[{_ascii_bool(locks[key])}] {label}")
    lines.append(f"RHP rehydration complete: {status} | phase={phase} | evidence={evidence}")
    if degraded:
        lines.append(f"RHP degraded reason: {degraded_reason or 'one or more boot locks are not green'}")
    lines.append("RHP authority boundary: provider/model/tool=false | CMS/memory/API=false | external_ingestion=false | autonomy=false")

    return OperatorStartupStatus(
        ok=ok,
        phase=phase,
        evidence=evidence,
        locks=locks,
        lines=lines,
        status=status,
        degraded=degraded,
        degraded_reason=degraded_reason,
        non_claim_lock=(
            "RHP-013.5 displays RuntimeBootState-derived startup locks with degraded status when evidence or alignment is not green. "
            "It does not authorize tools, provider/model calls, CMS writes, memory writes, API writes, external ingestion, autonomy, or self-authorization."
        ),
    )

def render_operator_startup_status(packet: Any, *, evidence: str = "RHP-013.5") -> str:
    return "\n".join(build_operator_startup_status(packet, evidence=evidence).lines)
