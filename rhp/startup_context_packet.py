# RHP-011.1 startup context packet.
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
        schema="RHP-STARTUP-CONTEXT-PACKET-v0.3",
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
        boot_preflight_ok=boot.ok,
        startup_context_packet_created=True,
        operator_visible_status=os.environ.get("HERMES_RHP_OPERATOR_STATUS", ""),
        non_claim_lock=(
            "RHP-011.1 startup packet verifies the installed CLI path can carry read-only boot orientation and the gold-interface Rehydration Protocol strip. "
            "It does not execute Hermes autonomously, call providers/models/tools, write CMS or memory, write APIs, "
            "mutate dependencies, perform external ingestion, or self-authorize."
        ),
        **false_flags,
    )

def packet_json(repo_root: str | Path | None = None) -> str:
    return json.dumps(build_startup_context_packet(repo_root).as_dict(), indent=2, sort_keys=True)

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build RHP-010 startup context packet")
    parser.add_argument("--json", action="store_true")
    parser.parse_args(argv)
    packet = build_startup_context_packet()
    print(json.dumps(packet.as_dict(), indent=2, sort_keys=True))
    return 0 if packet.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())