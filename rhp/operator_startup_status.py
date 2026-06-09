# RHP-012 operator-visible startup status with degraded mode.
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

def build_operator_startup_status(packet: Any, *, evidence: str = "RHP-012") -> OperatorStartupStatus:
    data = _data(packet)
    checks = data.get("checks") if isinstance(data.get("checks"), dict) else {}
    boot_green = bool(data.get("boot_preflight_ok") or data.get("ok"))

    authority_false = all(data.get(key) is False for key in [
        "provider_call_executed", "model_call_executed", "tool_use_executed",
        "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
        "api_write", "dependency_mutation_committed", "external_ingestion",
        "self_authorization", "autonomous_authority",
    ])

    locks = {
        "repo_root": bool(data.get("repo_root")),
        "rhp_evidence": bool(checks.get("rhp_evidence_green", data.get("rhp_evidence_green", boot_green))),
        "hrcn_boundary": bool(checks.get("hrcn_boundary_green", data.get("hrcn_boundary_green", boot_green))),
        "alignment_guard": bool(checks.get("alignment_guard_green", data.get("alignment_guard_green", boot_green))),
        "startup_packet": bool(data.get("startup_context_packet_created")),
        "authority_false": authority_false,
        "external_ingestion_false": data.get("external_ingestion") is False,
        "provider_model_tool_false": (
            data.get("provider_call_executed") is False
            and data.get("model_call_executed") is False
            and data.get("tool_use_executed") is False
        ),
        "cms_memory_api_false": (
            data.get("cms_runtime_execution") is False
            and data.get("cms_write") is False
            and data.get("memory_write") is False
            and data.get("memory_promotion") is False
            and data.get("api_write") is False
        ),
    }

    ok = all(locks.values()) and boot_green
    degraded = bool(data.get("degraded")) or not ok
    status = "ok" if ok else "degraded"
    phase = "pre-interaction"
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
            "RHP-012 displays safe startup locks with degraded status when evidence or alignment is not green. "
            "It does not authorize tools, provider/model calls, CMS writes, memory writes, API writes, "
            "external ingestion, autonomy, or self-authorization."
        ),
    )

def render_operator_startup_status(packet: Any, *, evidence: str = "RHP-012") -> str:
    return "\n".join(build_operator_startup_status(packet, evidence=evidence).lines)