# RHP-014.1 dev-loop chart generator.
from __future__ import annotations
import argparse, json
from typing import Any

RHP_DEV_LOOP_CHART_SCHEMA = "RHP-DEV-LOOP-CHART-v0.1"

TOOLS = [
    ("AUTOHEAL-PREFLIGHT", "rhp/autoheal_preflight.py", "clean bounded failed-attempt residue before pull/rebase"),
    ("RESUME-PACKET", "rhp/resume_packet.py", "zero-context resume from evidence and transcript"),
    ("LOOP-REGISTRY", "rhp/loop_registry.py", "legal loops, mutation/commit permissions, attempt budgets"),
    ("CURRENT-SCRIPT-GATE", "rhp/current_script_gate.py", "block push if active script and evidence mismatch"),
    ("WARNING-COMPRESSOR", "rhp/warning_compressor.py", "compress noisy CRLF warning streams into one box"),
    ("GITHUB-PUSH-BOX", "rhp/push_controller.py", "commit/pull-rebase/push/seal visibility"),
    ("OPERATOR-INTERFACE", "rhp/operator_interface.py", "render stable human-readable boxes"),
]

SEQUENCE = ["AUTOHEAL-PREFLIGHT", "PULL-REBASE", "HUMAN-AUTHORIZATION", "OPERATION", "VALIDATION", "EVIDENCE", "SECRET-SCAN", "WARNING-COMPRESSOR", "CURRENT-SCRIPT-GATE", "GITHUB-PUSH-BOX", "RETURN-ROOT"]

def chart() -> dict[str, Any]:
    return {"schema": RHP_DEV_LOOP_CHART_SCHEMA, "sequence": SEQUENCE, "tools": [{"box": b, "tool": t, "purpose": p} for b, t, p in TOOLS]}

def markdown_table() -> str:
    rows = ["| Box | Tool | Purpose |", "|---|---|---|"]
    for b, t, p in TOOLS:
        rows.append(f"| {b} | `{t}` | {p} |")
    return "\n".join(rows)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render RHP dev-loop chart")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    print(json.dumps(chart(), indent=2, ensure_ascii=False) if args.json else markdown_table())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
