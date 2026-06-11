from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

RHP_CI_WOUND_HARVESTER_SCHEMA = "RHP-CI-WOUND-HARVESTER-v0.1"

PATTERNS: list[tuple[str, str]] = [
    ("autoheal_dry_run_api_compatibility", r"cannot import name 'RHP_AUTOHEAL_DRY_RUN_SCHEMA'|cannot import name 'dry_run_for_packet'"),
    ("alignment_guard_contract_drift", r"latest_rhp0135_has_boundary_shape|latest_rhp0135_passed|root_readme_latest_evidence|root_readme_current_status"),
    ("boot_preflight_ok_false", r"boot_preflight_ok is True|boot_preflight_ok"),
    ("operator_startup_degraded", r"OperatorStartupStatus\(ok=False|status\.ok is True"),
    ("module_path_execution_bug", r"ModuleNotFoundError: No module named 'rhp'"),
    ("collection_import_error", r"ERROR collecting|ImportError while importing test module"),
]


def harvest(text: str) -> dict[str, Any]:
    classifications: list[str] = []
    for classification, pattern in PATTERNS:
        if re.search(pattern, text):
            classifications.append(classification)
    failed_tests = sorted(set(re.findall(r"(tests/[A-Za-z0-9_./-]+\.py)", text)))
    missing_symbols = sorted(set(re.findall(r"cannot import name '([^']+)'", text)))
    return {
        "schema": RHP_CI_WOUND_HARVESTER_SCHEMA,
        "ok": True,
        "classifications": classifications,
        "primary_classification": classifications[0] if classifications else "unknown",
        "failed_tests": failed_tests,
        "missing_symbols": missing_symbols,
        "non_claim_lock": "CI wound harvester classifies pasted/exported CI text only. It does not call GitHub, rerun CI, mutate files, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Harvest RHP wound classes from pasted/exported CI logs")
    parser.add_argument("--input", required=True)
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    result = harvest(Path(args.input).read_text(encoding="utf-8", errors="replace"))
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
