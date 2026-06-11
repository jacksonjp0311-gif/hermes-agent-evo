from __future__ import annotations
import argparse, json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RHP_ZERO_CONTEXT_REBUILD_SCHEMA = "RHP-ZERO-CONTEXT-REBUILD-v0.3"
AUTHORITY_KEYS = ["provider_call_executed","model_call_executed","tool_use_executed","cms_runtime_execution","cms_write","memory_write","memory_promotion","api_write","dependency_mutation_committed","external_ingestion","autonomous_authority","self_authorization"]

@dataclass(frozen=True)
class ZeroContextRebuild:
    schema: str
    ok: bool
    latest_operation: str
    latest_evidence: str
    latest_commit_or_base: str
    next_operation: str
    active_sequence: list[str]
    required_read_order: list[str]
    required_gates: list[str]
    authority_locks: dict[str, bool]
    roles: dict[str, str]
    non_claim_lock: str
    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def find_latest_evidence(root: Path) -> Path:
    candidates = sorted((root / "docs" / "context-layer" / "ops").glob("RHP-*-final-evidence.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not candidates:
        raise FileNotFoundError("no RHP final evidence found")
    return candidates[0]

def build_packet(root: str | Path = ".") -> ZeroContextRebuild:
    root = Path(root)
    evidence_path = find_latest_evidence(root)
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    authority = {k: bool(evidence.get(k, False)) for k in AUTHORITY_KEYS}
    ok = all(v is False for v in authority.values())
    return ZeroContextRebuild(
        RHP_ZERO_CONTEXT_REBUILD_SCHEMA,
        ok,
        str(evidence.get("operation", "unknown")),
        str(evidence_path.as_posix()),
        str(evidence.get("base_commit", "unknown")),
        str(evidence.get("next_recommended_operation", "unknown")),
        ["ENTRYPOINT-GATE","ROOT-ANCHOR","RESIDUE-MANAGER","AUTOHEAL-PREFLIGHT","PULL-REBASE","HUMAN-AUTHORIZATION","OPERATION","VALIDATION","EVIDENCE","BOUNDARY","SECRET-SCAN","CURRENT-SCRIPT-GATE","COMMAND-RUNNER","STREAM-COLLAPSE","ERROR-BOX","GITHUB-PUSH-BOX","HUMAN-UI-SUMMARY","RETURN-ROOT"],
        ["docs/context-layer/latest-rhp.json","docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md","docs/context-layer/all-one-script-contract.md","docs/context-layer/rhp_gate_checklist.md","README.md","AGENTS.md","rhp/README.md",str(evidence_path.as_posix())],
        ["entrypoint must be file invocation","residue manager must classify failed-run residue","operator_script_name must match expected script","operation in evidence must match current operation","authority locks must remain false","unknown dirty paths must block","no push before current-script gate"],
        authority,
        {"Hermes":"agent/runtime surface and operator shell candidate","RHP":"governance, evidence, reconstruction, residue classification, and safety gating","All-One":"local human-authorized actuator","Evidence":"proof memory and zero-context replay surface","Human":"authorization boundary"},
        "Zero-context rebuild reconstructs loop state only. It grants no provider/model/tool/CMS/memory/API/autonomous/self-authorization authority.",
    )

def render_markdown(packet: ZeroContextRebuild) -> str:
    lines = ["# RHP Zero-Context Rebuild Packet","",f"- schema: `{packet.schema}`",f"- ok: `{packet.ok}`",f"- latest operation: `{packet.latest_operation}`",f"- latest evidence: `{packet.latest_evidence}`",f"- latest commit/base: `{packet.latest_commit_or_base}`",f"- next operation: `{packet.next_operation}`","","## Required read order"]
    lines += [f"{i+1}. `{item}`" for i, item in enumerate(packet.required_read_order)]
    lines += ["","## Active sequence"] + [f"{i+1}. `{item}`" for i, item in enumerate(packet.active_sequence)]
    lines += ["","## Required gates"] + [f"- {item}" for item in packet.required_gates]
    lines += ["","## Authority locks"] + [f"- `{k}`: `{v}`" for k, v in packet.authority_locks.items()]
    lines += ["","## Roles"] + [f"- {k}: {v}" for k, v in packet.roles.items()]
    lines += ["",f"Non-claim lock: {packet.non_claim_lock}",""]
    return "\n".join(lines)

def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", default=".")
    p.add_argument("--out-json", default="")
    p.add_argument("--out-md", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    packet = build_packet(args.repo_root)
    if args.out_json:
        Path(args.out_json).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_json).write_text(json.dumps(packet.as_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.out_md:
        Path(args.out_md).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_md).write_text(render_markdown(packet), encoding="utf-8", newline="\n")
    print(json.dumps(packet.as_dict(), indent=2, ensure_ascii=False) if args.json else render_markdown(packet))
    return 0 if packet.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
