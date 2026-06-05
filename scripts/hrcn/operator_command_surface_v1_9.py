#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CURRENT = "HRCN v1.9"
NEXT = "HRCN v2.0"
LOOP_STEPS = ["observe", "propose", "classify", "dry_run", "evidence", "authorize", "limited_apply", "validate", "ledger"]
ALLOWED_EXACT = {"README.md"}
ALLOWED_PREFIXES = ("docs/context-layer/",)
BLOCKED_PREFIXES = ("cms/", "agent/", "tools/", "skills/", "plugins/", "providers/", "gateway/", "hermes_cli/", "tui_gateway/", "ui-tui/", "web/")
REQUIRED_AUTHORIZATION_PHRASE = "I AUTHORIZE HRCN V1.6 LIMITED DOCS CONTEXT APPLY"

def run_git(args: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)

def repo_root() -> Path:
    proc = run_git(["rev-parse", "--show-toplevel"], Path.cwd())
    if proc.returncode != 0:
        raise SystemExit("Not inside a git repository.")
    return Path(proc.stdout.strip())

def normalize_path(raw: str) -> str:
    p = raw.replace("\\", "/").strip()
    if not p or p.startswith("/") or ".." in Path(p).parts:
        raise ValueError(f"Unsafe path: {raw}")
    return p

def allowed_path(path: str) -> bool:
    p = normalize_path(path)
    if any(p.startswith(prefix) for prefix in BLOCKED_PREFIXES):
        return False
    return p in ALLOWED_EXACT or any(p.startswith(prefix) for prefix in ALLOWED_PREFIXES)

def load_validation(root: Path, version: str) -> dict[str, Any]:
    path = root / "docs" / "context-layer" / f"hrcn-{version}.validation.json"
    return json.loads(path.read_text(encoding="utf-8"))

def status(root: Path) -> dict[str, Any]:
    head = run_git(["rev-parse", "HEAD"], root).stdout.strip()
    git_status = run_git(["status", "--short"], root).stdout.splitlines()
    versions = ["v1.6", "v1.7", "v1.8"]
    validations = {v: load_validation(root, v) for v in versions}
    return {
        "schema": "HRCN-v1.9-operator-status",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "head": head,
        "working_tree_clean": len(git_status) == 0,
        "current": CURRENT,
        "next": NEXT,
        "validated_dependencies": {
            v: {
                "passed": validations[v].get("passed"),
                "checkpoint": validations[v].get("checkpoint"),
                "roadmap_current": validations[v].get("roadmap_current"),
                "roadmap_next": validations[v].get("roadmap_next"),
            }
            for v in versions
        },
        "allowed_scope": ["README.md", "docs/context-layer/**"],
        "blocked_scope": ["cms/**", "runtime folders", "dependency files", "local secrets", "external APIs"],
        "self_authorization_enabled": False,
        "automatic_apply_enabled": False,
        "automatic_rollback_enabled": False,
        "api_write_authority_granted": False,
    }

def gate_matrix() -> dict[str, Any]:
    return {
        "schema": "HRCN-v1.9-gate-matrix",
        "steps": LOOP_STEPS,
        "required_before_apply": [
            "clean worktree",
            "expected base commit",
            "operation packet",
            "bounded target paths",
            "dry-run/evidence package",
            "human authorization",
            "v1.6 limited apply packet",
            "secret scan",
            "post-apply validation",
            "v1.8 replay/rollback manifest",
        ],
        "invariants": {
            "self_authorization_enabled": False,
            "automatic_apply_enabled": False,
            "automatic_rollback_enabled": False,
            "scope": ["README.md", "docs/context-layer/**"],
        },
    }

def make_packet_template(root: Path, target_paths: list[str], summary: str) -> Path:
    normalized = [normalize_path(p) for p in target_paths]
    blocked = [p for p in normalized if not allowed_path(p)]
    if blocked:
        raise ValueError(f"Paths outside HRCN v1.9/v1.6 scope: {blocked}")

    out_dir = root / "docs" / "context-layer" / "hrcn-v1.9-operator-packets"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = out_dir / f"operation-packet-template-{stamp}.json"
    head = run_git(["rev-parse", "HEAD"], root).stdout.strip()
    packet = {
        "schema": "HRCN-v1.7-governed-operation-packet",
        "packet_id": f"hrcn-v1.9-template-{stamp}",
        "created_by": "HRCN v1.9 operator command surface",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "expected_base_commit": head,
        "summary": summary,
        "loop_steps": LOOP_STEPS,
        "target_paths": normalized,
        "requires_human_authorization": True,
        "self_authorization_enabled": False,
        "automatic_apply_enabled": False,
        "automatic_rollback_enabled": False,
        "next_manual_steps": [
            "review packet",
            "prepare dry-run/evidence package",
            "prepare v1.6 limited apply packet if authorized",
            "run v1.8 replay/rollback hardening after any future apply",
        ],
    }
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out

def next_commands() -> dict[str, Any]:
    return {
        "schema": "HRCN-v1.9-next-commands",
        "commands": {
            "status": "python scripts/hrcn/operator_command_surface_v1_9.py --status",
            "gates": "python scripts/hrcn/operator_command_surface_v1_9.py --gates",
            "make_packet_template": "python scripts/hrcn/operator_command_surface_v1_9.py --make-packet-template --summary \"...run summary...\" --target README.md",
            "loop_status": "python scripts/hrcn/governed_operational_loop_v1_7.py --packet <packet.json> --status-only",
            "limited_apply_plan": "python scripts/hrcn/limited_apply_executor_v1_6.py --packet <apply-packet.json> --plan",
            "replay_check": "python scripts/hrcn/replay_rollback_hardening_v1_8.py --manifest <manifest.json> --check",
        },
        "non_claim_lock": "Commands expose operations; they do not authorize operations.",
    }

def main() -> int:
    parser = argparse.ArgumentParser(description="HRCN v1.9 operator command surface")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--gates", action="store_true")
    parser.add_argument("--next-commands", action="store_true")
    parser.add_argument("--make-packet-template", action="store_true")
    parser.add_argument("--target", action="append", default=[])
    parser.add_argument("--summary", default="")
    args = parser.parse_args()

    root = repo_root()
    selected = sum(bool(x) for x in [args.status, args.gates, args.next_commands, args.make_packet_template])
    if selected == 0:
        args.status = True
    if selected > 1:
        raise SystemExit("Choose one operator command at a time.")

    if args.status:
        print(json.dumps(status(root), indent=2, sort_keys=True))
    elif args.gates:
        print(json.dumps(gate_matrix(), indent=2, sort_keys=True))
    elif args.next_commands:
        print(json.dumps(next_commands(), indent=2, sort_keys=True))
    elif args.make_packet_template:
        if not args.target:
            raise SystemExit("--make-packet-template requires at least one --target")
        if not args.summary:
            raise SystemExit("--make-packet-template requires --summary")
        out = make_packet_template(root, args.target, args.summary)
        print(json.dumps({"packet_template": str(out.relative_to(root)), "applied": False, "authority_granted": False}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
