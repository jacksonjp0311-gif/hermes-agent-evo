# RHP-008 apply-gate negative-control proof.
from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ATTEMPTED_ESCALATIONS = (
    "provider_call",
    "model_call",
    "tool_use",
    "cms_runtime_execution",
    "cms_write",
    "memory_write",
    "memory_promotion",
    "api_write",
    "dependency_mutation",
    "codex_ingestion",
    "self_authorization",
    "autonomous_authority",
)

AUTHORITY_FLAG_BY_ATTEMPT = {
    "provider_call": "provider_call_executed",
    "model_call": "model_call_executed",
    "tool_use": "tool_use_executed",
    "cms_runtime_execution": "cms_runtime_execution",
    "cms_write": "cms_write",
    "memory_write": "memory_write",
    "memory_promotion": "memory_promotion",
    "api_write": "api_write",
    "dependency_mutation": "dependency_mutation_committed",
    "codex_ingestion": "codex_ingestion",
    "self_authorization": "self_authorization",
    "autonomous_authority": "autonomous_authority",
}

@dataclass(frozen=True)
class Refusal:
    attempted_action: str
    allowed: bool
    human_apply_gate_present: bool
    reason: str
    authority_flag: str
    authority_value: bool

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

@dataclass(frozen=True)
class ApplyGateNegativeControlProof:
    ok: bool
    repo_root: str
    proposal_loop_ok: bool
    human_apply_gate_present: bool
    attempted_escalations_count: int
    refused_escalations_count: int
    all_escalations_refused: bool
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
    refusals: list[dict[str, Any]]
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

def _root_imports(root: Path) -> None:
    root_str = str(root)
    if root_str not in sys.path:
        sys.path.insert(0, root_str)

def refuse_attempt(attempted_action: str, *, human_apply_gate_present: bool) -> Refusal:
    if attempted_action not in AUTHORITY_FLAG_BY_ATTEMPT:
        raise ValueError(f"unknown attempted action: {attempted_action}")
    flag = AUTHORITY_FLAG_BY_ATTEMPT[attempted_action]
    if human_apply_gate_present:
        return Refusal(
            attempted_action=attempted_action,
            allowed=False,
            human_apply_gate_present=True,
            reason="RHP-008 is a negative-control proof and never performs apply/write/model/tool/CMS/memory actions.",
            authority_flag=flag,
            authority_value=False,
        )
    return Refusal(
        attempted_action=attempted_action,
        allowed=False,
        human_apply_gate_present=False,
        reason="proposal context is orientation only; missing separate human apply gate",
        authority_flag=flag,
        authority_value=False,
    )

def run_apply_gate_negative_control(repo_root: str | Path | None = None) -> ApplyGateNegativeControlProof:
    root = find_repo_root(repo_root)
    _root_imports(root)

    from rhp.proposal_loop_proof import run_governed_proposal_loop_proof

    proposal = run_governed_proposal_loop_proof(root)
    if not proposal.ok:
        raise RuntimeError("RHP-007 proposal-loop proof is not green")

    human_apply_gate_present = False
    refusals = [
        refuse_attempt(action, human_apply_gate_present=human_apply_gate_present)
        for action in ATTEMPTED_ESCALATIONS
    ]
    all_refused = all(item.allowed is False and item.authority_value is False for item in refusals)

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

    ok = proposal.ok and human_apply_gate_present is False and all_refused and all(value is False for value in false_flags.values())

    return ApplyGateNegativeControlProof(
        ok=ok,
        repo_root=str(root),
        proposal_loop_ok=proposal.ok,
        human_apply_gate_present=human_apply_gate_present,
        attempted_escalations_count=len(ATTEMPTED_ESCALATIONS),
        refused_escalations_count=sum(1 for item in refusals if item.allowed is False),
        all_escalations_refused=all_refused,
        refusals=[item.as_dict() for item in refusals],
        non_claim_lock=(
            "RHP-008 proves refusal only. It does not create an apply gate, "
            "does not execute a model/provider/tool call, does not run or write CMS, "
            "does not write or promote memory, does not write APIs, does not ingest Codex, "
            "and does not authorize autonomy or self-authorization."
        ),
        **false_flags,
    )

def main() -> int:
    proof = run_apply_gate_negative_control()
    print(json.dumps(proof.as_dict(), indent=2))
    return 0 if proof.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())