# RHP-014.3 autoheal executor dry-run.
from __future__ import annotations
import argparse, json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RHP_AUTOHEAL_DRY_RUN_SCHEMA = "RHP-AUTOHEAL-DRY-RUN-v0.1"

@dataclass(frozen=True)
class DryRun:
    schema: str
    ok: bool
    classification: str
    would_mutate: bool
    would_commit: bool
    allowed_paths: list[str] = field(default_factory=list)
    planned_steps: list[str] = field(default_factory=list)
    validation_commands: list[list[str]] = field(default_factory=list)
    stop_reason: str = ""
    non_claim_lock: str = "Dry-run autoheal never mutates, commits, pushes, grants authority, calls providers, writes CMS/memory/API state, or performs remote CI mutation."

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def dry_run_for_packet(packet: dict[str, Any]) -> DryRun:
    classification = str(packet.get("classification", "unknown"))
    if classification == "no_failure_detected":
        return DryRun(RHP_AUTOHEAL_DRY_RUN_SCHEMA, True, classification, False, False, [], ["seal NO-OP evidence"], [], "")
    if classification == "module_path_execution_bug":
        return DryRun(RHP_AUTOHEAL_DRY_RUN_SCHEMA, True, classification, False, False, ["AGENTS.md", "rhp/README.md"], ["switch direct file execution to python -m package execution", "add focused import test"], [["python", "-m", "py_compile", "rhp/resume_packet.py"]])
    if classification == "current_script_identity_mismatch":
        return DryRun(RHP_AUTOHEAL_DRY_RUN_SCHEMA, True, classification, False, False, ["docs/context-layer/ops/<operation>-final-evidence.json"], ["block push", "repair evidence/script identity only if current operation owns the file", "rerun current-script gate"], [["python", "-m", "rhp.current_script_gate"]])
    if classification == "stream_output_leak_or_crlf_noise":
        return DryRun(RHP_AUTOHEAL_DRY_RUN_SCHEMA, True, classification, False, False, ["rhp/stream_collapse.py", "rhp/command_runner.py"], ["wrap noisy command through command_runner", "write raw stream to evidence", "print only box"], [["python", "-m", "pytest", "-q", "tests/test_rhp_014_2_v3_stream_collapse_strict.py"]])
    if classification == "stale_evidence_key_surface":
        return DryRun(RHP_AUTOHEAL_DRY_RUN_SCHEMA, True, classification, False, False, ["tests/*alignment*", "rhp/alignment_guard.py", "docs/context-layer/ops/*final-evidence.json"], ["update stale test/guard key expectation", "preserve authority=false keys", "rerun focused guard tests"], [["python", "-m", "pytest", "-q", "tests/test_rhp_alignment_guard.py"]])
    if classification == "assertion_failure":
        return DryRun(RHP_AUTOHEAL_DRY_RUN_SCHEMA, True, classification, False, False, ["tests/<focused>", "rhp/<focused>"], ["extract exact assertion", "identify source vs stale-test surface", "propose smallest patch"], [["python", "-m", "pytest", "-q", "<focused-test>"]])
    return DryRun(RHP_AUTOHEAL_DRY_RUN_SCHEMA, False, classification, False, False, [], ["return to DIAGNOSIS loop"], [], "no bounded dry-run plan exists")

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Generate dry-run autoheal plan from CI wound packet")
    p.add_argument("--packet", required=True)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    packet = json.loads(Path(args.packet).read_text(encoding="utf-8"))
    dry = dry_run_for_packet(packet)
    print(json.dumps(dry.as_dict(), indent=2, ensure_ascii=False))
    return 0 if dry.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
