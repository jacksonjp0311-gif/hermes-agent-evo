from __future__ import annotations

import argparse
import json
from typing import Any

RHP_LOOP_GEOMETRY_SCHEMA = "RHP-LOOP-GEOMETRY-v0.1"

GEOMETRY = {
    "origin": "latest sealed evidence",
    "axes": ["evidence", "transcript", "wound", "dry_run", "residue", "authority", "tools", "geometry"],
    "boundary": "human authorization",
    "motion": "next legal delta only after gates pass",
    "adaptation_rule": "failure classes become bounded tools or dashboard surfaces before any autonomy is added",
}

def geometry() -> dict[str, Any]:
    return {
        "schema": RHP_LOOP_GEOMETRY_SCHEMA,
        **GEOMETRY,
        "non_claim_lock": "Loop geometry is an orientation model only. It does not assert cognition, autonomy, production readiness, or external authority.",
    }

def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    data = geometry()
    if args.json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        print("| Field | Value |")
        print("|---|---|")
        for key, value in data.items():
            print(f"| {key} | `{value}` |")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
