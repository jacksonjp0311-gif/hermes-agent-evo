
# RHP-013.8 loop registry enforcement.
from __future__ import annotations
import argparse, json
from dataclasses import dataclass, field
from typing import Any

RHP_LOOP_REGISTRY_SCHEMA = "RHP-LOOP-REGISTRY-v0.1"

@dataclass(frozen=True)
class LoopDefinition:
    name: str
    purpose: str
    mutation_allowed: bool
    commit_allowed: bool
    max_attempts: int
    required_inputs: list[str] = field(default_factory=list)
    required_outputs: list[str] = field(default_factory=list)
    allowed_next: list[str] = field(default_factory=list)
    non_claim_lock: str = "Loop definition grants no authority outside its explicit boundary."

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def build_registry() -> dict[str, LoopDefinition]:
    return {
        "REHYDRATION": LoopDefinition("REHYDRATION", "Load repo truth, latest evidence, transcript, and boundary state.", False, False, 1, ["repo_root"], ["rehydration_status"], ["DIAGNOSIS", "CI-WATCH", "EVOLUTION"]),
        "DIAGNOSIS": LoopDefinition("DIAGNOSIS", "Classify state or failure before mutation.", False, False, 2, ["evidence_or_failure_text"], ["classification"], ["CI-REPAIR", "AUTOHEAL-PLAN", "NO-OP"]),
        "CI-WATCH": LoopDefinition("CI-WATCH", "Observe CI state without mutation.", False, False, 3, ["commit_sha"], ["ci_watch_packet"], ["DIAGNOSIS", "CI-REPAIR", "NO-OP"]),
        "CI-REPAIR": LoopDefinition("CI-REPAIR", "Repair a classified CI failure inside an allowlisted boundary.", True, True, 2, ["classification", "allowed_paths"], ["repair_evidence", "focused_tests"], ["CI-WATCH", "AUTOHEAL-PLAN"]),
        "EVOLUTION": LoopDefinition("EVOLUTION", "Add bounded capability with evidence and tests.", True, True, 1, ["proposal", "allowed_paths"], ["final_evidence", "tests"], ["CI-WATCH"]),
        "AUTOHEAL-PLAN": LoopDefinition("AUTOHEAL-PLAN", "Generate a bounded autoheal plan without mutation.", False, False, 2, ["classification", "transcript"], ["autoheal_plan"], ["AUTOHEAL-EXECUTE", "DIAGNOSIS"]),
        "AUTOHEAL-EXECUTE": LoopDefinition("AUTOHEAL-EXECUTE", "Execute one approved bounded autoheal plan.", True, True, 1, ["approved_plan", "allowed_paths"], ["repair_evidence", "tests"], ["CI-WATCH", "DIAGNOSIS"]),
        "NO-OP": LoopDefinition("NO-OP", "Seal evidence that no mutation is needed.", False, True, 1, ["reason"], ["no_op_evidence"], ["CI-WATCH", "REHYDRATION"]),
    }

def registry_as_dict() -> dict[str, Any]:
    reg = build_registry()
    return {"schema": RHP_LOOP_REGISTRY_SCHEMA, "loops": {name: loop.as_dict() for name, loop in reg.items()}}

def validate_loop(name: str, *, mutation_requested: bool = False, commit_requested: bool = False, attempt: int = 1) -> tuple[bool, list[str]]:
    reg = build_registry()
    failures: list[str] = []
    loop = reg.get(name)
    if loop is None:
        return False, [f"unknown_loop:{name}"]
    if mutation_requested and not loop.mutation_allowed:
        failures.append("mutation_not_allowed")
    if commit_requested and not loop.commit_allowed:
        failures.append("commit_not_allowed")
    if attempt < 1 or attempt > loop.max_attempts:
        failures.append("attempt_budget_exceeded")
    return not failures, failures

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="RHP loop registry")
    p.add_argument("--loop", default="")
    p.add_argument("--mutation-requested", action="store_true")
    p.add_argument("--commit-requested", action="store_true")
    p.add_argument("--attempt", type=int, default=1)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    if not args.loop:
        print(json.dumps(registry_as_dict(), indent=2, ensure_ascii=False))
        return 0
    ok, failures = validate_loop(args.loop, mutation_requested=args.mutation_requested, commit_requested=args.commit_requested, attempt=args.attempt)
    result = {"schema": RHP_LOOP_REGISTRY_SCHEMA, "loop": args.loop, "ok": ok, "failures": failures}
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
