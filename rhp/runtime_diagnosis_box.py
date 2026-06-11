from __future__ import annotations
import argparse
import json
from typing import Any

SCHEMA = "RHP-RUNTIME-DIAGNOSIS-BOX-v0.1"

def classify(text: str) -> str:
    low = text.lower()
    if "expression after '&'" in low or "$args[0]" in low:
        return "powershell_command_invocation_collision"
    if "current script gate" in low or "operator_script_name" in low:
        return "current_script_gate_failure"
    if "remote_ci_red" in low or ("ci_status" in low and "red" in low):
        return "remote_ci_wound"
    if "secret" in low and "trigger" in low:
        return "secret_scan_failure"
    if "dirty" in low or "residue" in low:
        return "residue_boundary_failure"
    return "unknown_runtime_failure"

def diagnosis(stage: str, text: str, raw_path: str = "") -> dict[str, Any]:
    return {"schema": SCHEMA, "stage": stage, "class": classify(text), "raw": raw_path, "summary": text[:240], "next": "inspect raw artifact, classify failure, repair bounded surface, rerun", "non_claim_lock": "Runtime diagnosis boxes classify failures only. They do not repair, rerun CI, or grant authority."}

def render_box(data: dict[str, Any]) -> str:
    return "\n".join([f"RHPDIAG loop=RUNTIME-DIAGNOSIS | stage={data['stage']} | class={data['class']} [DIAG]", "`- runtime diagnosis box", f"   +- summary: {data['summary']}", f"   +- raw: {data['raw']}", "   +- expand: open raw artifact for complete details", f"   `- next: {data['next']}"])

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Classify and render an RHP runtime diagnosis box")
    p.add_argument("--stage", required=True)
    p.add_argument("--text", default="")
    p.add_argument("--raw", default="")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    data = diagnosis(a.stage, a.text, a.raw)
    print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else render_box(data))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
