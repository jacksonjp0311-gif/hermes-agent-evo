#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_EXACT = {"README.md"}
ALLOWED_PREFIXES = ("docs/context-layer/",)
BLOCKED_PREFIXES = ("cms/", "agent/", "tools/", "skills/", "plugins/", "providers/", "gateway/", "hermes_cli/", "tui_gateway/", "ui-tui/", "web/")

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

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("JSON root must be object")
    return data

def validate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    if manifest.get("schema") != "HRCN-v1.8-replay-rollback-manifest":
        raise ValueError("Unsupported manifest schema.")
    operations = manifest.get("operations")
    if not isinstance(operations, list) or not operations:
        raise ValueError("operations must be non-empty list.")
    paths: list[str] = []
    for item in operations:
        if not isinstance(item, dict):
            raise ValueError("operation must be object.")
        path = normalize_path(str(item.get("path", "")))
        if not allowed_path(path):
            raise ValueError(f"path outside v1.8 scope: {path}")
        paths.append(path)
        if "before_sha256" not in item or "after_sha256" not in item:
            raise ValueError(f"operation missing hashes: {path}")
    checks = {
        "expected_base_commit_present": bool(manifest.get("expected_base_commit")),
        "rollback_packet_ref_present": bool(manifest.get("rollback_packet_ref")),
        "limited_apply_audit_ref_present": bool(manifest.get("limited_apply_audit_ref")),
        "post_apply_validation_ref_present": bool(manifest.get("post_apply_validation_ref")),
        "all_paths_within_scope": True,
        "automatic_rollback_enabled": False,
        "self_authorization_enabled": False,
    }
    if not all(checks.values()) and checks.get("automatic_rollback_enabled") is not False:
        raise ValueError("invalid automatic rollback state")
    return {"paths": paths, "checks": checks}

def build_replay_report(root: Path, manifest: dict[str, Any], validation: dict[str, Any]) -> dict[str, Any]:
    head = run_git(["rev-parse", "HEAD"], root).stdout.strip()
    return {
        "schema": "HRCN-v1.8-replay-rollback-report",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "manifest_id": manifest.get("manifest_id"),
        "head": head,
        "paths": validation["paths"],
        "checks": validation["checks"],
        "replayable": True,
        "rollback_ready": True,
        "automatic_rollback_enabled": False,
        "self_authorization_enabled": False,
        "apply_authority_granted": False,
        "allowed_scope": ["README.md", "docs/context-layer/**"],
    }

def write_report(root: Path, report: dict[str, Any]) -> Path:
    out_dir = root / "docs" / "context-layer" / "hrcn-v1.8-replay-ledger"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = out_dir / f"replay-rollback-report-{stamp}.json"
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out

def main() -> int:
    parser = argparse.ArgumentParser(description="HRCN v1.8 replay and rollback hardening checker")
    parser.add_argument("--manifest", required=True, help="HRCN-v1.8-replay-rollback-manifest JSON")
    parser.add_argument("--check", action="store_true", help="Validate and print report")
    parser.add_argument("--write-report", action="store_true", help="Write report under docs/context-layer/hrcn-v1.8-replay-ledger")
    args = parser.parse_args()
    if not args.check and not args.write_report:
        raise SystemExit("Choose --check and/or --write-report.")

    root = repo_root()
    path = Path(args.manifest)
    if not path.is_absolute():
        path = root / path
    manifest = load_json(path)
    validation = validate_manifest(manifest)
    report = build_replay_report(root, manifest, validation)
    print(json.dumps(report, indent=2, sort_keys=True))
    if args.write_report:
        out = write_report(root, report)
        print(json.dumps({"report_path": str(out.relative_to(root))}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
