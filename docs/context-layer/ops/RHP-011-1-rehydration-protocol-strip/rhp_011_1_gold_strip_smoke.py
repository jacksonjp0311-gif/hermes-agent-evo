from __future__ import annotations
import json
import os
import sys
from pathlib import Path

root = Path(r"C:\Users\jacks\OneDrive\Desktop\hermes-agent-evo")
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
os.chdir(root)

os.environ["HERMES_RHP_BOOT_PREFLIGHT_STATUS"] = "ok"
os.environ["HERMES_RHP_OPERATOR_STATUS"] = "\n".join([
    "RHP rehydration sequence:",
    "[OK] repo root found",
    "[OK] RHP-010 evidence green",
    "[OK] HRCN boundary green",
    "[OK] alignment guard green",
    "[OK] startup packet created",
    "[OK] authority=false",
    "[OK] external_ingestion=false",
    "[OK] provider/model/tool execution=false",
    "[OK] CMS/memory/API write=false",
    "RHP rehydration complete: ok | phase=pre-interaction | evidence=RHP-010",
])

from hermes_cli.banner import _rhp_rehydration_protocol_lines

joined = "\n".join(_rhp_rehydration_protocol_lines())
required = [
    "Rehydration Protocol",
    "verified",
    "phase=pre-interaction",
    "authority=false",
    "repo ok",
    "evidence ok",
    "HRCN ok",
    "alignment ok",
    "startup ok",
    "#7DF9FF",
    "#B388FF",
]
for item in required:
    assert item in joined, (item, joined)

print(json.dumps({
    "ok": True,
    "rehydration_protocol_strip_passed": True,
    "gold_interface_strip_smoke_passed": True,
    "rendered_markup": joined,
}, indent=2))