from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

LATEST_EVIDENCE = "docs/context-layer/ops/RHP-013-5-final-evidence.json"
PREVIOUS_EVIDENCE = "docs/context-layer/ops/RHP-013-4-final-evidence.json"
LATEST_POINTER = "docs/context-layer/latest-rhp.json"

AUTHORITY_FALSE_KEYS = [
    "provider_call_executed", "model_call_executed", "tool_use_executed",
    "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
    "api_write", "dependency_mutation_committed", "self_authorization",
    "autonomous_authority", "external_ingestion",
]

@dataclass(frozen=True)
class AlignmentResult:
    ok: bool
    repo_root: str
    mode: str
    checks: dict[str, bool] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {"ok": self.ok, "repo_root": self.repo_root, "mode": self.mode, "checks": dict(self.checks), "failures": list(self.failures)}

def find_repo_root(start: str | Path | None = None) -> Path:
    current = Path(start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".git").exists():
            return candidate
    raise FileNotFoundError("Could not locate Hermes repository root")

def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")

def _json(path: Path) -> dict[str, Any]:
    data = json.loads(_read(path))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data

def _json_or_empty(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        return _json(path)
    except Exception:
        return {}

def _false_authority(data: dict[str, Any]) -> bool:
    return all(data.get(key) is False for key in AUTHORITY_FALSE_KEYS if key in data)

def _rhp0135_boundary_shape(data: dict[str, Any]) -> bool:
    return (
        data.get("schema") == "RHP-013.5-final-evidence"
        and data.get("operation") == "RHP-013.5"
        and data.get("ci_watch_loop_automation_added") is True
        and _false_authority(data)
    )

def _rhp0135_final_green(data: dict[str, Any]) -> bool:
    return (
        _rhp0135_boundary_shape(data)
        and data.get("runtimebootstate_display_wired") is True
        and data.get("stale_operator_visible_test_repaired") is True
        and data.get("py_compile_passed") is True
        and data.get("focused_tests_passed") is True
        and data.get("alignment_guard_self_check_passed") is True
    )

def validate_alignment(repo_root: str | Path | None = None, *, require_latest_passed: bool = True) -> AlignmentResult:
    root = find_repo_root(repo_root)
    mode = "final" if require_latest_passed else "preflight"
    readme = _read(root / "README.md")
    rhp_readme = _read(root / "rhp" / "README.md")
    startup_packet = _read(root / "rhp" / "startup_context_packet.py")
    boot_preflight = _read(root / "rhp" / "boot_preflight.py")
    operator_status = _read(root / "rhp" / "operator_startup_status.py")
    banner = _read(root / "hermes_cli" / "banner.py")
    ci_watch = _read(root / "rhp" / "ci_watch.py")
    previous = _json(root / PREVIOUS_EVIDENCE)
    legacy_latest_path = root / LATEST_EVIDENCE
    latest_exists = legacy_latest_path.is_file()
    legacy_latest = _json_or_empty(legacy_latest_path)
    pointer_path = root / LATEST_POINTER
    pointer = _json_or_empty(pointer_path)
    current_operation = str(pointer.get("latest_operation", ""))
    current_rel = str(pointer.get("latest_evidence", ""))
    current_next = str(pointer.get("next_operation", ""))
    current_path = root / current_rel if current_rel else root / "__missing_latest_evidence__"
    current = _json_or_empty(current_path)
    legacy_boundary = _rhp0135_boundary_shape(legacy_latest)
    legacy_final = _rhp0135_final_green(legacy_latest)
    checks: dict[str, bool] = {}
    checks["previous_rhp0134_passed"] = (
        previous.get("schema") == "RHP-013.4-final-evidence"
        and previous.get("operation") == "RHP-013.4"
        and previous.get("runtimebootstate_display_wired") is True
        and previous.get("focused_tests_passed") is True
        and _false_authority(previous)
    )
    checks["latest_evidence_exists"] = latest_exists
    checks["latest_rhp0135_has_boundary_shape"] = legacy_boundary
    checks["latest_rhp0135_passed"] = legacy_final if require_latest_passed else True
    checks["current_pointer_exists"] = pointer_path.is_file()
    checks["current_pointer_shape"] = bool(current_operation and current_rel and current_next)
    checks["current_evidence_exists"] = current_path.is_file()
    checks["current_evidence_alignment"] = current.get("operation") == current_operation
    checks["current_evidence_authority_false"] = _false_authority(current)
    checks["root_readme_latest_evidence"] = (
        LATEST_EVIDENCE in readme
        or current_rel in readme
        or current_operation in readme
        or "RHP_014_9_AUTOHEAL_DRY_RUN" in readme
        or "RHP-014.9" in readme
    )
    checks["root_readme_current_status"] = (
        "RHP-013.5 CI Watch Loop automation + stale operator-visible test repair sealed" in readme
        or "RHP-013.5 CI Watch Loop automation sealed" in readme
        or current_operation in readme
        or "RHP-014.9 adds autoheal executor dry-run" in readme
        or "RHP-014.9" in readme
    )
    checks["rhp_readme_rhp0135_present"] = "RHP-013.5 CI Watch Loop" in rhp_readme
    checks["runtimebootstate_schema_present"] = "RHP-RUNTIME-BOOT-STATE-v0.1" in startup_packet
    checks["runtimebootstate_evidence_0135"] = "RHP-013.5" in startup_packet
    checks["boot_preflight_latest_evidence_present"] = LATEST_EVIDENCE in boot_preflight
    checks["operator_status_evidence_0135"] = "RHP-013.5" in operator_status
    checks["banner_evidence_0135"] = "RHP-013.5" in banner
    checks["ci_watch_tool_present"] = "RHP-CI-WATCH-PACKET-v0.1" in ci_watch
    failures = [key for key, value in checks.items() if value is not True]
    return AlignmentResult(ok=not failures, repo_root=str(root), mode=mode, checks=checks, failures=failures)

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="RHP README/state/bridge/evidence alignment guard")
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args(argv)
    result = validate_alignment(args.repo_root, require_latest_passed=not args.preflight)
    print(json.dumps(result.as_dict(), indent=2))
    return 0 if result.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
