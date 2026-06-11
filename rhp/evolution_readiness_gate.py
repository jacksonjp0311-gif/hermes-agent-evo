from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

RHP_EVOLUTION_READINESS_GATE_SCHEMA = "RHP-EVOLUTION-READINESS-GATE-v0.1"

OPERATION_CLASSES = {
    "observe",
    "diagnostic",
    "known_wound_repair",
    "governance_kernel_update",
    "documentation_only",
    "feature_evolution",
    "residue_cleanup",
}

AUTHORITY_LOCKS = {
    "provider_call_executed": False,
    "model_call_executed": False,
    "tool_use_executed": False,
    "cms_runtime_execution": False,
    "cms_write": False,
    "memory_write": False,
    "memory_promotion": False,
    "api_write": False,
    "dependency_mutation_committed": False,
    "external_ingestion": False,
    "autonomous_authority": False,
    "self_authorization": False,
}


def _git_status_clean(root: Path) -> tuple[bool, list[str]]:
    proc = subprocess.run(["git", "status", "--short"], cwd=str(root), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        return False, ["git_status_failed"]
    paths = [line[3:].replace("\\\\", "/") for line in proc.stdout.splitlines() if len(line) >= 4]
    return not paths, paths


def allowed_classes_for_pointer(pointer: dict[str, Any], *, worktree_clean: bool = True) -> tuple[str, set[str], str, str]:
    observed = str(pointer.get("observed_ci_status", "unknown")).lower()
    active_wound = str(pointer.get("active_wound_class", "unknown"))
    integrated = pointer.get("integration_closed") is True
    state = str(pointer.get("state", ""))

    if not worktree_clean:
        return (
            "DIRTY_BLOCK",
            {"residue_cleanup"},
            "bounded_residue_cleanup_required",
            "Worktree is dirty; only residue cleanup is legal.",
        )

    if observed == "red" or active_wound not in {"no_active_wound", "", None}:
        if active_wound == "remote_ci_pending" and observed in {"pending", "unknown"}:
            return (
                "REMOTE_NOT_FINAL",
                {"observe", "diagnostic"},
                "wait_or_ingest_final_ci_status_before_green_claim",
                "Remote CI is not final; only observation or diagnostics are legal.",
            )
        return (
            "WOUND_OPEN",
            {"observe", "diagnostic", "known_wound_repair"},
            "create_wound_packet_or_repair_known_wound",
            "A wound is active; feature compounding is blocked until repair/reconciliation.",
        )

    if observed in {"pending", "unknown"} or not integrated:
        return (
            "REMOTE_NOT_FINAL",
            {"observe", "diagnostic"},
            "wait_or_ingest_final_ci_status_before_green_claim",
            "Unknown or pending is not pass.",
        )

    if observed == "green" and integrated and active_wound == "no_active_wound":
        return (
            "READY_INTEGRATED",
            {"observe", "diagnostic", "known_wound_repair", "governance_kernel_update", "documentation_only", "feature_evolution"},
            "continue_bounded_evolution_after_named_subject_green",
            "Latest named subject is green, integrated, and has no active wound.",
        )

    return (
        "UNKNOWN_BLOCK",
        {"observe", "diagnostic"},
        "ingest_commit_scoped_ci_status",
        f"Unrecognized readiness state: state={state!r} observed={observed!r} active_wound={active_wound!r}.",
    )


def evaluate(
    repo_root: str | Path = ".",
    *,
    candidate_operation_class: str,
    current_head_ci_status: str = "unknown",
    ci_source: str = "operator-provided",
    allow_dirty: bool = False,
) -> dict[str, Any]:
    root = Path(repo_root)
    if candidate_operation_class not in OPERATION_CLASSES:
        raise ValueError(f"candidate_operation_class must be one of {sorted(OPERATION_CLASSES)}")

    pointer_path = root / "docs/context-layer/latest-rhp.json"
    pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
    clean, dirty_paths = _git_status_clean(root)
    effective_clean = clean or allow_dirty
    readiness_state, allowed, next_operation, reason = allowed_classes_for_pointer(pointer, worktree_clean=effective_clean)
    allowed_bool = candidate_operation_class in allowed

    blocks: list[str] = []
    if not allowed_bool:
        blocks.append("candidate_operation_class_not_allowed_by_readiness_state")
    if not clean and not allow_dirty:
        blocks.append("worktree_not_clean")
    if current_head_ci_status in {"red"}:
        blocks.append("current_head_red_requires_wound_packet")
    if current_head_ci_status in {"pending", "unknown"}:
        # Informational only for a new operation; not a block against installing a governance gate.
        pass

    decision = "allowed" if allowed_bool and not blocks else "blocked"
    return {
        "schema": RHP_EVOLUTION_READINESS_GATE_SCHEMA,
        "decision": decision,
        "allowed": decision == "allowed",
        "readiness_state": readiness_state,
        "candidate_operation_class": candidate_operation_class,
        "allowed_operation_classes": sorted(allowed),
        "blocked_reasons": blocks,
        "reason": reason,
        "next_legal_operation": next_operation,
        "latest_operation": pointer.get("latest_operation"),
        "latest_evidence": pointer.get("latest_evidence"),
        "observed_ci_status": pointer.get("observed_ci_status"),
        "active_wound_class": pointer.get("active_wound_class"),
        "integration_closed": pointer.get("integration_closed"),
        "current_head_ci_status": current_head_ci_status,
        "ci_source": ci_source,
        "worktree_clean": clean,
        "dirty_paths": dirty_paths,
        "authority_locks": dict(AUTHORITY_LOCKS),
        "command": "python -m rhp.evolution_readiness_gate --repo-root . --candidate-operation-class <class> --current-head-ci-status <status>",
        "box": "RHPREADY",
        "non_claim_lock": "Evolution readiness gate classifies legal next operation classes only. It does not call GitHub, rerun CI, mutate files, execute repairs, or grant authority.",
    }


def render_rhpready_box(result: dict[str, Any]) -> str:
    mode = "ALLOW" if result.get("allowed") else "BLOCK"
    lines = [
        f"RHPREADY [{mode}] class={result.get('candidate_operation_class')} decision={result.get('decision')}",
        "`- evolution readiness gate",
        f"   +- latest: {result.get('latest_operation')}",
        f"   +- state: {result.get('readiness_state')}",
        f"   +- observed-ci-status: {result.get('observed_ci_status')}",
        f"   +- active-wound: {result.get('active_wound_class')}",
        f"   +- integration-closed: {str(result.get('integration_closed')).lower()}",
        f"   +- allowed-classes: {', '.join(result.get('allowed_operation_classes', []))}",
        f"   +- next: {result.get('next_legal_operation')}",
        f"   +- reason: {result.get('reason')}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Run RHP evolution readiness gate")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--candidate-operation-class", default="diagnostic", choices=sorted(OPERATION_CLASSES))
    parser.add_argument("--current-head-ci-status", default="unknown", choices=["unknown", "pending", "green", "red", "cancelled", "skipped"])
    parser.add_argument("--ci-source", default="operator-provided")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--json-only", action="store_true")
    parser.add_argument("--out", default="")
    parser.add_argument("--box-out", default="")
    args = parser.parse_args(argv)
    result = evaluate(
        args.repo_root,
        candidate_operation_class=args.candidate_operation_class,
        current_head_ci_status=args.current_head_ci_status,
        ci_source=args.ci_source,
        allow_dirty=args.allow_dirty,
    )
    text = json.dumps(result, indent=2, ensure_ascii=False)
    box = render_rhpready_box(result)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    if args.box_out:
        box_out = Path(args.box_out)
        box_out.parent.mkdir(parents=True, exist_ok=True)
        box_out.write_text(box + "\n", encoding="utf-8")
    if args.json_only:
        print(text)
    else:
        print(box)
        print(text)
    return 0 if result["allowed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
