from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rhp.proposal_packet import build_proposal, validate_proposal
from rhp.wound_taxonomy import WOUND_CLASSES

RHP_AUTOHEAL_PROPOSAL_PLANNER_SCHEMA = "RHP-AUTOHEAL-PROPOSAL-PLANNER-v0.1"

DEFAULT_TESTS = {
    "remote_ci_pending": ["python -m pytest -q -o addopts= tests/test_rhp_015_9_autoheal_proposal_planner.py tests/test_rhp_015_9_wound_queue.py"],
    "remote_ci_red": ["python -m pytest -q -o addopts= tests/test_rhp_015_9_autoheal_proposal_planner.py tests/test_rhp_015_9_wound_queue.py"],
    "evidence_api_break": ["python -m pytest -q -o addopts= tests/test_rhp_015_6_evidence_api_compatibility_gate.py"],
    "post_seal_residue_leak": ["git status --short", "python -m pytest -q -o addopts= tests/test_rhp_015_9_wound_queue.py"],
    "no_active_wound": ["python -m pytest -q -o addopts= tests/test_rhp_015_9_autoheal_proposal_planner.py"],
}

DEFAULT_ALLOWED_PATHS = {
    "remote_ci_pending": ["docs/context-layer/ops/RHP-015-9*"],
    "remote_ci_red": ["docs/context-layer/ops/RHP-015-9*", "docs/context-layer/wounds/*"],
    "evidence_api_break": ["rhp/evidence_api_compatibility_gate.py", "tests/test_rhp_015_6_evidence_api_compatibility_gate.py", "docs/context-layer/ops/RHP-015-9*"],
    "post_seal_residue_leak": ["docs/context-layer/ops/RHP-015-9*", "rhp/compact_output.py"],
    "no_active_wound": ["docs/context-layer/ops/RHP-015-9*"],
}


def select_wound_for_ci(current_head_ci_status: str) -> str:
    if current_head_ci_status == "red":
        return "remote_ci_red"
    if current_head_ci_status in {"pending", "unknown"}:
        return "remote_ci_pending"
    return "no_active_wound"


def plan(
    *,
    wound_class: str,
    subject: str,
    current_head_ci_status: str = "pending",
    source: str = "operator-provided",
) -> dict[str, Any]:
    if wound_class not in WOUND_CLASSES:
        raise ValueError(f"unknown wound_class: {wound_class}")
    summary = f"Autoheal proposal planner selected {wound_class} for {subject}; execution remains disabled."
    allowed_paths = DEFAULT_ALLOWED_PATHS.get(wound_class, ["docs/context-layer/ops/RHP-015-9*"])
    test_commands = DEFAULT_TESTS.get(wound_class, ["python -m pytest -q"])
    risk_level = "high" if wound_class in {"remote_ci_red", "evidence_api_break", "unknown_residue", "secret_scan_trigger"} else "low"
    packet = build_proposal(
        wound_class=wound_class,
        subject=subject,
        summary=summary,
        allowed_paths=allowed_paths,
        test_commands=test_commands,
        risk_level=risk_level,
    )
    validation = validate_proposal(packet)
    return {
        "schema": RHP_AUTOHEAL_PROPOSAL_PLANNER_SCHEMA,
        "wound_class": wound_class,
        "subject": subject,
        "current_head_ci_status": current_head_ci_status,
        "source": source,
        "proposal": packet,
        "proposal_validation": validation,
        "execution_enabled": False,
        "authority_granted": False,
        "planner_mode": "dry-run-proposal-only",
        "next_action": packet["wound"]["default_next"],
        "non_claim_lock": "Autoheal proposal planner creates proposal packets only. It does not execute repair, rerun CI, mutate workflows, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build a non-executing autoheal proposal plan")
    parser.add_argument("--wound-class", default="")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--current-head-ci-status", default="pending")
    parser.add_argument("--source", default="operator-provided")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    wound_class = args.wound_class or select_wound_for_ci(args.current_head_ci_status)
    data = plan(
        wound_class=wound_class,
        subject=args.subject,
        current_head_ci_status=args.current_head_ci_status,
        source=args.source,
    )
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if data["proposal_validation"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
