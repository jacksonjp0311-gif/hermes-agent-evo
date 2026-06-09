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

import rhp.boot_preflight as boot_preflight
from rhp.operator_startup_status import build_operator_startup_status, render_operator_startup_status
from rhp.startup_context_packet import build_startup_context_packet

live = boot_preflight.run_boot_preflight(root)
live_status = build_operator_startup_status(live, evidence="RHP-012")
live_packet = build_startup_context_packet(root)

if not live.ok:
    raise AssertionError({"live_boot_not_ok": live.as_dict()})
if live.boot_status != "ok":
    raise AssertionError({"live_boot_status": live.as_dict()})
if not live_status.ok or live_status.status != "ok":
    raise AssertionError({"live_operator_status": live_status.as_dict()})
if not live_packet.ok or live_packet.schema != "RHP-STARTUP-CONTEXT-PACKET-v0.4":
    raise AssertionError({"live_packet": live_packet.as_dict()})

original_latest = boot_preflight.LATEST_RHP_EVIDENCE
boot_preflight.LATEST_RHP_EVIDENCE = "docs/context-layer/ops/DOES-NOT-EXIST-RHP-012-NEGATIVE-CONTROL.json"
try:
    degraded = boot_preflight.run_boot_preflight(root)
finally:
    boot_preflight.LATEST_RHP_EVIDENCE = original_latest

degraded_status = build_operator_startup_status(degraded, evidence="RHP-012-NEGATIVE")
degraded_render = render_operator_startup_status(degraded, evidence="RHP-012-NEGATIVE")

assert degraded.ok is False
assert degraded.degraded is True
assert degraded.boot_status == "degraded"
assert degraded.checks["latest_rhp_evidence_exists"] is False
assert degraded.provider_call_executed is False
assert degraded.model_call_executed is False
assert degraded.tool_use_executed is False
assert degraded.cms_write is False
assert degraded.memory_promotion is False
assert degraded.api_write is False
assert degraded.autonomous_authority is False
assert degraded.external_ingestion is False
assert degraded_status.status == "degraded"
assert "RHP degraded reason:" in degraded_render
assert "authority boundary" in degraded_render

payload = {
    "ok": True,
    "live_boot_green_path_passed": True,
    "missing_evidence_negative_control_passed": True,
    "operator_degraded_render_passed": True,
    "live_boot_status": live.boot_status,
    "live_packet_schema": live_packet.schema,
    "degraded_boot_status": degraded.boot_status,
    "degraded_reason": degraded.degraded_reason,
    "authority_false_in_negative_control": {
        "provider_call_executed": degraded.provider_call_executed,
        "model_call_executed": degraded.model_call_executed,
        "tool_use_executed": degraded.tool_use_executed,
        "cms_write": degraded.cms_write,
        "memory_promotion": degraded.memory_promotion,
        "api_write": degraded.api_write,
        "external_ingestion": degraded.external_ingestion,
        "autonomous_authority": degraded.autonomous_authority,
    },
}
print(json.dumps(payload, indent=2))