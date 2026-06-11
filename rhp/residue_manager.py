from __future__ import annotations
import argparse, json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RHP_RESIDUE_MANAGER_SCHEMA = "RHP-RESIDUE-MANAGER-v0.1"

SAFE_PREFIXES = [
    "docs/context-layer/ops/RHP-014-5",
]
SAFE_EXACT = {
    "tests/test_rhp_014_5_zero_context_rebuild.py",
    "tests/test_rhp_014_5_operator_dashboard.py",
    "tests/test_rhp_014_5_hermes_operator_context.py",
    "tests/test_rhp_014_5_v4_zero_context_rebuild.py",
    "tests/test_rhp_014_5_v4_operator_dashboard.py",
    "tests/test_rhp_014_5_v4_entrypoint_guard.py",
}

@dataclass(frozen=True)
class ResidueReport:
    schema: str
    ok: bool
    cleanable: list[str] = field(default_factory=list)
    blocked: list[str] = field(default_factory=list)
    classification: str = "unknown"
    non_claim_lock: str = "Residue manager only classifies bounded failed-run residue. It grants no authority and does not decide unknown user work is safe."

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def classify_paths(paths: list[str]) -> ResidueReport:
    cleanable: list[str] = []
    blocked: list[str] = []
    for raw in paths:
        path = raw.replace("\\", "/").strip()
        if not path:
            continue
        if path in SAFE_EXACT or any(path.startswith(prefix) for prefix in SAFE_PREFIXES):
            cleanable.append(path)
        else:
            blocked.append(path)
    classification = "bounded_failed_run_residue" if cleanable and not blocked else "blocked_unknown_residue" if blocked else "clean"
    return ResidueReport(RHP_RESIDUE_MANAGER_SCHEMA, not blocked, cleanable, blocked, classification)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Classify RHP residue paths")
    p.add_argument("paths", nargs="*")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    report = classify_paths(args.paths)
    print(json.dumps(report.as_dict(), indent=2, ensure_ascii=False))
    return 0 if report.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
