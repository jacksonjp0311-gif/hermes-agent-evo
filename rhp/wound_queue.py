from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

from rhp.autoheal_proposal_planner import plan, select_wound_for_ci
from rhp.wound_taxonomy import WOUND_CLASSES

RHP_WOUND_QUEUE_SCHEMA = "RHP-WOUND-QUEUE-v0.1"


def build_queue(
    *,
    current_head: str,
    current_head_ci_status: str,
    source: str = "operator-provided",
    include_no_active: bool = True,
) -> dict[str, Any]:
    wound_class = select_wound_for_ci(current_head_ci_status)
    items: list[dict[str, Any]] = []
    if wound_class != "no_active_wound" or include_no_active:
        proposal = plan(
            wound_class=wound_class,
            subject=f"commit:{current_head}",
            current_head_ci_status=current_head_ci_status,
            source=source,
        )
        items.append(
            {
                "id": f"{wound_class}:{current_head[:12]}",
                "wound_class": wound_class,
                "subject_type": "git_commit",
                "subject_id": current_head,
                "status": "open" if wound_class != "no_active_wound" else "closed",
                "severity": WOUND_CLASSES[wound_class]["severity"],
                "source": source,
                "observed_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
                "proposal_path_hint": "docs/context-layer/ops/RHP-015-9-autoheal-proposal-planner-wound-queue/autoheal-proposal-plan.json",
                "proposal": proposal,
                "execution_enabled": False,
                "authority_granted": False,
            }
        )
    open_count = sum(1 for item in items if item["status"] == "open")
    return {
        "schema": RHP_WOUND_QUEUE_SCHEMA,
        "current_head": current_head,
        "current_head_ci_status": current_head_ci_status,
        "source": source,
        "items": items,
        "open_count": open_count,
        "has_active_wound": open_count > 0,
        "execution_enabled": False,
        "authority_granted": False,
        "non_claim_lock": "Wound queue surfaces proposal-carrying evidence only. It does not execute repair, rerun CI, mutate workflows, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build a doctor-surfaced RHP wound queue")
    parser.add_argument("--current-head", required=True)
    parser.add_argument("--current-head-ci-status", default="pending")
    parser.add_argument("--source", default="operator-provided")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = build_queue(current_head=args.current_head, current_head_ci_status=args.current_head_ci_status, source=args.source)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
