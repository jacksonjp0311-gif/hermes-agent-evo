from __future__ import annotations

import argparse
import json
from pathlib import Path

from rhp.rhpload_doctor import doctor

RHP_DOCTOR_CLI_SCHEMA = "RHP-DOCTOR-CLI-v0.2"


def run_cli(
    repo_root: str = ".",
    current_head_ci_status: str = "pending",
    ci_source: str = "operator-provided",
    out: str = "",
    allow_operation_dirty: bool = False,
) -> dict:
    data = doctor(
        repo_root,
        current_head_ci_status=current_head_ci_status,
        ci_source=ci_source,
        allow_operation_dirty=allow_operation_dirty,
    )
    wrapped = {
        "schema": RHP_DOCTOR_CLI_SCHEMA,
        "doctor": data,
        "allow_operation_dirty": allow_operation_dirty,
        "human_summary": {
            "latest_operation": data.get("latest_operation"),
            "head": data.get("head"),
            "worktree_clean": data.get("worktree_clean"),
            "dirty_paths": data.get("dirty_paths", []),
            "allow_operation_dirty": data.get("allow_operation_dirty"),
            "evidence_api_ok": data.get("evidence_api_ok"),
            "replay_ok": data.get("replay_ok"),
            "current_head_ci_status": data.get("current_head_ci_status"),
            "state": data.get("state"),
            "next_legal_operation": data.get("next_legal_operation"),
            "can_mutate": data.get("can_mutate"),
            "blocked_reasons": data.get("blocked_reasons", []),
        },
        "non_claim_lock": "Doctor CLI wraps read-only doctor output. It does not call GitHub, rerun CI, mutate files, execute repair, or grant authority.",
    }
    if out:
        path = Path(out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(wrapped, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return wrapped


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run the read-only RHP doctor cockpit")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--current-head-ci-status", default="pending")
    parser.add_argument("--ci-source", default="operator-provided")
    parser.add_argument("--allow-operation-dirty", action="store_true")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = run_cli(
        args.repo_root,
        args.current_head_ci_status,
        args.ci_source,
        args.out,
        allow_operation_dirty=args.allow_operation_dirty,
    )
    print(json.dumps(data, indent=2, ensure_ascii=False))
    doctor_data = data["doctor"]
    ok_dirty = doctor_data.get("worktree_clean") or data.get("allow_operation_dirty")
    return 0 if doctor_data.get("evidence_api_ok") and doctor_data.get("replay_ok") and ok_dirty else 1


if __name__ == "__main__":
    raise SystemExit(main())
