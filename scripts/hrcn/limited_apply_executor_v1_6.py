#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_PHRASE = "I AUTHORIZE HRCN V1.6 LIMITED DOCS CONTEXT APPLY"
ALLOWED_EXACT = {"README.md"}
ALLOWED_PREFIXES = ("docs/context-layer/",)
BLOCKED_PREFIXES = ("cms/", "agent/", "tools/", "skills/", "plugins/", "providers/", "gateway/", "hermes_cli/", "tui_gateway/", "ui-tui/", "web/")
BLOCKED_EXACT = {"pyproject.toml", "uv.lock", "package.json", "package-lock.json"}

@dataclass(frozen=True)
class ApplyOp:
    path: str
    operation: str
    content: str | None = None
    sha256: str | None = None

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

def is_allowed_path(path: str) -> bool:
    p = normalize_path(path)
    if p in BLOCKED_EXACT or any(p.startswith(prefix) for prefix in BLOCKED_PREFIXES):
        return False
    return p in ALLOWED_EXACT or any(p.startswith(prefix) for prefix in ALLOWED_PREFIXES)

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_packet(packet_path: Path) -> dict[str, Any]:
    data = json.loads(packet_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Packet root must be an object.")
    return data

def parse_ops(packet: dict[str, Any]) -> list[ApplyOp]:
    raw_ops = packet.get("operations")
    if not isinstance(raw_ops, list) or not raw_ops:
        raise ValueError("Packet must contain non-empty operations array.")
    ops: list[ApplyOp] = []
    for idx, item in enumerate(raw_ops):
        if not isinstance(item, dict):
            raise ValueError(f"Operation {idx} must be an object.")
        path = normalize_path(str(item.get("path", "")))
        operation = str(item.get("operation", "")).lower().strip()
        if operation not in {"add", "modify", "delete"}:
            raise ValueError(f"Unsupported operation: {operation}")
        if not is_allowed_path(path):
            raise ValueError(f"Path outside v1.6 scope: {path}")
        content = item.get("content")
        if operation in {"add", "modify"} and not isinstance(content, str):
            raise ValueError("add/modify operations require string content.")
        if operation == "delete":
            content = None
        expected_hash = item.get("sha256")
        if expected_hash is not None and str(expected_hash) != sha256_text(content or ""):
            raise ValueError(f"Content sha256 mismatch: {path}")
        ops.append(ApplyOp(path=path, operation=operation, content=content, sha256=expected_hash))
    return ops

def require_clean_tree(root: Path) -> None:
    proc = run_git(["status", "--short"], root)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr)
    if proc.stdout.strip():
        raise RuntimeError("Working tree must be clean before limited apply.")

def require_base_commit(root: Path, expected: str | None) -> None:
    if not expected:
        raise ValueError("Packet must include expected_base_commit.")
    head = run_git(["rev-parse", "HEAD"], root)
    if head.returncode != 0:
        raise RuntimeError(head.stderr)
    actual = head.stdout.strip()
    if actual != expected:
        raise RuntimeError(f"HEAD mismatch. expected={expected} actual={actual}")

def validate_packet(packet: dict[str, Any], authorize: bool, phrase: str) -> list[ApplyOp]:
    if packet.get("schema") != "HRCN-v1.6-limited-apply-packet":
        raise ValueError("Unsupported packet schema.")
    if packet.get("authority_class") != "limited_docs_context_apply":
        raise ValueError("authority_class must be limited_docs_context_apply.")
    if packet.get("apply_gate_decision") != "eligible_for_future_limited_apply_executor":
        raise ValueError("apply_gate_decision is not eligible.")
    if packet.get("human_authorization_required") is not True:
        raise ValueError("human_authorization_required must be true.")
    for required in ("rollback_plan_ref", "validation_plan_ref", "evidence_package_ref"):
        if packet.get(required) in (None, ""):
            raise ValueError(f"{required} is required.")
    if packet.get("secret_scan_required") is not True:
        raise ValueError("secret_scan_required must be true.")
    if authorize and phrase != REQUIRED_PHRASE:
        raise ValueError("Authorization phrase mismatch.")
    return parse_ops(packet)

def write_audit(root: Path, packet: dict[str, Any], ops: list[ApplyOp], applied: bool) -> Path:
    out_dir = root / "docs" / "context-layer" / "hrcn-v1.6-apply-ledger"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    audit_path = out_dir / f"limited-apply-{stamp}.json"
    audit = {
        "schema": "HRCN-v1.6-limited-apply-audit",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "packet_id": packet.get("packet_id"),
        "applied": applied,
        "authority_granted": bool(applied),
        "operations": [op.__dict__ for op in ops],
    }
    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return audit_path

def apply_ops(root: Path, ops: list[ApplyOp]) -> None:
    for op in ops:
        target = root / op.path
        if op.operation == "delete":
            if target.exists():
                target.unlink()
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(op.content or "", encoding="utf-8", newline="\n")

def main() -> int:
    parser = argparse.ArgumentParser(description="HRCN v1.6 limited docs/context apply executor")
    parser.add_argument("--packet", required=True)
    parser.add_argument("--plan", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--authorization-phrase", default="")
    args = parser.parse_args()

    if args.plan == args.apply:
        raise SystemExit("Choose exactly one mode: --plan or --apply")

    root = repo_root()
    packet_path = Path(args.packet)
    if not packet_path.is_absolute():
        packet_path = root / packet_path

    packet = load_packet(packet_path)
    ops = validate_packet(packet, authorize=args.apply, phrase=args.authorization_phrase)
    require_base_commit(root, packet.get("expected_base_commit"))
    require_clean_tree(root)

    plan = {
        "schema": "HRCN-v1.6-limited-apply-plan",
        "packet_id": packet.get("packet_id"),
        "mode": "apply" if args.apply else "plan",
        "operation_count": len(ops),
        "operations": [op.__dict__ for op in ops],
        "allowed_scope": ["README.md", "docs/context-layer/**"],
        "applied": False,
        "authority_granted": False,
    }
    print(json.dumps(plan, indent=2, sort_keys=True))

    if args.plan:
        return 0

    apply_ops(root, ops)
    audit_path = write_audit(root, packet, ops, applied=True)
    print(json.dumps({"applied": True, "audit_path": str(audit_path.relative_to(root))}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
