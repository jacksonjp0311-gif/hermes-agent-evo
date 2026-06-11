from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from rhp.wound_taxonomy import WOUND_CLASSES

RHP_PROPOSAL_PACKET_SCHEMA = "RHP-PROPOSAL-PACKET-v0.1"


def build_proposal(
    *,
    wound_class: str,
    subject: str,
    summary: str,
    allowed_paths: list[str],
    test_commands: list[str],
    risk_level: str = "medium",
    rollback: str = "git restore scoped paths before commit; no post-seal mutation",
    execution_enabled: bool = False,
) -> dict[str, Any]:
    if wound_class not in WOUND_CLASSES:
        raise ValueError(f"unknown wound_class: {wound_class}")
    return {
        "schema": RHP_PROPOSAL_PACKET_SCHEMA,
        "wound_class": wound_class,
        "wound": WOUND_CLASSES[wound_class],
        "subject": subject,
        "summary": summary,
        "allowed_paths": allowed_paths,
        "blocked_paths": ["* unless explicitly listed in allowed_paths"],
        "test_commands": test_commands,
        "risk_level": risk_level,
        "rollback": rollback,
        "execution_enabled": bool(execution_enabled),
        "authority_required": "human_authorized_all_one_script",
        "authority_granted": False,
        "non_claim_lock": "Proposal packets carry repair intent only. They do not execute repair, rerun CI, mutate workflows, or grant authority.",
    }


def validate_proposal(packet: dict[str, Any]) -> dict[str, Any]:
    required = ["schema", "wound_class", "subject", "allowed_paths", "test_commands", "execution_enabled", "authority_granted"]
    missing = [key for key in required if key not in packet]
    wound_ok = packet.get("wound_class") in WOUND_CLASSES
    authority_ok = packet.get("authority_granted") is False and packet.get("execution_enabled") is False
    paths_ok = isinstance(packet.get("allowed_paths"), list)
    tests_ok = isinstance(packet.get("test_commands"), list)
    return {
        "ok": not missing and wound_ok and authority_ok and paths_ok and tests_ok,
        "missing": missing,
        "wound_ok": wound_ok,
        "authority_ok": authority_ok,
        "paths_ok": paths_ok,
        "tests_ok": tests_ok,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build a non-executing RHP proposal packet")
    parser.add_argument("--wound-class", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--allowed-path", action="append", default=[])
    parser.add_argument("--test-command", action="append", default=[])
    parser.add_argument("--risk-level", default="medium")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    packet = build_proposal(
        wound_class=args.wound_class,
        subject=args.subject,
        summary=args.summary,
        allowed_paths=args.allowed_path,
        test_commands=args.test_command,
        risk_level=args.risk_level,
    )
    packet["validation"] = validate_proposal(packet)
    text = json.dumps(packet, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if packet["validation"]["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
