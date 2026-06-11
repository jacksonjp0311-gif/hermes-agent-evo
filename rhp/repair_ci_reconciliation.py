from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

VALID_STATUSES = {"unknown", "pending", "green", "red", "cancelled", "skipped"}
RHP_REPAIR_CI_RECONCILIATION_SCHEMA = "RHP-REPAIR-CI-RECONCILIATION-v0.1"


def reconcile_repair_ci(
    *,
    subject_commit: str,
    observed_ci_status: str,
    ci_source: str,
    repaired_wound_class: str,
    prior_operation: str = "RHP-016.3",
    run_url: str = "",
    observed_at_utc: str | None = None,
) -> dict[str, Any]:
    if not subject_commit:
        raise ValueError("subject_commit is required")
    if observed_ci_status not in VALID_STATUSES:
        raise ValueError(f"observed_ci_status must be one of {sorted(VALID_STATUSES)}")
    if not repaired_wound_class:
        raise ValueError("repaired_wound_class is required")

    if observed_ci_status == "green":
        state = "REPAIR_RECONCILED_GREEN"
        integration_closed = True
        active_wound_class = "no_active_wound"
        next_operation = "RHP-016.5 git_status_short_path_parse_drift repair"
    elif observed_ci_status == "red":
        state = "REPAIR_STILL_RED"
        integration_closed = False
        active_wound_class = repaired_wound_class
        next_operation = "RHP-016.5 Re-wound packet for remaining browser supervisor failure"
    else:
        state = "REPAIR_CI_PENDING"
        integration_closed = False
        active_wound_class = "remote_ci_pending"
        next_operation = "wait_or_ingest_final_ci_status_before_green_claim"

    return {
        "schema": RHP_REPAIR_CI_RECONCILIATION_SCHEMA,
        "claim": "repair_commit_ci_observation",
        "subject_type": "git_commit",
        "subject_commit": subject_commit,
        "prior_operation": prior_operation,
        "observed_ci_status": observed_ci_status,
        "ci_source": ci_source,
        "run_url": run_url,
        "observed_at_utc": observed_at_utc or dt.datetime.now(dt.timezone.utc).isoformat(),
        "repaired_wound_class": repaired_wound_class,
        "active_wound_class": active_wound_class,
        "state": state,
        "integration_closed": integration_closed,
        "next_operation": next_operation,
        "authority_granted": False,
        "execution_enabled": False,
        "remote_ci_rerun_executed": False,
        "non_claim_lock": "Repair CI reconciliation scopes status to one subject commit only. It does not call GitHub, rerun CI, execute repair, mutate dependencies, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Observe and reconcile or re-wound a repair commit CI result")
    parser.add_argument("--subject-commit", required=True)
    parser.add_argument("--observed-ci-status", required=True, choices=sorted(VALID_STATUSES))
    parser.add_argument("--ci-source", default="operator-provided")
    parser.add_argument("--repaired-wound-class", required=True)
    parser.add_argument("--run-url", default="")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = reconcile_repair_ci(
        subject_commit=args.subject_commit,
        observed_ci_status=args.observed_ci_status,
        ci_source=args.ci_source,
        repaired_wound_class=args.repaired_wound_class,
        run_url=args.run_url,
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
