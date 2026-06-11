from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA = "RHP-CI-LOG-INGESTION-v0.1"

def classify_log(text: str) -> dict[str, Any]:
    failures: list[str] = []
    if "boot_preflight_ok is True" in text or "boot_preflight_ok" in text:
        failures.append("boot_preflight_ok_false")
    if "root_readme_latest_evidence" in text:
        failures.append("root_readme_latest_evidence")
    if "root_readme_current_status" in text:
        failures.append("root_readme_current_status")
    if "OperatorStartupStatus(ok=False" in text or "status.ok is True" in text:
        failures.append("operator_startup_degraded")
    if "tests/test_rhp_alignment_guard.py" in text:
        failures.append("alignment_guard_not_green")
    return {"schema": SCHEMA, "ok": True, "failures": sorted(set(failures)), "summary": "CI log ingestion classified known RHP startup/alignment wound surfaces.", "non_claim_lock": "CI log ingestion reads pasted/exported logs only. It does not call GitHub, rerun CI, mutate files, or grant authority."}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Classify pasted/exported RHP CI logs")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = classify_log(Path(args.input).read_text(encoding="utf-8", errors="replace"))
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
