# RHP-013.4 startup context packet and RuntimeBootState.
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

def _anchor_repo_root() -> Path:
    current = Path(__file__).resolve()
    for candidate in (current.parent, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".git").exists():
            candidate_str = str(candidate)
            if candidate_str not in sys.path:
                sys.path.insert(0, candidate_str)
            return candidate
    raise RuntimeError("Could not locate Hermes repository root for startup context packet")

_anchor_repo_root()

from rhp.boot_preflight import run_boot_preflight

@dataclass(frozen=True)
class StartupContextPacket:
    ok: bool
    schema: str
    repo_root: str
    installed_launcher_path: str
    installed_launcher_exists: bool
    native_boot_hook_file: str
    native_boot_hook_present: bool
    boot_preflight_status: str
    boot_preflight_gate: str
    rhp_context_gate: str
    hrcn_context_gate: str
    boot_preflight_requested: bool
    rhp_context_requested: bool
    hrcn_context_requested: bool
    boot_preflight_ok: bool
    boot_preflight_degraded: bool
    boot_preflight_degraded_reason: str
    startup_context_packet_created: bool
    provider_call_executed: bool
    model_call_executed: bool
    tool_use_executed: bool
    cms_runtime_execution: bool
    cms_write: bool
    memory_write: bool
    memory_promotion: bool
    api_write: bool
    dependency_mutation_committed: bool
    external_ingestion: bool
    self_authorization: bool
    autonomous_authority: bool
    operator_visible_status: str
    non_claim_lock: str

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

RUNTIME_BOOT_STATE_SCHEMA = "RHP-RUNTIME-BOOT-STATE-v0.1"

RUNTIME_AUTHORITY_FALSE_KEYS = (
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
    "self_authorization",
    "autonomous_authority",
)

@dataclass(frozen=True)
class RuntimeBootState:
    ok: bool
    schema: str
    evidence: str
    repo_root: str
    phase: str
    status: str
    degraded: bool
    degraded_reason: str
    entrypoint: str
    interface: str
    profile: str
    session_id: str
    boot_preflight_packet_schema: str
    startup_context_packet_schema: str
    boot_preflight_ok: bool
    startup_packet_ok: bool
    locks: dict[str, bool]
    authority: dict[str, bool]
    operator_status_text: str
    protocol_strip: str
    protocol_locks: list[str]
    prompt_context_json: str
    env: dict[str, str]
    non_claim_lock: str

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def find_repo_root(start: str | Path | None = None) -> Path:
    current = Path(start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".git").exists():
            return candidate
    raise FileNotFoundError("Could not locate Hermes repository root")

def _env_enabled(name: str) -> bool:
    return (os.environ.get(name) or "").strip().lower() in {"1", "true", "yes", "on", "proposal", "preflight"}

def build_startup_context_packet(repo_root: str | Path | None = None) -> StartupContextPacket:
    root = find_repo_root(repo_root)
    boot = run_boot_preflight(root)
    launcher = root / ".venv" / "Scripts" / "hermes.exe"
    main_file = root / "hermes_cli" / "main.py"
    main_text = main_file.read_text(encoding="utf-8", errors="replace")
    false_flags = {
        "provider_call_executed": False,
        "model_call_executed": False,
        "tool_use_executed": False,
        "cms_runtime_execution": False,
        "cms_write": False,
        "memory_write": False,
        "memory_promotion": False,
        "api_write": False,
        "dependency_mutation_committed": False,
        "external_ingestion": False,
        "self_authorization": False,
        "autonomous_authority": False,
    }
    native_hook_present = "RHP-010 RUNTIME-NATIVE BOOT INTERCONNECT START" in main_text
    status = os.environ.get("HERMES_RHP_BOOT_PREFLIGHT_STATUS", "")
    ok = bool(boot.ok and launcher.exists() and native_hook_present and all(value is False for value in false_flags.values()))
    return StartupContextPacket(
        ok=ok,
        schema="RHP-STARTUP-CONTEXT-PACKET-v0.4",
        repo_root=str(root),
        installed_launcher_path=str(launcher),
        installed_launcher_exists=launcher.exists(),
        native_boot_hook_file="hermes_cli/main.py",
        native_boot_hook_present=native_hook_present,
        boot_preflight_status=status,
        boot_preflight_gate="HERMES_RHP_BOOT_PREFLIGHT",
        rhp_context_gate="HERMES_RHP_CONTEXT",
        hrcn_context_gate="HERMES_HRCN_CONTEXT",
        boot_preflight_requested=_env_enabled("HERMES_RHP_BOOT_PREFLIGHT"),
        rhp_context_requested=_env_enabled("HERMES_RHP_CONTEXT"),
        hrcn_context_requested=_env_enabled("HERMES_HRCN_CONTEXT"),
        boot_preflight_ok=bool(boot.ok),
        boot_preflight_degraded=bool(getattr(boot, "degraded", False)),
        boot_preflight_degraded_reason=str(getattr(boot, "degraded_reason", "")),
        startup_context_packet_created=True,
        operator_visible_status=os.environ.get("HERMES_RHP_OPERATOR_STATUS", ""),
        non_claim_lock=(
            "RHP-012 startup packet verifies the installed CLI path can carry safe read-only boot orientation, "
            "degraded startup status, and the gold-interface Rehydration Protocol strip. "
            "It does not execute Hermes autonomously, call providers/models/tools, write CMS or memory, write APIs, "
            "mutate dependencies, perform external ingestion, or self-authorize."
        ),
        **false_flags,
    )

