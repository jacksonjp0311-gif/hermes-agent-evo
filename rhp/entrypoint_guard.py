from __future__ import annotations
import argparse, json
from dataclasses import dataclass
from typing import Any

RHP_ENTRYPOINT_GUARD_SCHEMA = "RHP-ENTRYPOINT-GUARD-v0.1"

@dataclass(frozen=True)
class EntrypointGuard:
    schema: str
    ok: bool
    expected_script: str
    actual_script: str
    invocation_mode: str
    failure: str = ""
    non_claim_lock: str = "Entrypoint guard verifies invocation surface only. It grants no authority."
    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def validate(expected_script: str, actual_script: str) -> EntrypointGuard:
    if not actual_script:
        return EntrypointGuard(RHP_ENTRYPOINT_GUARD_SCHEMA, False, expected_script, actual_script, "pasted_or_unknown", "missing_script_path")
    if actual_script != expected_script:
        return EntrypointGuard(RHP_ENTRYPOINT_GUARD_SCHEMA, False, expected_script, actual_script, "file", "script_name_mismatch")
    return EntrypointGuard(RHP_ENTRYPOINT_GUARD_SCHEMA, True, expected_script, actual_script, "file", "")

def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--expected-script", required=True)
    p.add_argument("--actual-script", default="")
    args = p.parse_args(argv)
    gate = validate(args.expected_script, args.actual_script)
    print(json.dumps(gate.as_dict(), indent=2, ensure_ascii=False))
    return 0 if gate.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
