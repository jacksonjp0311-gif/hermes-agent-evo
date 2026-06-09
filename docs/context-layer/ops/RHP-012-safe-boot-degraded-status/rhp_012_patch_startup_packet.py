from __future__ import annotations
import json
from pathlib import Path

root = Path(r"C:\Users\jacks\OneDrive\Desktop\hermes-agent-evo")
path = root / "rhp" / "startup_context_packet.py"
text = path.read_text(encoding="utf-8", errors="replace")
original = text

text = text.replace("RHP-STARTUP-CONTEXT-PACKET-v0.3", "RHP-STARTUP-CONTEXT-PACKET-v0.4")
text = text.replace(
    "RHP-011.1 startup packet verifies the installed CLI path can carry read-only boot orientation and the gold-interface Rehydration Protocol strip.",
    "RHP-012 startup packet verifies the installed CLI path can carry safe read-only boot orientation, degraded startup status, and the gold-interface Rehydration Protocol strip."
)
if "degraded" not in text:
    text = text.replace(
        '"boot_preflight_ok": bool(boot.ok),',
        '"boot_preflight_ok": bool(boot.ok),\n        "boot_preflight_degraded": bool(getattr(boot, "degraded", False)),\n        "boot_preflight_degraded_reason": str(getattr(boot, "degraded_reason", "")),'
    )

path.write_text(text, encoding="utf-8")
print(json.dumps({
    "ok": True,
    "changed": text != original,
    "schema_v04_present": "RHP-STARTUP-CONTEXT-PACKET-v0.4" in text,
    "degraded_fields_present": "boot_preflight_degraded" in text,
}, indent=2))