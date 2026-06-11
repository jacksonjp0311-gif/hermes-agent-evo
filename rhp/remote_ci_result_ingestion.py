
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

RHP_REMOTE_CI_RESULT_INGESTION_SCHEMA = "RHP-REMOTE-CI-RESULT-INGESTION-v0.1"
VALID_STATUSES = {"unknown", "pending", "green", "red", "cancelled", "skipped"}

def ingest(status: str, *, commit: str = "", source: str = "operator-provided", note: str = "") -> dict[str, Any]:
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of {sorted(VALID_STATUSES)}")
    return {
        "schema": RHP_REMOTE_CI_RESULT_INGESTION_SCHEMA,
        "status": status,
        "commit": commit,
        "source": source,
        "note": note,
        "green": status == "green",
        "closed": status == "green",
        "requires_wound_packet": status == "red",
        "pending": status in {"unknown", "pending"},
        "non_claim_lock": "CI result ingestion records a provided CI status only. It does not call GitHub, rerun CI, mutate workflows, or grant authority.",
    }

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Ingest an operator/connector-provided remote CI status")
    parser.add_argument("--status", required=True, choices=sorted(VALID_STATUSES))
    parser.add_argument("--commit", default="")
    parser.add_argument("--source", default="operator-provided")
    parser.add_argument("--note", default="")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = ingest(args.status, commit=args.commit, source=args.source, note=args.note)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
