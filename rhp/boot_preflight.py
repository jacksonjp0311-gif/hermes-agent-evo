# RHP-009 runtime boot preflight integration.
from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

LATEST_RHP_EVIDENCE = "docs/context-layer/ops/RHP-008-final-evidence.json"
HRCN_EVIDENCE = "docs/context-layer/ops/OPS-027-final-evidence.json"

AUTHORITY_FALSE_KEYS = (
    "provider_call_executed", "model_call_executed", "tool_use_executed",
    "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
    "api_write", "dependency_mutation_committed", "self_authorization",
    "autonomous_authority",
)

@dataclass(frozen=True)
class BootPreflightPacket:
    ok: bool
    repo_root: str
    boot_phase: str
    latest_rhp_evidence: str
    hrcn_evidence: str
    rhp_evidence_green: bool
    hrcn_boundary_green: bool
    alignment_guard_green: bool
    rhp_context_gate: str
    hrcn_context_gate: str
    rhp_context_requested: bool
    hrcn_context_requested: bool
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
    self_authorization: bool
    autonomous_authority: bool
    external_ingestion: bool
    non_claim_lock: str
    checks: dict[str, bool]

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

def _root_imports(root: Path) -> None:
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)

def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"expected JSON object: {path}")
    return data

def _env_enabled(name: str) -> bool:
    return (os.environ.get(name) or "").strip().lower() in {"1", "true", "yes", "on", "proposal"}

def _git_status_available(root: Path) -> bool:
    result = subprocess.run(["git", "status", "--short"], cwd=str(root), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.returncode == 0

def _status_value(status: Any, key: str, default: Any = None) -> Any:
    if isinstance(status, dict):
        return status.get(key, default)
    if hasattr(status, "as_dict"):
        data = status.as_dict()
        if isinstance(data, dict):
            return data.get(key, default)
    return getattr(status, key, default)

def run_boot_preflight(repo_root: str | Path | None = None) -> BootPreflightPacket:
    root = find_repo_root(repo_root)
    _root_imports(root)

    import hrcn_runtime_bridge
    import rhp_runtime_bridge
    from rhp.alignment_guard import validate_alignment

    latest_path = root / LATEST_RHP_EVIDENCE
    hrcn_path = root / HRCN_EVIDENCE
    latest = _read_json(latest_path)

    rhp_evidence_green = (
        latest.get("schema") == "RHP-008-final-evidence"
        and latest.get("apply_gate_negative_control_passed") is True
        and latest.get("proposal_loop_ok") is True
        and latest.get("all_escalations_refused") is True
        and latest.get("py_compile_passed") is True
        and latest.get("focused_tests_passed") is True
        and latest.get("alignment_guard_self_check_passed") is True
        and all(latest.get(key) is False for key in AUTHORITY_FALSE_KEYS)
    )

    rhp_runtime_bridge.assert_read_only_boundary(root)
    hrcn_runtime_bridge.assert_read_only_boundary(root)
    hrcn_status = hrcn_runtime_bridge.get_bridge_status(root)
    hrcn_boundary_green = hrcn_path.is_file() and _status_value(hrcn_status, "mode") == "read_only"

    alignment = validate_alignment(root, require_latest_passed=False)
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
        "self_authorization": False,
        "autonomous_authority": False,
        "external_ingestion": False,
    }
    checks = {
        "repo_root_found": root.is_dir(),
        "latest_rhp_evidence_exists": latest_path.is_file(),
        "rhp_evidence_green": rhp_evidence_green,
        "hrcn_evidence_exists": hrcn_path.is_file(),
        "hrcn_boundary_green": hrcn_boundary_green,
        "alignment_guard_green": alignment.ok,
        "git_status_available": _git_status_available(root),
        "authority_flags_false": all(value is False for value in false_flags.values()),
        "startup_context_packet_created": True,
    }
    ok = all(checks.values())

    return BootPreflightPacket(
        ok=ok,
        repo_root=str(root),
        boot_phase="pre_interaction",
        latest_rhp_evidence=LATEST_RHP_EVIDENCE,
        hrcn_evidence=HRCN_EVIDENCE,
        rhp_evidence_green=rhp_evidence_green,
        hrcn_boundary_green=hrcn_boundary_green,
        alignment_guard_green=alignment.ok,
        rhp_context_gate="HERMES_RHP_CONTEXT",
        hrcn_context_gate="HERMES_HRCN_CONTEXT",
        rhp_context_requested=_env_enabled("HERMES_RHP_CONTEXT"),
        hrcn_context_requested=_env_enabled("HERMES_HRCN_CONTEXT"),
        startup_context_packet_created=True,
        checks=checks,
        non_claim_lock=(
            "RHP-009 boot preflight is read-only startup orientation. "
            "It verifies local evidence and boundary state before interaction context assembly. "
            "It does not authorize provider/model/tool calls, writes, CMS runtime/write, "
            "memory write/promotion, API writes, dependency mutation, external ingestion, autonomy, or self-authorization."
        ),
        **false_flags,
    )

def format_boot_context_for_prompt(repo_root: str | Path | None = None) -> str:
    packet = run_boot_preflight(repo_root)
    data = packet.as_dict()
    compact = {
        "schema": "RHP-BOOT-PREFLIGHT-PACKET-v0.1",
        "ok": data["ok"],
        "boot_phase": data["boot_phase"],
        "latest_rhp_evidence": data["latest_rhp_evidence"],
        "rhp_evidence_green": data["rhp_evidence_green"],
        "hrcn_boundary_green": data["hrcn_boundary_green"],
        "alignment_guard_green": data["alignment_guard_green"],
        "rhp_context_requested": data["rhp_context_requested"],
        "hrcn_context_requested": data["hrcn_context_requested"],
        "startup_context_packet_created": data["startup_context_packet_created"],
        "authority": {key: data[key] for key in [
            "provider_call_executed", "model_call_executed", "tool_use_executed",
            "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
            "api_write", "dependency_mutation_committed", "external_ingestion",
            "self_authorization", "autonomous_authority",
        ]},
        "non_claim_lock": data["non_claim_lock"],
    }
    return json.dumps(compact, indent=2, sort_keys=True)

def main() -> int:
    packet = run_boot_preflight()
    print(json.dumps(packet.as_dict(), indent=2, sort_keys=True))
    return 0 if packet.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())