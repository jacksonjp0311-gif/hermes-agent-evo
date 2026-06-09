from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

LATEST_EVIDENCE = "docs/context-layer/ops/RHP-012-final-evidence.json"
PREVIOUS_EVIDENCE = "docs/context-layer/ops/RHP-011-2-final-evidence.json"

AUTHORITY_FALSE_KEYS = [
    "provider_call_executed",
    "model_call_executed",
    "tool_use_executed",
    "cms_runtime_execution",
    "cms_write",
    "memory_write",
    "memory_promotion",
    "api_write",
    "dependency_mutation_committed",
    "self_authorization",
    "autonomous_authority",
    "external_ingestion",
]

@dataclass(frozen=True)
class AlignmentResult:
    ok: bool
    repo_root: str
    mode: str
    checks: dict[str, bool] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "ok": self.ok,
            "repo_root": self.repo_root,
            "mode": self.mode,
            "checks": dict(self.checks),
            "failures": list(self.failures),
        }

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

def _json(path: Path) -> dict:
    data = json.loads(_read(path))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data

def _managed_hook(main_py: str) -> str:
    start = "# RHP-010 RUNTIME-NATIVE BOOT INTERCONNECT START"
    end = "# RHP-010 RUNTIME-NATIVE BOOT INTERCONNECT END"
    if start in main_py and end in main_py:
        return main_py.split(start, 1)[1].split(end, 1)[0]
    return ""

def validate_alignment(repo_root: str | Path | None = None, *, require_latest_passed: bool = True) -> AlignmentResult:
    root = find_repo_root(repo_root)
    mode = "final" if require_latest_passed else "preflight"

    readme = _read(root / "README.md")
    rhp_readme = _read(root / "rhp" / "README.md")
    main_py = _read(root / "hermes_cli" / "main.py")
    banner_py = _read(root / "hermes_cli" / "banner.py")
    boot_py = _read(root / "rhp" / "boot_preflight.py")
    startup_py = _read(root / "rhp" / "startup_context_packet.py")
    operator_py = _read(root / "rhp" / "operator_startup_status.py")

    previous = _json(root / PREVIOUS_EVIDENCE)
    latest_path = root / LATEST_EVIDENCE
    latest_exists = latest_path.is_file()
    latest = _json(latest_path) if latest_exists else {}

    checks: dict[str, bool] = {}
    checks["previous_rhp011_2_passed"] = (
        previous.get("schema") == "RHP-011.2-final-evidence"
        and previous.get("operation") == "RHP-011.2"
        and previous.get("readme_geometry_closure_passed") is True
        and previous.get("evidence_hygiene_closure_passed") is True
        and previous.get("progress_telemetry_contract_recorded") is True
        and previous.get("alignment_guard_self_check_passed") is True
        and all(previous.get(key) is False for key in AUTHORITY_FALSE_KEYS)
    )
    checks["latest_evidence_exists"] = latest_exists
    checks["root_readme_latest_evidence"] = LATEST_EVIDENCE in readme
    checks["root_readme_current_status"] = "RHP-012 safe boot failure mode and degraded startup status passed" in readme
    checks["root_readme_next_rhp013"] = "RHP-013" in readme and "operator dashboard and status packet normalization" in readme
    checks["rhp_readme_rhp012_present"] = "RHP-012 safe boot failure mode and degraded startup status" in rhp_readme
    checks["failure_lessons_042_043_present"] = "RHP-L-042" in readme and "RHP-L-043" in readme
    checks["boot_preflight_safe_degraded"] = (
        "RHP-012 safe boot failure mode" in boot_py
        and "_read_json_or_empty" in boot_py
        and "degraded_reason" in boot_py
        and "boot_status" in boot_py
        and "RHP-BOOT-PREFLIGHT-PACKET-v0.3" in boot_py
    )
    checks["operator_status_degraded"] = (
        "RHP-012 operator-visible startup status with degraded mode" in operator_py
        and "DEGRADED" in operator_py
        and "RHP degraded reason" in operator_py
    )
    checks["startup_packet_v04"] = "RHP-STARTUP-CONTEXT-PACKET-v0.4" in startup_py and "boot_preflight_degraded" in startup_py
    checks["banner_rehydration_protocol_strip"] = (
        "_rhp_rehydration_protocol_lines" in banner_py
        and "Rehydration Protocol" in banner_py
        and "#7DF9FF" in banner_py
        and "#B388FF" in banner_py
    )
    checks["banner_strip_inserted"] = "left_lines.extend(_rhp_rehydration_protocol_lines())" in banner_py
    checks["operator_status_hooked"] = "_rhp_render_operator_status" in main_py and "RHP rehydration complete" in main_py
    checks["ascii_safe_hook"] = _managed_hook(main_py).isascii() and bool(_managed_hook(main_py))

    if require_latest_passed:
        checks["latest_rhp012_passed"] = (
            latest.get("schema") == "RHP-012-final-evidence"
            and latest.get("operation") == "RHP-012"
            and latest.get("safe_boot_degraded_status_passed") is True
            and latest.get("missing_evidence_negative_control_passed") is True
            and latest.get("operator_degraded_render_passed") is True
            and latest.get("live_boot_green_path_passed") is True
            and latest.get("alignment_guard_self_check_passed") is True
            and all(latest.get(key) is False for key in AUTHORITY_FALSE_KEYS)
        )
    else:
        checks["latest_rhp012_has_boundary_shape"] = (
            latest.get("schema") == "RHP-012-final-evidence"
            and latest.get("operation") == "RHP-012"
            and latest.get("failed_tests_are_commit_blockers") is True
            and all(latest.get(key) is False for key in AUTHORITY_FALSE_KEYS)
        )

    failures = [key for key, value in checks.items() if not value]
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