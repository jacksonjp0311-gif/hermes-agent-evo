
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

RHP_GREEN_SEAL_RECONCILER_SCHEMA = "RHP-GREEN-SEAL-RECONCILER-v0.1"

def reconcile(*, local_validation_ok: bool, ci_status: str, previous_sealed_commit: str, operation_base_commit: str) -> dict[str, Any]:
    integration_closed = local_validation_ok and ci_status == "green"
    if integration_closed:
        next_action = "green seal can be recorded for the observed commit"
    elif ci_status == "red":
        next_action = "harvest remote CI logs and create a wound packet"
    elif ci_status in {"pending", "unknown"}:
        next_action = "wait for CI or ingest a final status before green closure"
    else:
        next_action = "record non-green terminal CI state and decide next bounded move"
    return {
        "schema": RHP_GREEN_SEAL_RECONCILER_SCHEMA,
        "local_validation_ok": local_validation_ok,
        "ci_status": ci_status,
        "previous_sealed_commit": previous_sealed_commit,
        "operation_base_commit": operation_base_commit,
        "integration_closed": integration_closed,
        "next_action": next_action,
        "non_claim_lock": "Green-seal reconciliation combines provided status and local evidence only. It does not call GitHub, rerun CI, mutate workflows, or grant authority.",
    }

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Reconcile local validation with remote CI status")
    parser.add_argument("--local-validation-ok", action="store_true")
    parser.add_argument("--ci-status", required=True)
    parser.add_argument("--previous-sealed-commit", required=True)
    parser.add_argument("--operation-base-commit", required=True)
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = reconcile(local_validation_ok=args.local_validation_ok, ci_status=args.ci_status, previous_sealed_commit=args.previous_sealed_commit, operation_base_commit=args.operation_base_commit)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if data["local_validation_ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
