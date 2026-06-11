from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from rhp.evidence_api_compatibility_gate import gate as evidence_api_gate
from rhp.rhpload_replay import replay
from rhp.state_machine import derive_state

RHPLOAD_DOCTOR_SCHEMA = "RHPLOAD-DOCTOR-v0.2"


def _git(root: Path, *args: str) -> tuple[str, int]:
    proc = subprocess.run(["git", *args], cwd=str(root), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    return proc.stdout.strip(), proc.returncode


def doctor(repo_root: str | Path = ".", current_head_ci_status: str = "pending", ci_source: str = "operator-provided", allow_operation_dirty: bool = False) -> dict[str, Any]:
    root = Path(repo_root)
    pointer_path = root / "docs/context-layer/latest-rhp.json"
    pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
    evidence_path = root / pointer["latest_evidence"]
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))

    head, head_code = _git(root, "rev-parse", "HEAD")
    short_head, _ = _git(root, "rev-parse", "--short", "HEAD")
    status, status_code = _git(root, "status", "--short")
    dirty_paths = [line[3:].replace("\\", "/") for line in status.splitlines() if len(line) >= 4]
    worktree_clean = status_code == 0 and status == ""

    api = evidence_api_gate(repo_root)
    rep = replay(repo_root)
    local_validation_ok = evidence.get("validation_passed") is True and evidence.get("focused_tests_passed") is True
    pushed = head_code == 0
    integration_closed = bool(pointer.get("current_head_integration_closed")) and current_head_ci_status == "green"
    state = derive_state(
        local_validation_ok=local_validation_ok,
        pushed=pushed,
        current_head_ci_status=current_head_ci_status,
        integration_closed=integration_closed,
    )

    blocked_reasons: list[str] = []
    if not worktree_clean and not allow_operation_dirty:
        blocked_reasons.append("worktree_not_clean")
    if not worktree_clean and allow_operation_dirty:
        blocked_reasons.append("operation_bootstrap_dirty_allowed")
    if not api["ok"]:
        blocked_reasons.append("evidence_api_incompatible")
    if not rep["ok"]:
        blocked_reasons.append("replay_incomplete")
    if current_head_ci_status in {"unknown", "pending"}:
        blocked_reasons.append("remote_ci_not_final")
    if current_head_ci_status == "red":
        blocked_reasons.append("remote_ci_red_requires_wound_packet")
    blocked_reasons.append("human_all_one_authorization_required_for_mutation")

    next_legal_operation = state["next_legal_operation"]
    if current_head_ci_status in {"unknown", "pending"}:
        next_legal_operation = "wait_or_ingest_final_ci_status_before_green_claim"
    if current_head_ci_status == "red":
        next_legal_operation = "create_ci_wound_packet_before_repair"
    if current_head_ci_status == "green":
        next_legal_operation = "record_current_head_green_reconciliation_or_continue_bounded_evolution"

    return {
        "schema": RHPLOAD_DOCTOR_SCHEMA,
        "latest_operation": pointer.get("latest_operation"),
        "latest_evidence": pointer.get("latest_evidence"),
        "head": head,
        "short_head": short_head,
        "worktree_clean": worktree_clean,
        "dirty_paths": dirty_paths,
        "allow_operation_dirty": allow_operation_dirty,
        "evidence_api_ok": api["ok"],
        "replay_ok": rep["ok"],
        "local_validation_ok": local_validation_ok,
        "current_head_ci_status": current_head_ci_status,
        "ci_source": ci_source,
        "state": state["state"],
        "next_legal_operation": next_legal_operation,
        "can_mutate": False,
        "blocked_reasons": blocked_reasons,
        "authority_required": "human_authorized_all_one_script",
        "api_summary": {
            "missing_pointer_required": api.get("missing_pointer_required", []),
            "missing_evidence_required": api.get("missing_evidence_required", []),
            "authority_not_false": api.get("authority_not_false", []),
            "deprecated_present": api.get("deprecated_present", []),
        },
        "replay_summary": {
            "replay_completeness": rep.get("replay_completeness"),
            "required": rep.get("required"),
        },
        "non_claim_lock": "Doctor is read/classify/propose-only. It does not call GitHub, rerun CI, mutate files, execute repairs, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run RHP doctor cockpit")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--current-head-ci-status", default="pending")
    parser.add_argument("--ci-source", default="operator-provided")
    parser.add_argument("--allow-operation-dirty", action="store_true")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = doctor(args.repo_root, args.current_head_ci_status, args.ci_source, allow_operation_dirty=args.allow_operation_dirty)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    doctor_ok = data["evidence_api_ok"] and data["replay_ok"] and (data["worktree_clean"] or data["allow_operation_dirty"])
    return 0 if doctor_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
