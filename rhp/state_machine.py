from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

RHP_STATE_MACHINE_SCHEMA = "RHP-STATE-MACHINE-v0.1"

STATES = [
    "NEW",
    "PREFLIGHT",
    "AUTHORIZED",
    "MUTATED",
    "VALIDATED",
    "SEALED_LOCAL",
    "PUSHED",
    "REMOTE_PENDING",
    "REMOTE_GREEN",
    "REMOTE_RED",
    "RECONCILED",
]

TERMINAL_CI = {"green", "red", "cancelled", "skipped"}
VALID_CI = {"unknown", "pending", "green", "red", "cancelled", "skipped"}


def derive_state(*, local_validation_ok: bool, pushed: bool, current_head_ci_status: str, integration_closed: bool = False) -> dict[str, Any]:
    if current_head_ci_status not in VALID_CI:
        raise ValueError(f"current_head_ci_status must be one of {sorted(VALID_CI)}")

    if integration_closed:
        state = "RECONCILED"
    elif current_head_ci_status == "green":
        state = "REMOTE_GREEN"
    elif current_head_ci_status == "red":
        state = "REMOTE_RED"
    elif pushed:
        state = "REMOTE_PENDING"
    elif local_validation_ok:
        state = "SEALED_LOCAL"
    else:
        state = "PREFLIGHT"

    if state == "REMOTE_GREEN":
        next_legal_operation = "record_green_reconciliation_or_continue_bounded_evolution"
    elif state == "REMOTE_RED":
        next_legal_operation = "create_ci_wound_packet_before_repair"
    elif state == "REMOTE_PENDING":
        next_legal_operation = "wait_or_ingest_final_ci_status"
    elif state == "SEALED_LOCAL":
        next_legal_operation = "push_or_verify_remote_integration"
    elif state == "RECONCILED":
        next_legal_operation = "continue_next_bounded_evolution"
    else:
        next_legal_operation = "complete_preflight_authorization_validation_seal"

    return {
        "schema": RHP_STATE_MACHINE_SCHEMA,
        "state": state,
        "states": STATES,
        "local_validation_ok": local_validation_ok,
        "pushed": pushed,
        "current_head_ci_status": current_head_ci_status,
        "integration_closed": integration_closed,
        "next_legal_operation": next_legal_operation,
        "mutation_allowed": False,
        "mutation_authority_required": "human_all_one_authorization",
        "non_claim_lock": "State machine classifies local evidence and provided CI status only. It does not call GitHub, rerun CI, mutate workflows, execute repairs, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Classify an RHP operation state")
    parser.add_argument("--local-validation-ok", action="store_true")
    parser.add_argument("--pushed", action="store_true")
    parser.add_argument("--current-head-ci-status", required=True, choices=sorted(VALID_CI))
    parser.add_argument("--integration-closed", action="store_true")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = derive_state(
        local_validation_ok=args.local_validation_ok,
        pushed=args.pushed,
        current_head_ci_status=args.current_head_ci_status,
        integration_closed=args.integration_closed,
    )
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
