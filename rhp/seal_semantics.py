
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

RHP_SEAL_SEMANTICS_SCHEMA = "RHP-SEAL-SEMANTICS-v0.1"

def explain() -> dict[str, Any]:
    return {
        "schema": RHP_SEAL_SEMANTICS_SCHEMA,
        "fields": {
            "operation_base_commit": "HEAD before the current All-One mutation begins.",
            "previous_sealed_commit": "Already-published commit that sealed the previous operation; knowable at the start of the next operation.",
            "current_operation_commit": "Commit produced by the current operation; cannot be embedded into files inside that same commit without a self-referential hash paradox.",
            "current_operation_commit_observed_by": "A later operation or external post-push observation can record the commit that sealed this operation.",
            "remote_ci_status": "Remote integration status for a specific observed commit: unknown, pending, green, red, cancelled, or skipped.",
        },
        "law": "A sealed RHP operation must distinguish local validation, operation base commit, previous sealed commit, current sealed commit observation, and remote CI result.",
        "non_claim_lock": "Seal semantics are descriptive only. They do not mutate files, compute remote CI, or grant authority.",
    }

def build_record(*, operation: str, operation_base_commit: str, previous_sealed_commit: str, remote_ci_status: str, remote_ci_source: str) -> dict[str, Any]:
    data = explain()
    data.update({
        "operation": operation,
        "operation_base_commit": operation_base_commit,
        "previous_sealed_commit": previous_sealed_commit,
        "current_operation_commit": "unobservable-from-inside-same-commit",
        "current_operation_commit_observed_by": "next-operation-or-external-post-push-observer",
        "remote_ci_status": remote_ci_status,
        "remote_ci_source": remote_ci_source,
    })
    return data

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Render RHP seal semantics")
    parser.add_argument("--operation", default="")
    parser.add_argument("--operation-base-commit", default="")
    parser.add_argument("--previous-sealed-commit", default="")
    parser.add_argument("--remote-ci-status", default="unknown")
    parser.add_argument("--remote-ci-source", default="operator-provided")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = build_record(operation=args.operation, operation_base_commit=args.operation_base_commit, previous_sealed_commit=args.previous_sealed_commit, remote_ci_status=args.remote_ci_status, remote_ci_source=args.remote_ci_source)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
