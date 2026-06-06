# Read-only HRCN runtime bridge for Hermes.
#
# This module exposes the sealed HRCN bounded-loop state to Hermes runtime
# surfaces without granting write/apply/tool/runtime authority.

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping


FORBIDDEN_AUTHORITIES = {
    "provider_call_executed": False,
    "model_call_executed": False,
    "tool_use_executed": False,
    "runtime_source_mutation": False,
    "cms_runtime_execution": False,
    "cms_write": False,
    "memory_write": False,
    "api_write": False,
    "dependency_mutation_committed": False,
    "env_file_committed": False,
    "rollback_executed": False,
    "self_authorization": False,
    "ongoing_provider_authority": False,
    "autonomous_authority": False,
}


@dataclass(frozen=True)
class HRCNBridgeStatus:
    enabled: bool
    mode: str
    repo_root: str
    sealed_anchor_tag: str
    current_state: str
    latest_evidence_path: str
    next_recommended_operation: str
    authority: Mapping[str, bool]
    non_claim_lock: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "mode": self.mode,
            "repo_root": self.repo_root,
            "sealed_anchor_tag": self.sealed_anchor_tag,
            "current_state": self.current_state,
            "latest_evidence_path": self.latest_evidence_path,
            "next_recommended_operation": self.next_recommended_operation,
            "authority": dict(self.authority),
            "non_claim_lock": self.non_claim_lock,
        }


def find_repo_root(start: str | Path | None = None) -> Path:
    current = Path(start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".git").exists():
            return candidate
    raise FileNotFoundError("Could not locate Hermes repository root")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def load_hrcn_context(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    evidence_path = root / "docs" / "context-layer" / "ops" / "OPS-020-final-evidence.json"
    if not evidence_path.is_file():
        raise FileNotFoundError(str(evidence_path))
    evidence = _load_json(evidence_path)
    if evidence.get("bounded_loop_v0_2_seal_passed") is not True:
        raise RuntimeError("HRCN bounded loop v0.2 seal is not marked passed")
    for key, expected in FORBIDDEN_AUTHORITIES.items():
        if evidence.get(key) is not expected:
            raise RuntimeError(f"HRCN authority boundary mismatch: {key}")
    return {"repo_root": str(root), "latest_evidence_path": str(evidence_path.relative_to(root)), "evidence": evidence}


def get_bridge_status(repo_root: str | Path | None = None) -> HRCNBridgeStatus:
    context = load_hrcn_context(repo_root)
    evidence = context["evidence"]
    return HRCNBridgeStatus(
        enabled=True,
        mode="read_only",
        repo_root=context["repo_root"],
        sealed_anchor_tag=str(evidence.get("new_tag", "hrcn-ops-v0.2.0")),
        current_state="HRCN OPS v0.2.0 bounded loop sealed",
        latest_evidence_path=context["latest_evidence_path"],
        next_recommended_operation=str(evidence.get("next_recommended_operation", "OPS-021 governed runtime bridge interface design")),
        authority=FORBIDDEN_AUTHORITIES,
        non_claim_lock=(
            "HRCN runtime bridge is read-only. It provides orientation only and "
            "does not authorize tools, runtime mutation, CMS write, memory write, "
            "API write, dependency mutation, autonomy, or self-authorization."
        ),
    )


def make_gui_context_packet(repo_root: str | Path | None = None) -> dict[str, Any]:
    status = get_bridge_status(repo_root)
    return {
        "packet_schema": "HRCN-GUI-RUNTIME-CONTEXT-PACKET-v0.1",
        "bridge_status": status.as_dict(),
        "bounded_loop_formula": "observe -> retrieve bounded context -> classify authority -> propose -> dry-run -> evidence -> human gate -> limited apply only if authorized",
        "allowed_runtime_use": ["display HRCN status", "include HRCN boundary summary in session context", "orient proposals to the sealed HRCN loop"],
        "forbidden_runtime_use": ["grant tool authority", "grant provider/model authority", "mutate runtime source", "execute CMS runtime", "write CMS", "write memory", "write APIs", "change dependencies", "operate autonomously", "self-authorize"],
    }


def format_context_for_prompt(repo_root: str | Path | None = None) -> str:
    packet = make_gui_context_packet(repo_root)
    status = packet["bridge_status"]
    forbidden = ", ".join(packet["forbidden_runtime_use"])
    return (
        "HRCN Runtime Bridge: READ ONLY\n"
        f"State: {status['current_state']}\n"
        f"Anchor: {status['sealed_anchor_tag']}\n"
        f"Evidence: {status['latest_evidence_path']}\n"
        f"Next: {status['next_recommended_operation']}\n"
        f"Loop: {packet['bounded_loop_formula']}\n"
        f"Forbidden: {forbidden}\n"
        f"Lock: {status['non_claim_lock']}"
    )


def assert_read_only_boundary(repo_root: str | Path | None = None) -> bool:
    status = get_bridge_status(repo_root)
    if status.mode != "read_only":
        raise RuntimeError("HRCN bridge mode is not read_only")
    for key, value in status.authority.items():
        if value is not False:
            raise RuntimeError(f"HRCN bridge authority is not false: {key}")
    return True
