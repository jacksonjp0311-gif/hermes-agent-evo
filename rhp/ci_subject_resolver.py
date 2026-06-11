from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rhp.claim_ledger import make_claim, build_ledger

RHP_CI_SUBJECT_RESOLVER_SCHEMA = "RHP-CI-SUBJECT-RESOLVER-v0.1"
VALID_STATUSES = {"unknown", "pending", "green", "red", "cancelled", "skipped"}


def resolve(
    *,
    previous_commit: str,
    previous_ci_status: str,
    current_head: str,
    current_head_ci_status: str,
    source: str,
) -> dict[str, Any]:
    if previous_ci_status not in VALID_STATUSES:
        raise ValueError("invalid previous_ci_status")
    if current_head_ci_status not in VALID_STATUSES:
        raise ValueError("invalid current_head_ci_status")
    claims = [
        make_claim(
            claim="previous_commit_remote_ci_status",
            subject_type="git_commit",
            subject_id=previous_commit,
            status=previous_ci_status,
            source=source,
            applies_to_current_head=previous_commit == current_head,
            authority_granted=False,
            note="CI status ascribed to the observed previous/base commit.",
        ),
        make_claim(
            claim="current_head_remote_ci_status",
            subject_type="git_commit",
            subject_id=current_head,
            status=current_head_ci_status,
            source=source,
            applies_to_current_head=True,
            authority_granted=False,
            note="CI status ascribed to current HEAD at operation start.",
        ),
    ]
    if previous_ci_status == "green":
        claims.append(
            make_claim(
                claim="remote_ci_green",
                subject_type="git_commit",
                subject_id=previous_commit,
                status="green",
                source=source,
                applies_to_current_head=previous_commit == current_head,
                authority_granted=False,
                note="Green claim applies only to its subject commit.",
            )
        )
    ledger = build_ledger(claims)
    return {
        "schema": RHP_CI_SUBJECT_RESOLVER_SCHEMA,
        "previous_commit": previous_commit,
        "previous_ci_status": previous_ci_status,
        "current_head": current_head,
        "current_head_ci_status": current_head_ci_status,
        "current_head_green": current_head_ci_status == "green",
        "previous_green_applies_to_current_head": previous_commit == current_head and previous_ci_status == "green",
        "claims": claims,
        "ledger_ok": ledger["ok"],
        "conflicts": ledger["conflicts"],
        "non_claim_lock": "CI subject resolver does not query GitHub or rerun CI. It scopes provided CI observations to explicit commit subjects only.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Resolve CI claims by commit subject")
    parser.add_argument("--previous-commit", required=True)
    parser.add_argument("--previous-ci-status", required=True)
    parser.add_argument("--current-head", required=True)
    parser.add_argument("--current-head-ci-status", required=True)
    parser.add_argument("--source", default="operator-provided")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = resolve(
        previous_commit=args.previous_commit,
        previous_ci_status=args.previous_ci_status,
        current_head=args.current_head,
        current_head_ci_status=args.current_head_ci_status,
        source=args.source,
    )
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if data["ledger_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
