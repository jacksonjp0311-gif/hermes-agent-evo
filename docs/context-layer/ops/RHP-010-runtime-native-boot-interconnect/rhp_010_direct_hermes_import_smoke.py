from pathlib import Path
import json
import os
import sys

root = Path(__file__).resolve().parents[4]
root_str = str(root)
if root_str not in sys.path:
    sys.path.insert(0, root_str)
os.chdir(root)

os.environ["HERMES_RHP_NATIVE_BOOT"] = "1"
os.environ["HERMES_RHP_BOOT_BANNER"] = "0"
os.environ["HERMES_RHP_BOOT_QUIET"] = "1"

import hermes_cli.main  # noqa: F401

result = {
    "ok": True,
    "runner": "direct_hermes_cli_main_import_smoke",
    "native_boot_status": os.environ.get("HERMES_RHP_BOOT_PREFLIGHT_STATUS"),
    "boot_preflight_gate": os.environ.get("HERMES_RHP_BOOT_PREFLIGHT"),
    "rhp_context_gate": os.environ.get("HERMES_RHP_CONTEXT"),
    "hrcn_context_gate": os.environ.get("HERMES_HRCN_CONTEXT"),
    "packet": os.environ.get("HERMES_RHP_BOOT_PREFLIGHT_PACKET"),
}
assert result["native_boot_status"] == "ok", result
assert result["boot_preflight_gate"] == "preflight", result
assert result["rhp_context_gate"] == "proposal", result
assert result["hrcn_context_gate"] == "proposal", result
print(json.dumps(result, indent=2))