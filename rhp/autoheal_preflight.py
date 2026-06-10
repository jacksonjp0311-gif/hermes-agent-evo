
# RHP-013.9 Autoheal Preflight Box.
from __future__ import annotations
import argparse, fnmatch, json, subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RHP_AUTOHEAL_PREFLIGHT_SCHEMA = "RHP-AUTOHEAL-PREFLIGHT-v0.1"

DEFAULT_RESIDUE_ALLOWLIST = [
    "README.md",
    "AGENTS.md",
    "rhp/README.md",
    "rhp/autoheal_preflight.py",
    "rhp/autoheal_plan.py",
    "tests/test_rhp_013_9_autoheal_preflight.py",
    "tests/test_rhp_013_9_autoheal_plan.py",
    "docs/context-layer/ops/RHP-013-9*",
]

@dataclass(frozen=True)
class PreflightResult:
    schema: str
    ok: bool
    status: str
    operation: str
    dirty_paths: list[str] = field(default_factory=list)
    allowed_paths: list[str] = field(default_factory=list)
    blocked_paths: list[str] = field(default_factory=list)
    action: str = "none"
    verified: bool = False
    glyph: str = "[OK]"
    non_claim_lock: str = (
        "Autoheal preflight may classify and optionally clean bounded failed-attempt residue only. "
        "It grants no runtime, tool, CMS, memory, API, external-ingestion, autonomous, or self-authorization authority."
    )

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def git_status_short(repo_root: str | Path = ".") -> list[str]:
    p = subprocess.run(["git", "status", "--short"], cwd=str(repo_root), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        raise RuntimeError(p.stdout)
    paths = []
    for line in p.stdout.splitlines():
        if len(line) >= 4:
            paths.append(line[3:].strip().replace("\\", "/"))
    return paths

def path_allowed(path: str, allowlist: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in allowlist)

def classify_dirty(paths: list[str], operation: str, allowlist: list[str] | None = None) -> PreflightResult:
    allowlist = allowlist or DEFAULT_RESIDUE_ALLOWLIST
    allowed = [p for p in paths if path_allowed(p, allowlist)]
    blocked = [p for p in paths if not path_allowed(p, allowlist)]
    if not paths:
        return PreflightResult(RHP_AUTOHEAL_PREFLIGHT_SCHEMA, True, "clean", operation, [], [], [], "continue", True, "[OK]")
    if blocked:
        return PreflightResult(RHP_AUTOHEAL_PREFLIGHT_SCHEMA, False, "blocked_dirty_worktree", operation, paths, allowed, blocked, "stop", False, "[BLOCKED]")
    return PreflightResult(RHP_AUTOHEAL_PREFLIGHT_SCHEMA, True, "bounded_residue_detected", operation, paths, allowed, [], "clean_bounded_residue_then_continue", False, "[WARN]")

def render_preflight_box(result: PreflightResult) -> str:
    lines = [
        f"RHPLOAD [003%] loop=AUTOHEAL-PREFLIGHT operation={result.operation} | status={result.status}",
        "`- autoheal preflight box",
        f"   +- dirty paths: {len(result.dirty_paths)}",
        f"   +- allowed residue: {len(result.allowed_paths)}",
        f"   +- blocked paths: {len(result.blocked_paths)}",
        f"   +- action: {result.action}",
        f"   `- verified: {str(result.verified).lower()} {result.glyph}",
    ]
    for path in result.blocked_paths:
        lines.append(f"      blocked: {path}")
    return "\n".join(lines)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="RHP autoheal preflight classifier")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--operation", default="RHP")
    p.add_argument("--path", action="append", default=[])
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    paths = args.path if args.path else git_status_short(args.repo_root)
    result = classify_dirty(paths, args.operation)
    print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False) if args.json else render_preflight_box(result))
    return 0 if result.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
