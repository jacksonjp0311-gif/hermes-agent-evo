from __future__ import annotations

import argparse
import json
from pathlib import Path
from rhp.proposal_packet import build_proposal, validate_proposal

RHP_BROWSER_SUPERVISOR_WEBSOCKETS_PROPOSAL_SCHEMA = "RHP-BROWSER-SUPERVISOR-WEBSOCKETS-PROPOSAL-v0.1"
WOUND_CLASS = "browser_supervisor_websockets_dependency_api_drift"

def build_browser_supervisor_websockets_proposal(*, subject_commit: str, run_url: str = "") -> dict:
    packet = build_proposal(
        wound_class=WOUND_CLASS,
        subject=f"commit:{subject_commit}",
        summary=(
            "Remote CI failure in tests/tools/test_browser_supervisor.py caused by websockets dependency/API drift: "
            "websockets.asyncio.client expects websockets.proxy / uri.Proxy but installed package surface does not provide them."
        ),
        allowed_paths=[
            "tools/browser_supervisor.py",
            "tests/tools/test_browser_supervisor.py",
            "pyproject.toml",
            "requirements*.txt",
            "uv.lock",
            "poetry.lock",
            "docs/context-layer/ops/RHP-016-2*",
        ],
        test_commands=[
            "python -m pytest tests/tools/test_browser_supervisor.py",
            "python -m pytest -q -o addopts= tests/test_rhp_016_2_ci_wound_packet.py tests/test_rhp_016_2_browser_supervisor_websockets_proposal.py",
        ],
        risk_level="medium",
        rollback="git restore scoped paths before commit; no post-seal mutation",
    )
    packet["schema"] = RHP_BROWSER_SUPERVISOR_WEBSOCKETS_PROPOSAL_SCHEMA
    packet["run_url"] = run_url
    packet["repair_options"] = [
        "Pin or align websockets dependency to a version exposing the expected proxy API.",
        "Patch browser_supervisor import/use site to support the installed websockets API.",
        "Add a small compatibility shim around websockets proxy imports.",
    ]
    packet["execution_enabled"] = False
    packet["authority_granted"] = False
    packet["validation"] = validate_proposal(packet)
    packet["non_claim_lock"] = "This is a proposal only. It does not modify dependencies, patch browser supervisor code, rerun CI, execute repair, or grant authority."
    return packet

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build browser supervisor websockets drift proposal")
    parser.add_argument("--subject-commit", required=True)
    parser.add_argument("--run-url", default="")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = build_browser_supervisor_websockets_proposal(subject_commit=args.subject_commit, run_url=args.run_url)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if data["validation"]["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
