from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA = "RHP-AUTOHEAL-PROPOSAL-EVALUATOR-v0.1"

def evaluate(packet: dict[str, Any]) -> dict[str, Any]:
    failures = packet.get("failures") or packet.get("issues") or []
    if isinstance(failures, str):
        failures = [failures]
    actions: list[dict[str, Any]] = []
    for failure in failures:
        item = str(failure)
        if item in {"root_readme_latest_evidence", "root_readme_current_status", "alignment_guard_not_green"}:
            proposal = "repair alignment guard to accept current latest-rhp pointer plus legacy RHP-013.5 boot kernel"
        elif item in {"boot_preflight_ok_false", "operator_startup_degraded"}:
            proposal = "run startup/alignment focused tests after pointer-aware alignment guard repair"
        else:
            proposal = "collect CI log context before proposing code mutation"
        actions.append({"failure": item, "proposal": proposal, "executes": False})
    return {"schema": SCHEMA, "ok": True, "dry_run_only": True, "autoheal_execution_enabled": False, "actions": actions, "non_claim_lock": "Autoheal proposal evaluator creates proposals only. It does not mutate files, execute repairs, rerun CI, or grant authority."}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate an RHP autoheal proposal packet")
    parser.add_argument("--input", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    packet: dict[str, Any] = {"failures": []}
    if args.input:
        packet = json.loads(Path(args.input).read_text(encoding="utf-8"))
    print(json.dumps(evaluate(packet), indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
