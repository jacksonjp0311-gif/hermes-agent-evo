#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

LOOP_STEPS = [
    "observe",
    "propose",
    "classify",
    "dry_run",
    "evidence",
    "authorize",
    "limited_apply",
    "validate",
    "ledger",
]

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

def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON root must be object")
    return data

def validate_operation_packet(packet: dict[str, Any]) -> list[str]:
    if packet.get("schema") != "HRCN-v1.7-governed-operation-packet":
        raise ValueError("Unsupported packet schema.")
    if packet.get("loop_steps") != LOOP_STEPS:
        raise ValueError("loop_steps must match HRCN v1.7 sequence.")
    paths = packet.get("target_paths", [])
    if not isinstance(paths, list) or not paths:
        raise ValueError("target_paths must be a non-empty list.")
    normalized = [normalize_path(str(p)) for p in paths]
    blocked = [p for p in normalized if not allowed_path(p)]
    if blocked:
        raise ValueError(f"Paths outside v1.7/v1.6 scope: {blocked}")
    if packet.get("self_authorization_enabled") is not False:
        raise ValueError("self_authorization_enabled must be false.")
    if packet.get("automatic_apply_enabled") is not False:
        raise ValueError("automatic_apply_enabled must be false.")
    if packet.get("requires_human_authorization") is not True:
        raise ValueError("requires_human_authorization must be true.")
    return normalized

def build_status(root: Path, packet: dict[str, Any], paths: list[str]) -> dict[str, Any]:
    head = run_git(["rev-parse", "HEAD"], root).stdout.strip()
    return {
        "schema": "HRCN-v1.7-governed-loop-status",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "packet_id": packet.get("packet_id"),
        "head": head,
        "loop_steps": LOOP_STEPS,
        "target_paths": paths,
        "allowed_scope": ["README.md", "docs/context-layer/**"],
        "requires_human_authorization": True,
        "self_authorization_enabled": False,
        "automatic_apply_enabled": False,
        "apply_authority_granted": False,
        "next_allowed_action": "prepare_v1_6_limited_apply_packet_after_human_authorization",
    }

def write_ledger(root: Path, status: dict[str, Any]) -> Path:
    out_dir = root / "docs" / "context-layer" / "hrcn-v1.7-operational-ledger"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = out_dir / f"loop-status-{stamp}.json"
    out.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out

def main() -> int:
    parser = argparse.ArgumentParser(description="HRCN v1.7 governed operational loop controller")
    parser.add_argument("--packet", required=True, help="HRCN-v1.7-governed-operation-packet JSON")
    parser.add_argument("--status-only", action="store_true", help="Validate packet and print loop status")
    parser.add_argument("--write-ledger", action="store_true", help="Write docs/context ledger status JSON")
    args = parser.parse_args()

    root = repo_root()
    packet_path = Path(args.packet)
    if not packet_path.is_absolute():
        packet_path = root / packet_path

    packet = load_json(packet_path)
    paths = validate_operation_packet(packet)
    status = build_status(root, packet, paths)
    print(json.dumps(status, indent=2, sort_keys=True))

    if args.write_ledger:
        out = write_ledger(root, status)
        print(json.dumps({"ledger_path": str(out.relative_to(root))}, indent=2))

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
