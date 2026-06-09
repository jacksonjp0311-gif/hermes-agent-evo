from pathlib import Path
import json
import os
import sys

root = Path(__file__).resolve().parents[4]
root_str = str(root)
if root_str not in sys.path:
    sys.path.insert(0, root_str)
os.chdir(root)
os.environ["HERMES_RHP_BOOT_PREFLIGHT"] = "preflight"
os.environ["HERMES_RHP_CONTEXT"] = "proposal"
os.environ["HERMES_HRCN_CONTEXT"] = "proposal"

from rhp.startup_context_packet import build_startup_context_packet, packet_json
from rhp.alignment_guard import validate_alignment

packet = build_startup_context_packet(root)
data = packet.as_dict()
assert packet.ok is True
assert packet.schema == "RHP-STARTUP-CONTEXT-PACKET-v0.2"
assert packet.installed_launcher_exists is True
assert packet.native_boot_hook_present is True
assert packet.boot_preflight_ok is True
for key in ["provider_call_executed","model_call_executed","tool_use_executed","cms_runtime_execution","cms_write","memory_write","memory_promotion","api_write","dependency_mutation_committed","external_ingestion","self_authorization","autonomous_authority"]:
    assert data[key] is False, key
text = packet_json(root)
assert "RHP-STARTUP-CONTEXT-PACKET-v0.2" in text
assert '"ok": true' in text
preflight_alignment = validate_alignment(root, require_latest_passed=False)
assert preflight_alignment.ok is True
print(json.dumps({"ok": True, "runner": "direct_python_focused_smoke_no_pytest", "startup_context_packet_ok": packet.ok, "native_boot_hook_present": packet.native_boot_hook_present, "alignment_guard_preflight_green": preflight_alignment.ok, "authority_flags_false": True}, indent=2))