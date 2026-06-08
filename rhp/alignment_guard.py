# RHP README/state/bridge/evidence alignment guard.
#
# This guard verifies that the public README, /rhp mini README, bridge surfaces,
# and latest evidence agree before future RHP commits.

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


LATEST_RHP = "RHP-006"
LATEST_EVIDENCE = "docs/context-layer/ops/RHP-006-final-evidence.json"
PREVIOUS_EVIDENCE = "docs/context-layer/ops/RHP-005-final-evidence.json"
HRCN_TAG = "hrcn-ops-v0.3.0"
HRCN_EVIDENCE = "docs/context-layer/ops/OPS-027-final-evidence.json"


@dataclass(frozen=True)
class AlignmentResult:
    ok: bool
    repo_root: str
    checks: dict[str, bool] = field(default_factory=dict)
    failures: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "ok": self.ok,
            "repo_root": self.repo_root,
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


def _contains(text: str, needle: str) -> bool:
    return needle in text


def _git_status_clean(root: Path) -> bool:
    proc = subprocess.run(["git", "status", "--short"], cwd=str(root), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # During an operation the tree may be dirty; this guard checks coherence, not cleanliness.
    return proc.returncode == 0


def validate_alignment(repo_root: str | Path | None = None) -> AlignmentResult:
    root = find_repo_root(repo_root)
    failures: list[str] = []
    checks: dict[str, bool] = {}

    readme = _read(root / "README.md")
    rhp_readme = _read(root / "rhp" / "README.md")
    hrcn_bridge = _read(root / "hrcn_runtime_bridge.py")
    rhp_bridge = _read(root / "rhp_runtime_bridge.py")

    previous = _json(root / PREVIOUS_EVIDENCE)
    latest_path = root / LATEST_EVIDENCE
    latest_exists = latest_path.is_file()
    latest = _json(latest_path) if latest_exists else {}

    checks["previous_rhp005_passed"] = previous.get("py_compile_passed") is True and previous.get("focused_tests_passed") is True and previous.get("guard_self_check_passed") is True
    checks["latest_evidence_exists"] = latest_exists
    checks["latest_rhp006_passed"] = latest.get("py_compile_passed") is True and latest.get("focused_tests_passed") is True and latest.get("alignment_guard_self_check_passed") is True
    checks["root_readme_latest_evidence"] = _contains(readme, LATEST_EVIDENCE)
    checks["root_readme_rhp006_passed"] = _contains(readme, "| RHP-006 | Add README/state/bridge/evidence alignment guard before future RHP commits. | passed |")
    checks["root_readme_next_rhp007"] = _contains(readme, "| RHP-007 | First governed RHP → HRCN → Hermes proposal-loop proof. | next |")
    checks["rhp_readme_latest_boundary"] = _contains(rhp_readme, "Current repository boundary: RHP-006.")
    checks["rhp_readme_latest_evidence"] = _contains(rhp_readme, LATEST_EVIDENCE)
    checks["rhp_readme_alignment_guard"] = _contains(rhp_readme, "alignment_guard.py")
    checks["hrcn_bridge_v03_anchor"] = _contains(hrcn_bridge, "OPS-027-final-evidence.json") and _contains(hrcn_bridge, HRCN_TAG)
    checks["rhp_bridge_read_only"] = _contains(rhp_bridge, "READ ONLY PROPOSAL ORIENTATION")
    checks["rhp005_next_was_rhp006"] = previous.get("next_recommended_operation") == "RHP-006 README/state/bridge/evidence alignment guard before future RHP commits"
    checks["authority_false"] = all(latest.get(key) is False for key in [
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
    ])
    checks["git_status_command_available"] = _git_status_clean(root)

    for key, value in checks.items():
        if not value:
            failures.append(key)

    return AlignmentResult(ok=not failures, repo_root=str(root), checks=checks, failures=failures)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="RHP README/state/bridge/evidence alignment guard")
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = validate_alignment(args.repo_root)
    print(json.dumps(result.as_dict(), indent=2))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
