from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

RHP_CI_WOUND_PACKET_SCHEMA = "RHP-CI-WOUND-PACKET-v0.1"

def build_packet(
    *,
    wound_class: str,
    subject_commit: str,
    workflow: str,
    run_url: str,
    failed_test_file: str,
    repro_command: str,
    source: str,
    root_cause: str,
    observed_at_utc: str | None = None,
) -> dict[str, Any]:
    if not subject_commit:
        raise ValueError("subject_commit is required")
    if not wound_class:
        raise ValueError("wound_class is required")
    return {
        "schema": RHP_CI_WOUND_PACKET_SCHEMA,
        "wound_class": wound_class,
        "subject_type": "git_commit",
        "subject_commit": subject_commit,
        "workflow": workflow,
        "run_url": run_url,
        "failed_test_file": failed_test_file,
        "repro_command": repro_command,
        "source": source,
        "observed_at_utc": observed_at_utc or dt.datetime.now(dt.timezone.utc).isoformat(),
        "root_cause": root_cause,
        "status": "open",
        "ci_status": "red",
        "integration_closed": False,
        "authority_granted": False,
        "execution_enabled": False,
        "non_claim_lock": "CI wound packet records a remote CI failure only. It does not repair, rerun CI, mutate dependencies, or grant authority.",
    }

def validate_packet(packet: dict[str, Any]) -> dict[str, Any]:
    required = [
        "schema", "wound_class", "subject_commit", "workflow", "run_url",
        "failed_test_file", "repro_command", "source", "authority_granted", "execution_enabled"
    ]
    missing = [key for key in required if key not in packet]
    authority_ok = packet.get("authority_granted") is False and packet.get("execution_enabled") is False
    return {
        "ok": not missing and authority_ok and bool(packet.get("subject_commit")) and bool(packet.get("repro_command")),
        "missing": missing,
        "authority_ok": authority_ok,
    }

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build a remote CI wound packet")
    parser.add_argument("--wound-class", required=True)
    parser.add_argument("--subject-commit", required=True)
    parser.add_argument("--workflow", default="Tests")
    parser.add_argument("--run-url", default="")
    parser.add_argument("--failed-test-file", required=True)
    parser.add_argument("--repro-command", required=True)
    parser.add_argument("--source", default="github-actions-verified")
    parser.add_argument("--root-cause", required=True)
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    packet = build_packet(
        wound_class=args.wound_class,
        subject_commit=args.subject_commit,
        workflow=args.workflow,
        run_url=args.run_url,
        failed_test_file=args.failed_test_file,
        repro_command=args.repro_command,
        source=args.source,
        root_cause=args.root_cause,
    )
    packet["validation"] = validate_packet(packet)
    text = json.dumps(packet, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if packet["validation"]["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
