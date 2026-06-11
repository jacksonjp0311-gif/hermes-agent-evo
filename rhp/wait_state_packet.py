from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

RHP_WAIT_STATE_PACKET_SCHEMA = "RHP-WAIT-STATE-PACKET-v0.1"


def build_packet(*, operation: str, observed_commit: str, remote_ci_status: str, next_operation: str) -> dict[str, Any]:
    if remote_ci_status not in {"unknown", "pending", "green", "red", "cancelled", "skipped"}:
        raise ValueError("invalid remote CI status")
    return {
        "schema": RHP_WAIT_STATE_PACKET_SCHEMA,
        "operation": operation,
        "observed_commit": observed_commit,
        "remote_ci_status": remote_ci_status,
        "wait_state": remote_ci_status in {"unknown", "pending"},
        "green_seal_ready": remote_ci_status == "green",
        "wound_packet_required": remote_ci_status == "red",
        "next_operation": next_operation,
        "non_claim_lock": "Wait-state packet records a provided CI status only. It does not call GitHub, rerun CI, mutate workflows, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Render an RHP wait-state packet")
    parser.add_argument("--operation", required=True)
    parser.add_argument("--observed-commit", required=True)
    parser.add_argument("--remote-ci-status", required=True)
    parser.add_argument("--next-operation", required=True)
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = build_packet(operation=args.operation, observed_commit=args.observed_commit, remote_ci_status=args.remote_ci_status, next_operation=args.next_operation)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
