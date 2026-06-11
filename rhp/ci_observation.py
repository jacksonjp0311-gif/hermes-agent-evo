from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

RHP_CI_OBSERVATION_SCHEMA = "RHP-CI-OBSERVATION-v0.1"
VALID_STATUSES = {"unknown", "pending", "green", "red", "cancelled", "skipped"}


def observe(
    *,
    subject_commit: str,
    ci_status: str,
    source: str,
    observed_at_utc: str | None = None,
    prior_operation: str = "",
) -> dict[str, Any]:
    if not subject_commit:
        raise ValueError("subject_commit is required")
    if ci_status not in VALID_STATUSES:
        raise ValueError(f"ci_status must be one of {sorted(VALID_STATUSES)}")
    integration_closed = ci_status == "green"
    state = "RECONCILED" if integration_closed else ("REMOTE_RED" if ci_status == "red" else "REMOTE_PENDING")
    return {
        "schema": RHP_CI_OBSERVATION_SCHEMA,
        "claim": "current_operation_ci_observation",
        "subject_type": "git_commit",
        "subject_commit": subject_commit,
        "prior_operation": prior_operation,
        "ci_status": ci_status,
        "source": source,
        "observed_at_utc": observed_at_utc or dt.datetime.now(dt.timezone.utc).isoformat(),
        "integration_closed": integration_closed,
        "state": state,
        "authority_granted": False,
        "execution_enabled": False,
        "non_claim_lock": "CI observation scopes status to one commit only. It does not call GitHub, rerun CI, mutate workflows, execute repair, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Record a commit-scoped CI observation")
    parser.add_argument("--subject-commit", required=True)
    parser.add_argument("--ci-status", required=True, choices=sorted(VALID_STATUSES))
    parser.add_argument("--source", default="operator-provided")
    parser.add_argument("--prior-operation", default="")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = observe(
        subject_commit=args.subject_commit,
        ci_status=args.ci_status,
        source=args.source,
        prior_operation=args.prior_operation,
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
