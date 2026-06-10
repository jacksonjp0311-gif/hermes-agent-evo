
# RHP-014.0 current script gate.
from __future__ import annotations
import argparse, json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RHP_CURRENT_SCRIPT_GATE_SCHEMA = "RHP-CURRENT-SCRIPT-GATE-v0.1"

@dataclass(frozen=True)
class CurrentScriptGate:
    schema: str
    ok: bool
    operation: str
    expected_script: str
    actual_script: str
    evidence_script: str
    failures: list[str] = field(default_factory=list)
    glyph: str = "[OK]"
    non_claim_lock: str = (
        "Current-script gate verifies script/evidence identity only. It grants no runtime, provider, tool, CMS, memory, API, external-ingestion, autonomous, or self-authorization authority."
    )

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def validate_current_script(operation: str, expected_script: str, actual_script: str, evidence_path: str | Path) -> CurrentScriptGate:
    failures: list[str] = []
    evidence_script = ""
    path = Path(evidence_path)
    if not path.exists():
        failures.append("missing_evidence")
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        evidence_script = str(data.get("operator_script_name", ""))
        if data.get("operation") != operation:
            failures.append("operation_mismatch")
        if evidence_script != expected_script:
            failures.append("evidence_script_mismatch")
    if actual_script != expected_script:
        failures.append("actual_script_mismatch")
    ok = not failures
    return CurrentScriptGate(RHP_CURRENT_SCRIPT_GATE_SCHEMA, ok, operation, expected_script, actual_script, evidence_script, failures, "[OK]" if ok else "[BLOCKED]")

def render_gate(gate: CurrentScriptGate) -> str:
    lines = [
        f"RHPLOAD [088%] loop=CURRENT-SCRIPT-GATE operation={gate.operation} | status={'ok' if gate.ok else 'blocked'} {gate.glyph}",
        "`- current script gate",
        f"   +- expected: {gate.expected_script}",
        f"   +- actual: {gate.actual_script}",
        f"   +- evidence: {gate.evidence_script}",
        f"   `- verified: {str(gate.ok).lower()} {gate.glyph}",
    ]
    for failure in gate.failures:
        lines.append(f"      failure: {failure}")
    return "\n".join(lines)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="RHP current script gate")
    p.add_argument("--operation", required=True)
    p.add_argument("--expected-script", required=True)
    p.add_argument("--actual-script", required=True)
    p.add_argument("--evidence", required=True)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    gate = validate_current_script(args.operation, args.expected_script, args.actual_script, args.evidence)
    print(json.dumps(gate.as_dict(), indent=2, ensure_ascii=False) if args.json else render_gate(gate))
    return 0 if gate.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
