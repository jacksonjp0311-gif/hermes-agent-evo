from __future__ import annotations
import json
import os
import sys
from pathlib import Path

root = Path(r"C:\Users\jacks\OneDrive\Desktop\hermes-agent-evo")
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
os.chdir(root)

os.environ["HERMES_RHP_NATIVE_BOOT"] = "1"
os.environ["HERMES_RHP_BOOT_PREFLIGHT"] = "preflight"
os.environ["HERMES_RHP_CONTEXT"] = "proposal"
os.environ["HERMES_HRCN_CONTEXT"] = "proposal"

from rhp.boot_preflight import format_boot_context_for_prompt, run_boot_preflight
from rhp.startup_context_packet import build_startup_context_packet

boot = run_boot_preflight(root)
packet = build_startup_context_packet(root)
context = format_boot_context_for_prompt(root)

payload = {
    "boot": boot.as_dict() if hasattr(boot, "as_dict") else boot.__dict__,
    "packet": packet.as_dict() if hasattr(packet, "as_dict") else packet.__dict__,
    "context_contains_v02": "RHP-BOOT-PREFLIGHT-PACKET-v0.2" in context,
}
print(json.dumps(payload, indent=2))

assert boot.ok is True
assert boot.latest_rhp_evidence == "docs/context-layer/ops/RHP-011-final-evidence.json"
assert packet.ok is True
assert packet.schema == "RHP-STARTUP-CONTEXT-PACKET-v0.3"
assert "RHP-BOOT-PREFLIGHT-PACKET-v0.2" in context