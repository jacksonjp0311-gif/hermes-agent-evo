from __future__ import annotations
import json
import os
import sys
from pathlib import Path

root = Path(r"C:\Users\jacks\OneDrive\Desktop\hermes-agent-evo")
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
os.chdir(root)

main = (root / "hermes_cli" / "main.py").read_text(encoding="utf-8", errors="replace")
banner = (root / "hermes_cli" / "banner.py").read_text(encoding="utf-8", errors="replace")

checks = {
    "main_evidence_rhp012": 'evidence="RHP-012"' in main and "evidence=RHP-012" in main,
    "main_no_stale_evidence_rhp010": "evidence=RHP-010" not in main and 'evidence="RHP-010"' not in main,
    "protocol_strip_env_present": "HERMES_RHP_PROTOCOL_STRIP" in main,
    "protocol_locks_env_present": "HERMES_RHP_PROTOCOL_LOCKS" in main,
    "boot_packet_v03": "RHP-BOOT-PREFLIGHT-PACKET-v0.3" in main,
    "banner_evidence_rhp012": 'evidence = "RHP-012"' in banner,
    "banner_degraded_supported": '{"blocked", "error", "degraded"}' in banner,
}
payload = {"ok": all(checks.values()), "checks": checks}
print(json.dumps(payload, indent=2))
assert payload["ok"], payload