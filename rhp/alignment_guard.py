# RHP README/state/bridge/evidence alignment guard.
from __future__ import annotations
import argparse, json, subprocess
from dataclasses import dataclass, field
from pathlib import Path
LATEST_EVIDENCE = "docs/context-layer/ops/RHP-011-final-evidence.json"
PREVIOUS_EVIDENCE = "docs/context-layer/ops/RHP-010-final-evidence.json"
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
def _rhp_managed_main_text(main_py: str) -> str:
    start = "# RHP-010 RUNTIME-NATIVE BOOT INTERCONNECT START"
    end = "# RHP-010 RUNTIME-NATIVE BOOT INTERCONNECT END"
    if start in main_py and end in main_py:
        return main_py.split(start, 1)[1].split(end, 1)[0]
    return ""
def _git_status_command_available(root: Path) -> bool:
    return subprocess.run(["git", "status", "--short"], cwd=str(root), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).returncode == 0
def validate_alignment(repo_root: str | Path | None = None, *, require_latest_passed: bool = True) -> AlignmentResult:
    root = find_repo_root(repo_root); failures=[]; checks={}; mode="final" if require_latest_passed else "preflight"
    readme=_read(root/"README.md"); rhp_readme=_read(root/"rhp"/"README.md"); main_py=_read(root/"hermes_cli"/"main.py")
    previous=_json(root/PREVIOUS_EVIDENCE); latest_path=root/LATEST_EVIDENCE; latest_exists=latest_path.is_file(); latest=_json(latest_path) if latest_exists else {}
    checks["previous_rhp010_passed"] = previous.get("runtime_native_boot_interconnect_passed") is True and previous.get("direct_hermes_import_boot_status_ok") is True and previous.get("startup_context_packet_ok") is True and previous.get("alignment_guard_self_check_passed") is True
    checks["latest_evidence_exists"] = latest_exists
    checks["root_readme_latest_evidence"] = _contains(readme, LATEST_EVIDENCE)
    checks["root_readme_rhp011_passed"] = _contains(readme, "| RHP-011 | Operator-visible startup lock sequence. | passed |")
    checks["root_readme_next_rhp012"] = _contains(readme, "| RHP-012 | Safe boot failure mode and degraded startup status. | next |")
    checks["root_public_metrics_latest_rhp"] = _contains(readme, "| Latest RHP proof | `docs/context-layer/ops/RHP-011-final-evidence.json` |")
    checks["rhp_readme_operator_visible"] = _contains(rhp_readme, "Operator-Visible Startup Lock Sequence")
    checks["operator_status_exists"] = (root/"rhp"/"operator_startup_status.py").is_file()
    checks["operator_status_hooked"] = _contains(main_py, "_rhp_render_operator_status") and _contains(main_py, "RHP rehydration complete")
    checks["startup_packet_exists"] = (root/"rhp"/"startup_context_packet.py").is_file()
    checks["ascii_safe_hook"] = _rhp_managed_main_text(main_py).isascii() and bool(_rhp_managed_main_text(main_py))
    checks["authority_false"] = all(latest.get(k) is False for k in ["provider_call_executed","model_call_executed","tool_use_executed","cms_runtime_execution","cms_write","memory_write","memory_promotion","api_write","dependency_mutation_committed","self_authorization","autonomous_authority","external_ingestion"])
    checks["git_status_command_available"] = _git_status_command_available(root)
    if require_latest_passed:
        checks["latest_rhp011_passed"] = latest.get("schema")=="RHP-011-final-evidence" and latest.get("operation")=="RHP-011" and latest.get("operator_visible_startup_locks_passed") is True and latest.get("operator_status_ascii_safe") is True and latest.get("installed_launcher_visible_status_smoke_passed") is True and latest.get("py_compile_passed") is True and latest.get("focused_tests_passed") is True and latest.get("alignment_guard_self_check_passed") is True
    else:
        checks["latest_rhp011_has_boundary_shape"] = latest.get("schema")=="RHP-011-final-evidence" and latest.get("operation")=="RHP-011" and latest.get("failed_tests_are_commit_blockers") is True
    for key, value in checks.items():
        if not value: failures.append(key)
    return AlignmentResult(ok=not failures, repo_root=str(root), mode=mode, checks=checks, failures=failures)
def main(argv=None):
    parser=argparse.ArgumentParser(description="RHP README/state/bridge/evidence alignment guard"); parser.add_argument("--repo-root", default=None); parser.add_argument("--json", action="store_true"); parser.add_argument("--preflight", action="store_true")
    args=parser.parse_args(argv); result=validate_alignment(args.repo_root, require_latest_passed=not args.preflight); print(json.dumps(result.as_dict(), indent=2)); return 0 if result.ok else 1
if __name__ == "__main__": raise SystemExit(main())
