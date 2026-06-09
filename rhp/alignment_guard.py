from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path

LATEST_EVIDENCE = "docs/context-layer/ops/RHP-011-2-final-evidence.json"
PREVIOUS_EVIDENCE = "docs/context-layer/ops/RHP-011-1-final-evidence.json"

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

    previous = _json(root / PREVIOUS_EVIDENCE)
    latest_path = root / LATEST_EVIDENCE
    latest_exists = latest_path.is_file()
    latest = _json(latest_path) if latest_exists else {}

    stale_forbidden = [
        "RHP is the active runtime-threshold track and is current through RHP-010.",
        "HRCN v2.0 + OPS-027 + RHP-010 = read-only runtime-native boot orientation through direct Hermes executable startup.",
        "| RHP-011 | Installed launcher smoke and operator-visible startup status. | next |",
        "| next | RHP-011 installed launcher smoke and operator-visible startup status. | next |",
    ]

    checks: dict[str, bool] = {}
    checks["previous_rhp011_1_passed"] = (
        previous.get("schema") == "RHP-011.1-final-evidence"
        and previous.get("operation") == "RHP-011.1"
        and previous.get("rehydration_protocol_strip_passed") is True
        and previous.get("gold_interface_strip_smoke_passed") is True
        and previous.get("context_truth_alignment_passed") is True
        and previous.get("alignment_guard_self_check_passed") is True
        and all(previous.get(key) is False for key in AUTHORITY_FALSE_KEYS)
    )
    checks["latest_evidence_exists"] = latest_exists
    checks["root_readme_latest_evidence"] = LATEST_EVIDENCE in readme
    checks["root_readme_current_status"] = "RHP-011.2 README geometry and evidence hygiene closure passed" in readme
    checks["root_readme_next_rhp012"] = "RHP-012" in readme and "Safe boot failure mode" in readme
    checks["root_readme_no_stale_rhp010_current"] = all(item not in readme for item in stale_forbidden)
    checks["root_readme_rhp011_1_and_011_2_rows"] = "RHP-011.1 | Gold interface Rehydration Protocol strip" in readme and "RHP-011.2 | README geometry and evidence hygiene closure" in readme
    checks["failure_lessons_036_to_041_present"] = all(f"RHP-L-0{n}" in readme for n in range(36, 42))
    checks["rhp_readme_rhp011_2_present"] = "RHP-011.2 README geometry and evidence hygiene closure" in rhp_readme
    checks["banner_rehydration_protocol_strip"] = (
        "_rhp_rehydration_protocol_lines" in banner_py
        and "Rehydration Protocol" in banner_py
        and "#7DF9FF" in banner_py
        and "#B388FF" in banner_py
    )
    checks["banner_strip_inserted"] = "left_lines.extend(_rhp_rehydration_protocol_lines())" in banner_py
    checks["boot_preflight_runtime_anchor_still_rhp011"] = "docs/context-layer/ops/RHP-011-final-evidence.json" in boot_py
    checks["startup_packet_mentions_rhp011_1"] = "RHP-011.1" in startup_py and "RHP-STARTUP-CONTEXT-PACKET-v0.3" in startup_py
    checks["operator_status_hooked"] = "_rhp_render_operator_status" in main_py and "RHP rehydration complete" in main_py
    checks["ascii_safe_hook"] = _managed_hook(main_py).isascii() and bool(_managed_hook(main_py))

    if require_latest_passed:
        checks["latest_rhp011_2_passed"] = (
            latest.get("schema") == "RHP-011.2-final-evidence"
            and latest.get("operation") == "RHP-011.2"
            and latest.get("readme_geometry_closure_passed") is True
            and latest.get("evidence_hygiene_closure_passed") is True
            and latest.get("progress_telemetry_contract_recorded") is True
            and latest.get("alignment_guard_self_check_passed") is True
            and all(latest.get(key) is False for key in AUTHORITY_FALSE_KEYS)
        )
    else:
        checks["latest_rhp011_2_has_boundary_shape"] = (
            latest.get("schema") == "RHP-011.2-final-evidence"
            and latest.get("operation") == "RHP-011.2"
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