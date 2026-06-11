from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

RHP_GREEN_RECONCILIATION_SCHEMA = "RHP-GREEN-RECONCILIATION-v0.1"
VALID_STATUSES = {"unknown", "pending", "green", "red", "cancelled", "skipped"}


def reconcile(
    *,
    subject_commit: str,
    remote_ci_status: str,
    source: str,
    observed_at_utc: str | None = None,
    note: str = "",
) -> dict[str, Any]:
    if remote_ci_status not in VALID_STATUSES:
        raise ValueError(f"remote_ci_status must be one of {sorted(VALID_STATUSES)}")
    integration_closed = remote_ci_status == "green"
    if not subject_commit:
        raise ValueError("subject_commit is required")
    return {
        "schema": RHP_GREEN_RECONCILIATION_SCHEMA,
        "claim": "remote_ci_green_reconciliation" if integration_closed else "remote_ci_non_green_observation",
        "subject_type": "git_commit",
        "subject_commit": subject_commit,
        "remote_ci_status": remote_ci_status,
        "source": source,
        "observed_at_utc": observed_at_utc or dt.datetime.now(dt.timezone.utc).isoformat(),
        "integration_closed": integration_closed,
        "state": "RECONCILED" if integration_closed else ("REMOTE_RED" if remote_ci_status == "red" else "REMOTE_PENDING"),
        "authority_granted": False,
        "execution_enabled": False,
        "note": note,
        "non_claim_lock": "Green reconciliation scopes CI status to one subject commit only. It does not call GitHub, rerun CI, mutate workflows, execute repair, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Create an RHP green reconciliation packet scoped to a commit")
    parser.add_argument("--subject-commit", required=True)
    parser.add_argument("--remote-ci-status", required=True, choices=sorted(VALID_STATUSES))
    parser.add_argument("--source", default="operator-provided")
    parser.add_argument("--note", default="")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = reconcile(
        subject_commit=args.subject_commit,
        remote_ci_status=args.remote_ci_status,
        source=args.source,
        note=args.note,
    )
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if data["integration_closed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
