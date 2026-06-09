# RHP README/state/bridge/evidence alignment guard.
from __future__ import annotations
import argparse, json, subprocess
from dataclasses import dataclass, field
from pathlib import Path
LATEST_EVIDENCE = "docs/context-layer/ops/RHP-010-final-evidence.json"
PREVIOUS_EVIDENCE = "docs/context-layer/ops/RHP-009-final-evidence.json"
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
def _managed_text(readme: str) -> str:
    chunks=[]
    for start,end in [
        ("<!-- HERMES_CURRENT_PUBLIC_METRICS_START -->","<!-- HERMES_CURRENT_PUBLIC_METRICS_END -->"),
        ("<!-- HERMES_RHP_RUNTIME_ACTIVATION_START -->","<!-- HERMES_RHP_RUNTIME_ACTIVATION_END -->"),
        ("<!-- HRCN_OPS_OPERATIONAL_BRIDGE_STATUS_START -->","<!-- HRCN_OPS_OPERATIONAL_BRIDGE_STATUS_END -->"),
        ("<!-- HRCN_POST_SEAL_CYBERNETIC_TRACK_START -->","<!-- HRCN_POST_SEAL_CYBERNETIC_TRACK_END -->"),
    ]:
        if start in readme and end in readme:
            chunks.append(readme.split(start,1)[1].split(end,1)[0])
    return "\n".join(chunks)
def validate_alignment(repo_root: str | Path | None = None, *, require_latest_passed: bool = True) -> AlignmentResult:
    root = find_repo_root(repo_root); failures=[]; checks={}; mode="final" if require_latest_passed else "preflight"
    readme=_read(root/"README.md"); rhp_readme=_read(root/"rhp"/"README.md"); hrcn_bridge=_read(root/"hrcn_runtime_bridge.py"); rhp_bridge=_read(root/"rhp_runtime_bridge.py"); agent_init=_read(root/"agent"/"agent_init.py"); main_py=_read(root/"hermes_cli"/"main.py")
    previous=_json(root/PREVIOUS_EVIDENCE); latest_path=root/LATEST_EVIDENCE; latest_exists=latest_path.is_file(); latest=_json(latest_path) if latest_exists else {}
    checks["previous_rhp009_passed"] = previous.get("runtime_boot_preflight_integration_passed") is True and previous.get("boot_preflight_packet_ok") is True and previous.get("agent_init_boot_preflight_hooked") is True and previous.get("alignment_guard_self_check_passed") is True
    checks["latest_evidence_exists"] = latest_exists
    checks["root_readme_latest_evidence"] = _contains(readme, LATEST_EVIDENCE)
    checks["root_readme_no_codex_header"] = "## Codex / RCC-CMS-HRCN Context Layer" not in readme and "## RCC-CMS-HRCN Runtime Governance Layer" in readme
    checks["root_readme_rhp010_passed"] = _contains(readme, "| RHP-010 | Runtime-native boot interconnect. | passed |")
    checks["root_readme_next_rhp011"] = _contains(readme, "| RHP-011 | Installed launcher smoke and operator-visible startup status. | next |")
    checks["root_public_metrics_latest_rhp"] = _contains(readme, "| Latest RHP proof | `docs/context-layer/ops/RHP-010-final-evidence.json` |")
    checks["root_readme_no_mojibake_in_managed_blocks"] = "Ã" not in _managed_text(readme)
    checks["rhp_readme_latest_evidence"] = _contains(rhp_readme, "RHP-010-final-evidence.json")
    checks["rhp_readme_runtime_native"] = _contains(rhp_readme, "Runtime-Native Boot Interconnect")
    checks["native_hook_present"] = _contains(main_py, "RHP-010 RUNTIME-NATIVE BOOT INTERCONNECT START") and _contains(main_py, "_rhp_native_boot_orientation_early()")
    checks["agent_init_boot_preflight_hook"] = _contains(agent_init, "_maybe_append_rhp_boot_preflight_context") and _contains(agent_init, "[RHP BOOT PREFLIGHT CONTEXT]")
    checks["startup_packet_exists"] = (root/"rhp"/"startup_context_packet.py").is_file()
    checks["hrcn_bridge_v03_anchor"] = _contains(hrcn_bridge, "OPS-027-final-evidence.json") and _contains(hrcn_bridge, HRCN_TAG)
    checks["rhp_bridge_read_only"] = _contains(rhp_bridge, "READ ONLY PROPOSAL ORIENTATION")
    checks["authority_false"] = all(latest.get(k) is False for k in ["provider_call_executed","model_call_executed","tool_use_executed","cms_runtime_execution","cms_write","memory_write","memory_promotion","api_write","dependency_mutation_committed","self_authorization","autonomous_authority","external_ingestion"])
    checks["git_status_command_available"] = _git_status_command_available(root)
    if require_latest_passed:
        checks["latest_rhp010_passed"] = latest.get("schema")=="RHP-010-final-evidence" and latest.get("operation")=="RHP-010" and latest.get("runtime_native_boot_interconnect_passed") is True and latest.get("direct_hermes_import_boot_status_ok") is True and latest.get("readme_stale_surface_repaired") is True and latest.get("py_compile_passed") is True and latest.get("focused_tests_passed") is True and latest.get("alignment_guard_self_check_passed") is True
    else:
        checks["latest_rhp010_has_boundary_shape"] = latest.get("schema")=="RHP-010-final-evidence" and latest.get("operation")=="RHP-010" and latest.get("failed_tests_are_commit_blockers") is True
    for key, value in checks.items():
        if not value: failures.append(key)
    return AlignmentResult(ok=not failures, repo_root=str(root), mode=mode, checks=checks, failures=failures)
def main(argv=None):
    parser=argparse.ArgumentParser(description="RHP README/state/bridge/evidence alignment guard"); parser.add_argument("--repo-root", default=None); parser.add_argument("--json", action="store_true"); parser.add_argument("--preflight", action="store_true")
    args=parser.parse_args(argv); result=validate_alignment(args.repo_root, require_latest_passed=not args.preflight); print(json.dumps(result.as_dict(), indent=2)); return 0 if result.ok else 1
if __name__ == "__main__": raise SystemExit(main())