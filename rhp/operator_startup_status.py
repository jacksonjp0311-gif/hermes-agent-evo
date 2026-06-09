# RHP-011 operator-visible startup status.
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

LOCK_LABELS = [
    ("repo_root", "repo root found"),
    ("rhp010_evidence", "RHP-010 evidence green"),
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

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def _ascii_bool(value: bool) -> str:
    return "OK" if value else "BLOCKED"

def build_operator_startup_status(packet: Any, *, evidence: str = "RHP-010") -> OperatorStartupStatus:
    data = packet.as_dict() if hasattr(packet, "as_dict") else dict(packet)
    boot_green = bool(data.get("boot_preflight_ok") or data.get("ok"))
    locks = {
        "repo_root": bool(data.get("repo_root")),
        "rhp010_evidence": boot_green,
        "hrcn_boundary": boot_green,
        "alignment_guard": boot_green,
        "startup_packet": bool(data.get("startup_context_packet_created")),
        "authority_false": all(data.get(key) is False for key in [
            "provider_call_executed", "model_call_executed", "tool_use_executed",
            "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
            "api_write", "dependency_mutation_committed", "external_ingestion",
            "self_authorization", "autonomous_authority",
        ]),
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
    ok = all(locks.values())
    phase = "pre-interaction"
    lines = ["RHP rehydration sequence:"]
    for key, label in LOCK_LABELS:
        lines.append(f"[{_ascii_bool(locks[key])}] {label}")
    lines.append(f"RHP rehydration complete: {'ok' if ok else 'blocked'} | phase={phase} | evidence={evidence}")
    lines.append("RHP authority boundary: provider/model/tool=false | CMS/memory/API=false | external_ingestion=false | autonomy=false")
    return OperatorStartupStatus(
        ok=ok,
        phase=phase,
        evidence=evidence,
        locks=locks,
        lines=lines,
        non_claim_lock=(
            "RHP-011 displays operator-visible startup locks only. It does not authorize tools, "
            "provider/model calls, CMS writes, memory writes, API writes, external ingestion, autonomy, or self-authorization."
        ),
    )

def render_operator_startup_status(packet: Any, *, evidence: str = "RHP-010") -> str:
    return "\n".join(build_operator_startup_status(packet, evidence=evidence).lines)
