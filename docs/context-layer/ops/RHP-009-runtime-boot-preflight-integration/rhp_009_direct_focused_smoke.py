from pathlib import Path
import json
import os
import sys

def find_repo_root(start: Path) -> Path:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".git").exists():
            return candidate
    raise RuntimeError("could not locate repo root")

root = find_repo_root(Path(__file__))
root_str = str(root)
if root_str not in sys.path:
    sys.path.insert(0, root_str)

os.chdir(root)
os.environ["HERMES_RHP_CONTEXT"] = "proposal"
os.environ["HERMES_HRCN_CONTEXT"] = "proposal"
os.environ["HERMES_RHP_BOOT_PREFLIGHT"] = "preflight"

from rhp.boot_preflight import format_boot_context_for_prompt, run_boot_preflight
from rhp.alignment_guard import validate_alignment

packet = run_boot_preflight(root)
data = packet.as_dict()

assert packet.ok is True
assert packet.boot_phase == "pre_interaction"
assert packet.rhp_evidence_green is True
assert packet.hrcn_boundary_green is True
assert packet.alignment_guard_green is True
assert packet.rhp_context_requested is True
assert packet.hrcn_context_requested is True
assert packet.startup_context_packet_created is True

for key in [
    "provider_call_executed",
    "model_call_executed",
    "tool_use_executed",
    "cms_runtime_execution",
    "cms_write",
    "memory_write",
    "memory_promotion",
    "api_write",
    "dependency_mutation_committed",
    "external_ingestion",
    "self_authorization",
    "autonomous_authority",
]:
    assert data[key] is False, key

context = format_boot_context_for_prompt(root)
assert "RHP-BOOT-PREFLIGHT-PACKET-v0.1" in context
assert '"ok": true' in context
assert "external_ingestion" in context

preflight_alignment = validate_alignment(root, require_latest_passed=False)
assert preflight_alignment.ok is True

print(json.dumps({
    "ok": True,
    "runner": "direct_python_focused_smoke_no_pytest",
    "repo_root_anchored": True,
    "boot_packet_ok": packet.ok,
    "startup_context_packet_created": packet.startup_context_packet_created,
    "alignment_guard_preflight_green": preflight_alignment.ok,
    "authority_flags_false": True
}, indent=2))