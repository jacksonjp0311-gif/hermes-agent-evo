from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

RHP_CLAIM_LEDGER_SCHEMA = "RHP-CLAIM-LEDGER-v0.1"

REQUIRED_CLAIM_FIELDS = [
    "claim",
    "subject_type",
    "subject_id",
    "status",
    "source",
    "observed_at_utc",
    "applies_to_current_head",
    "authority_granted",
]


def make_claim(
    *,
    claim: str,
    subject_type: str,
    subject_id: str,
    status: str,
    source: str,
    applies_to_current_head: bool,
    authority_granted: bool = False,
    observed_at_utc: str | None = None,
    note: str = "",
) -> dict[str, Any]:
    return {
        "claim": claim,
        "subject_type": subject_type,
        "subject_id": subject_id,
        "status": status,
        "source": source,
        "observed_at_utc": observed_at_utc or dt.datetime.now(dt.timezone.utc).isoformat(),
        "applies_to_current_head": bool(applies_to_current_head),
        "authority_granted": bool(authority_granted),
        "note": note,
    }


def validate_claim(data: dict[str, Any]) -> dict[str, Any]:
    missing = [key for key in REQUIRED_CLAIM_FIELDS if key not in data]
    authority_ok = data.get("authority_granted") is False
    subject_ok = bool(data.get("subject_id"))
    return {
        "ok": not missing and authority_ok and subject_ok,
        "missing": missing,
        "authority_ok": authority_ok,
        "subject_ok": subject_ok,
    }


def build_ledger(claims: list[dict[str, Any]]) -> dict[str, Any]:
    validations = [validate_claim(claim) for claim in claims]
    conflicts = detect_conflicts(claims)
    return {
        "schema": RHP_CLAIM_LEDGER_SCHEMA,
        "claims": claims,
        "validations": validations,
        "ok": all(item["ok"] for item in validations) and not conflicts,
        "conflicts": conflicts,
        "claim_precision": sum(1 for claim in claims if claim.get("subject_id")) / max(1, len(claims)),
        "non_claim_lock": "Claim ledger records provenance only. It grants no action authority and does not call remote APIs, rerun CI, mutate workflows, or execute repairs.",
    }


def detect_conflicts(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    current_ci_green = [
        c for c in claims
        if c.get("claim") == "remote_ci_green"
        and c.get("applies_to_current_head") is True
        and c.get("status") == "green"
    ]
    current_ci_pending = [
        c for c in claims
        if c.get("claim") == "current_head_remote_ci_status"
        and c.get("applies_to_current_head") is True
        and c.get("status") in {"pending", "unknown"}
    ]
    if current_ci_green and current_ci_pending:
        conflicts.append({
            "class": "current_head_ci_status_conflict",
            "green_claims": len(current_ci_green),
            "pending_claims": len(current_ci_pending),
        })
    return conflicts


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate or render an RHP claim ledger")
    parser.add_argument("--claims", default="", help="JSON file containing a list of claims")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    if args.claims:
        claims = json.loads(Path(args.claims).read_text(encoding="utf-8"))
    else:
        claims = []
    data = build_ledger(claims)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
