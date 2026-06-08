# RHP README/state/bridge/evidence alignment guard.
from __future__ import annotations
import argparse, json, subprocess
from dataclasses import dataclass, field
from pathlib import Path
LATEST_EVIDENCE = "docs/context-layer/ops/RHP-008-final-evidence.json"
PREVIOUS_EVIDENCE = "docs/context-layer/ops/RHP-007-final-evidence.json"
HRCN_TAG = "hrcn-ops-v0.3.0"
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
    if current.is_file(): current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".git").exists(): return candidate
    raise FileNotFoundError("Could not locate Hermes repository root")
def _read(path: Path) -> str: return path.read_text(encoding="utf-8", errors="replace")
def _json(path: Path) -> dict:
    data = json.loads(_read(path))
    if not isinstance(data, dict): raise ValueError(f"Expected JSON object: {path}")
    return data
def _contains(text: str, needle: str) -> bool: return needle in text
def _git_status_command_available(root: Path) -> bool:
    return subprocess.run(["git", "status", "--short"], cwd=str(root), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).returncode == 0
def validate_alignment(repo_root: str | Path | None = None, *, require_latest_passed: bool = True) -> AlignmentResult:
    root = find_repo_root(repo_root); failures=[]; checks={}; mode="final" if require_latest_passed else "preflight"
    readme=_read(root/"README.md"); rhp_readme=_read(root/"rhp"/"README.md"); hrcn_bridge=_read(root/"hrcn_runtime_bridge.py"); rhp_bridge=_read(root/"rhp_runtime_bridge.py")
    previous=_json(root/PREVIOUS_EVIDENCE); latest_path=root/LATEST_EVIDENCE; latest_exists=latest_path.is_file(); latest=_json(latest_path) if latest_exists else {}
    checks["previous_rhp007_passed"] = previous.get("governed_proposal_loop_proof_passed") is True and previous.get("rhp_before_hrcn_context_order") is True and previous.get("py_compile_passed") is True and previous.get("focused_tests_passed") is True
    checks["latest_evidence_exists"] = latest_exists
    checks["root_readme_latest_evidence"] = _contains(readme, LATEST_EVIDENCE)
    checks["root_readme_rhp008_passed"] = _contains(readme, "| RHP-008 | Proposal-loop negative-control and apply-gate boundary proof. | passed |")
    checks["root_readme_next_rhp009"] = _contains(readme, "| RHP-009 | Human apply-gate dry-run contract proof. | next |")
    checks["root_public_metrics_latest_rhp"] = _contains(readme, "| Latest RHP proof | `docs/context-layer/ops/RHP-008-final-evidence.json` |")
    checks["rhp_readme_latest_boundary"] = _contains(rhp_readme, "Current repository boundary: RHP-008.")
    checks["rhp_readme_latest_evidence"] = _contains(rhp_readme, "RHP-008-final-evidence.json")
    checks["rhp_readme_negative_control"] = _contains(rhp_readme, "apply_gate_negative_control.py")
    checks["hrcn_bridge_v03_anchor"] = _contains(hrcn_bridge, "OPS-027-final-evidence.json") and _contains(hrcn_bridge, HRCN_TAG)
    checks["rhp_bridge_read_only"] = _contains(rhp_bridge, "READ ONLY PROPOSAL ORIENTATION")
    checks["authority_false"] = all(latest.get(k) is False for k in ["provider_call_executed","model_call_executed","tool_use_executed","cms_runtime_execution","cms_write","memory_write","memory_promotion","api_write","dependency_mutation_committed","self_authorization","autonomous_authority","codex_ingestion"])
    checks["git_status_command_available"] = _git_status_command_available(root)
    if require_latest_passed:
        checks["latest_rhp008_passed"] = latest.get("schema")=="RHP-008-final-evidence" and latest.get("operation")=="RHP-008" and latest.get("apply_gate_negative_control_passed") is True and latest.get("all_escalations_refused") is True and latest.get("human_apply_gate_present") is False and latest.get("py_compile_passed") is True and latest.get("focused_tests_passed") is True and latest.get("alignment_guard_self_check_passed") is True
    else:
        checks["latest_rhp008_has_boundary_shape"] = latest.get("schema")=="RHP-008-final-evidence" and latest.get("operation")=="RHP-008" and latest.get("failed_tests_are_commit_blockers") is True
    for key, value in checks.items():
        if not value: failures.append(key)
    return AlignmentResult(ok=not failures, repo_root=str(root), mode=mode, checks=checks, failures=failures)
def main(argv=None):
    parser=argparse.ArgumentParser(description="RHP README/state/bridge/evidence alignment guard"); parser.add_argument("--repo-root", default=None); parser.add_argument("--json", action="store_true"); parser.add_argument("--preflight", action="store_true")
    args=parser.parse_args(argv); result=validate_alignment(args.repo_root, require_latest_passed=not args.preflight); print(json.dumps(result.as_dict(), indent=2)); return 0 if result.ok else 1
if __name__ == "__main__": raise SystemExit(main())