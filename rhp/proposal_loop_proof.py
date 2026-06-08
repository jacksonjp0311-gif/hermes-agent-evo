# RHP-007 governed proposal-loop proof.
from __future__ import annotations

import contextlib
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

FORBIDDEN_AUTHORITY_KEYS = (
    "provider_call_executed", "model_call_executed", "tool_use_executed",
    "runtime_source_mutation", "cms_runtime_execution", "cms_write",
    "memory_write", "memory_promotion", "api_write",
    "dependency_mutation_committed", "env_file_committed", "rollback_executed",
    "self_authorization", "ongoing_provider_authority", "autonomous_authority",
)

@dataclass(frozen=True)
class ProposalLoopProof:
    ok: bool
    repo_root: str
    rhp_packet_schema: str
    hrcn_packet_schema: str
    rhp_before_hrcn: bool
    proposal_context_contains_rhp: bool
    proposal_context_contains_hrcn: bool
    provider_call_executed: bool
    model_call_executed: bool
    tool_use_executed: bool
    cms_runtime_execution: bool
    cms_write: bool
    memory_write: bool
    memory_promotion: bool
    api_write: bool
    dependency_mutation_committed: bool
    codex_ingestion: bool
    self_authorization: bool
    autonomous_authority: bool
    forbidden_authority_all_false: bool
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

@contextlib.contextmanager
def _temporary_env(updates: dict[str, str]):
    old = {key: os.environ.get(key) for key in updates}
    try:
        for key, value in updates.items():
            os.environ[key] = value
        yield
    finally:
        for key, value in old.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value

def _all_false(mapping: dict[str, Any]) -> bool:
    return all(mapping.get(key) is False for key in FORBIDDEN_AUTHORITY_KEYS if key in mapping)

def run_governed_proposal_loop_proof(repo_root: str | Path | None = None) -> ProposalLoopProof:
    root = find_repo_root(repo_root)
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)

    import rhp_runtime_bridge
    import hrcn_runtime_bridge
    from agent import agent_init

    rhp_runtime_bridge.assert_read_only_boundary(root)
    hrcn_runtime_bridge.assert_read_only_boundary(root)

    rhp_packet = rhp_runtime_bridge.make_runtime_context_packet(root)
    hrcn_packet = hrcn_runtime_bridge.make_gui_context_packet(root)
    rhp_authority = rhp_packet["bridge_status"]["authority"]
    hrcn_authority = hrcn_packet["bridge_status"]["authority"]

    if not _all_false(rhp_authority):
        raise RuntimeError("RHP authority flags are not all false")
    if not _all_false(hrcn_authority):
        raise RuntimeError("HRCN authority flags are not all false")

    with _temporary_env({"HERMES_RHP_CONTEXT": "proposal", "HERMES_HRCN_CONTEXT": "proposal"}):
        proposal_prompt = agent_init._maybe_append_hrcn_context(
            agent_init._maybe_append_rhp_context("RHP-007 BASE PROPOSAL CONTEXT")
        )

    rhp_marker = "[RHP ORIGIN-ALIGNMENT CONTEXT]"
    hrcn_marker = "[HRCN READ-ONLY RUNTIME CONTEXT]"
    contains_rhp = rhp_marker in proposal_prompt
    contains_hrcn = hrcn_marker in proposal_prompt
    rhp_before_hrcn = contains_rhp and contains_hrcn and proposal_prompt.index(rhp_marker) < proposal_prompt.index(hrcn_marker)

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
        "codex_ingestion": False,
        "self_authorization": False,
        "autonomous_authority": False,
    }
    forbidden_all_false = all(value is False for value in false_flags.values()) and _all_false(rhp_authority) and _all_false(hrcn_authority)
    ok = (
        contains_rhp
        and contains_hrcn
        and rhp_before_hrcn
        and rhp_packet.get("packet_schema") == "RHP-HERMES-RUNTIME-CONTEXT-PACKET-v0.1"
        and hrcn_packet.get("packet_schema") == "HRCN-GUI-RUNTIME-CONTEXT-PACKET-v0.3"
        and forbidden_all_false
    )
    return ProposalLoopProof(
        ok=ok,
        repo_root=str(root),
        rhp_packet_schema=str(rhp_packet.get("packet_schema", "")),
        hrcn_packet_schema=str(hrcn_packet.get("packet_schema", "")),
        rhp_before_hrcn=rhp_before_hrcn,
        proposal_context_contains_rhp=contains_rhp,
        proposal_context_contains_hrcn=contains_hrcn,
        forbidden_authority_all_false=forbidden_all_false,
        non_claim_lock="RHP-007 proves only the local read-only proposal-context order. It does not execute a model, call a provider, call tools, run CMS, write memory, promote memory, mutate runtime source, ingest Codex, operate autonomously, or self-authorize.",
        **false_flags,
    )

def main() -> int:
    proof = run_governed_proposal_loop_proof()
    print(json.dumps(proof.as_dict(), indent=2))
    return 0 if proof.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())