from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

LATEST_EVIDENCE = "docs/context-layer/ops/RHP-013-1-final-evidence.json"
PREVIOUS_EVIDENCE = "docs/context-layer/ops/RHP-013-0-final-evidence.json"

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

def _json(path: Path) -> dict:
    data = json.loads(_read(path))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data

def _false_authority(data: dict) -> bool:
    return all(data.get(key) is False for key in AUTHORITY_FALSE_KEYS if key in data)

def validate_alignment(repo_root: str | Path | None = None, *, require_latest_passed: bool = True) -> AlignmentResult:
    root = find_repo_root(repo_root)
    mode = "final" if require_latest_passed else "preflight"
    readme = _read(root / "README.md")
    rhp_readme = _read(root / "rhp" / "README.md")
    startup_packet = _read(root / "rhp" / "startup_context_packet.py")
    boot_preflight = _read(root / "rhp" / "boot_preflight.py")
    previous = _json(root / PREVIOUS_EVIDENCE)
    latest_path = root / LATEST_EVIDENCE
    latest_exists = latest_path.is_file()
    latest = _json(latest_path) if latest_exists else {}

    checks: dict[str, bool] = {}
    checks["previous_rhp0130_passed"] = (
        previous.get("schema") == "RHP-013.0-final-evidence"
        and previous.get("operation") == "RHP-013.0"
        and previous.get("evo_identity_block_added") is True
        and previous.get("runtimebootstate_implemented") is False
        and _false_authority(previous)
    )
    checks["latest_evidence_exists"] = latest_exists
    checks["root_readme_latest_evidence"] = LATEST_EVIDENCE in readme
    checks["root_readme_current_status"] = "RHP-013.1 RuntimeBootState v0.1 typed packet implemented" in readme
    checks["rhp_readme_rhp0131_present"] = "RHP-013.1 RuntimeBootState v0.1" in rhp_readme
    checks["runtimebootstate_schema_present"] = "RHP-RUNTIME-BOOT-STATE-v0.1" in startup_packet
    checks["runtimebootstate_builder_present"] = "def build_runtime_boot_state(" in startup_packet
    checks["boot_preflight_latest_evidence_present"] = LATEST_EVIDENCE in boot_preflight

    if require_latest_passed:
        checks["latest_rhp0131_passed"] = (
            latest.get("schema") == "RHP-013.1-final-evidence"
            and latest.get("operation") == "RHP-013.1"
            and latest.get("runtimebootstate_implemented") is True
            and latest.get("py_compile_passed") is True
            and latest.get("focused_tests_passed") is True
            and latest.get("alignment_guard_self_check_passed") is True
            and _false_authority(latest)
        )
    else:
        checks["latest_rhp0131_has_boundary_shape"] = (
            latest.get("schema") == "RHP-013.1-final-evidence"
            and latest.get("operation") == "RHP-013.1"
            and latest.get("runtimebootstate_implemented") is True
            and _false_authority(latest)
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