def _selected_rhp_env() -> dict[str, str]:
    names = (
        "HERMES_RHP_NATIVE_BOOT",
        "HERMES_RHP_BOOT_PREFLIGHT",
        "HERMES_RHP_CONTEXT",
        "HERMES_HRCN_CONTEXT",
        "HERMES_RHP_BOOT_PREFLIGHT_STATUS",
        "HERMES_RHP_OPERATOR_STATUS",
        "HERMES_RHP_PROTOCOL_STRIP",
        "HERMES_RHP_PROTOCOL_LOCKS",
    )
    return {name: os.environ.get(name, "") for name in names}

def build_runtime_boot_state(
    repo_root: str | Path | None = None,
    *,
    entrypoint: str = "hermes",
    interface: str = "cli",
    profile: str = "runtime",
    session_id: str = "",
) -> RuntimeBootState:
    packet = build_startup_context_packet(repo_root)
    root = find_repo_root(repo_root)
    packet_data = packet.as_dict()
    authority = {key: bool(packet_data.get(key, False)) for key in RUNTIME_AUTHORITY_FALSE_KEYS}
    authority_false = all(value is False for value in authority.values())
    locks = {
        "repo_root_found": True,
        "boot_preflight_ok": bool(packet.boot_preflight_ok),
        "native_boot_hook_present": bool(packet.native_boot_hook_present),
        "startup_context_packet_created": bool(packet.startup_context_packet_created),
        "authority_false": authority_false,
        "external_ingestion_false": authority.get("external_ingestion") is False,
        "cms_memory_api_write_false": (
            authority.get("cms_write") is False
            and authority.get("memory_write") is False
            and authority.get("api_write") is False
        ),
    }
    failed_locks = [name for name, ok in locks.items() if ok is not True]
    degraded = bool(packet.boot_preflight_degraded or failed_locks)
    degraded_reason = packet.boot_preflight_degraded_reason or (", ".join(failed_locks) if failed_locks else "")
    ok = bool(all(value is True for value in locks.values()) and not degraded)
    status = "verified" if ok else "degraded"
    protocol_locks = [f"{name}={str(value).lower()}" for name, value in locks.items()]
    protocol_strip = f"RHP RuntimeBootState: {status} | phase=pre-interaction | evidence=RHP-013.4 | authority=false"
    prompt_payload = {
        "schema": RUNTIME_BOOT_STATE_SCHEMA,
        "evidence": "RHP-013.4",
        "phase": "pre-interaction",
        "status": status,
        "degraded": degraded,
        "authority": authority,
        "locks": locks,
    }
    return RuntimeBootState(
        ok=ok,
        schema=RUNTIME_BOOT_STATE_SCHEMA,
        evidence="RHP-013.4",
        repo_root=str(root),
        phase="pre-interaction",
        status=status,
        degraded=degraded,
        degraded_reason=degraded_reason,
        entrypoint=entrypoint,
        interface=interface,
        profile=profile,
        session_id=session_id,
        boot_preflight_packet_schema="RHP-BOOT-PREFLIGHT-PACKET-v0.3",
        startup_context_packet_schema=packet.schema,
        boot_preflight_ok=bool(packet.boot_preflight_ok),
        startup_packet_ok=bool(packet.startup_context_packet_created),
        locks=locks,
        authority=authority,
        operator_status_text=packet.operator_visible_status,
        protocol_strip=protocol_strip,
        protocol_locks=protocol_locks,
        prompt_context_json=json.dumps(prompt_payload, sort_keys=True),
        env=_selected_rhp_env(),
        non_claim_lock=(
            "RHP-013.4 RuntimeBootState is the typed read-only boot truth packet wired into operator and banner surfaces. "
            "It normalizes startup/preflight/operator/protocol state for future consumers. "
            "It does not call providers/models/tools, write CMS or memory, write APIs, "
            "perform external ingestion, grant autonomy, or self-authorize."
        ),
    )

def runtime_boot_state_json(repo_root: str | Path | None = None) -> str:
    return json.dumps(build_runtime_boot_state(repo_root).as_dict(), indent=2, sort_keys=True)

def runtime_boot_state_from_env(repo_root: str | Path | None = None) -> RuntimeBootState:
    return build_runtime_boot_state(repo_root)


def packet_json(repo_root: str | Path | None = None) -> str:
    return json.dumps(build_startup_context_packet(repo_root).as_dict(), indent=2, sort_keys=True)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build RHP-012 startup context packet")
    parser.add_argument("--json", action="store_true")
    parser.parse_args(argv)
    packet = build_startup_context_packet()
    print(json.dumps(packet.as_dict(), indent=2, sort_keys=True))
    return 0 if packet.ok else 2

if __name__ == "__main__":
    raise SystemExit(main())