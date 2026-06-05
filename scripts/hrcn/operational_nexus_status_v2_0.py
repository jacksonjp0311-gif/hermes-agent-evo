#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CURRENT = "HRCN v2.0"
NEXT = "HRCN v2.1"
REQUIRED_VALIDATIONS = [
    "v1.0.3",
    "v1.1",
    "v1.2",
    "v1.3",
    "v1.4",
    "v1.5",
    "v1.6",
    "v1.7",
    "v1.8",
    "v1.9",
]
REQUIRED_TOOLS = [
    "scripts/hrcn/limited_apply_executor_v1_6.py",
    "scripts/hrcn/governed_operational_loop_v1_7.py",
    "scripts/hrcn/replay_rollback_hardening_v1_8.py",
    "scripts/hrcn/operator_command_surface_v1_9.py",
]

def run_git(args: list[str], root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *args], cwd=root, text=True, capture_output=True, check=False)

def repo_root() -> Path:
    proc = run_git(["rev-parse", "--show-toplevel"], Path.cwd())
    if proc.returncode != 0:
        raise SystemExit("Not inside a git repository.")
    return Path(proc.stdout.strip())

def read_validation(root: Path, version: str) -> dict[str, Any]:
    path = root / "docs" / "context-layer" / f"hrcn-{version}.validation.json"
    if not path.exists():
        return {"version": version, "exists": False, "passed": False}
    data = json.loads(path.read_text(encoding="utf-8"))
    data["exists"] = True
    return data

def build_status(root: Path) -> dict[str, Any]:
    head = run_git(["rev-parse", "HEAD"], root).stdout.strip()
    worktree = run_git(["status", "--short"], root).stdout.splitlines()
    validations = {v: read_validation(root, v) for v in REQUIRED_VALIDATIONS}
    tools = {p: (root / p).exists() for p in REQUIRED_TOOLS}
    all_validations_passed = all(v.get("exists") and v.get("passed") for v in validations.values())
    all_tools_present = all(tools.values())
    return {
        "schema": "HRCN-v2.0-operational-nexus-status",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "current": CURRENT,
        "next": NEXT,
        "head": head,
        "working_tree_clean": len(worktree) == 0,
        "operational_scope": ["README.md", "docs/context-layer/**"],
        "required_validations": validations,
        "required_tools": tools,
        "all_validations_passed": all_validations_passed,
        "all_tools_present": all_tools_present,
        "operational_for_docs_context_governance": bool(all_validations_passed and all_tools_present),
        "runtime_integration_enabled": False,
        "cms_write_authority_granted": False,
        "memory_write_authority_granted": False,
        "api_write_authority_granted": False,
        "dependency_mutation_authorized": False,
        "self_authorization_enabled": False,
        "autonomous_authority_granted": False,
        "human_operator_required": True,
    }

def write_report(root: Path, status: dict[str, Any]) -> Path:
    out_dir = root / "docs" / "context-layer" / "hrcn-v2.0-nexus-reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = out_dir / f"operational-nexus-status-{stamp}.json"
    out.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out

def main() -> int:
    parser = argparse.ArgumentParser(description="HRCN v2.0 operational nexus status")
    parser.add_argument("--status", action="store_true", help="Print operational nexus status")
    parser.add_argument("--write-report", action="store_true", help="Write status report under docs/context-layer/hrcn-v2.0-nexus-reports")
    args = parser.parse_args()
    if not args.status and not args.write_report:
        args.status = True

    root = repo_root()
    status = build_status(root)
    print(json.dumps(status, indent=2, sort_keys=True))
    if args.write_report:
        out = write_report(root, status)
        print(json.dumps({"report_path": str(out.relative_to(root))}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
