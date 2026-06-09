from __future__ import annotations

import json
import os
from pathlib import Path

root = Path(r"C:\Users\jacks\OneDrive\Desktop\hermes-agent-evo")
cli_path = root / "cli.py"
source = cli_path.read_text(encoding="utf-8", errors="replace")

os.environ["HERMES_RHP_PROTOCOL_STRIP"] = "Rehydration Protocol - verified - phase=pre-interaction - evidence=RHP-012 - authority=false"
os.environ["HERMES_RHP_PROTOCOL_LOCKS"] = "locks: repo ok - evidence ok - HRCN ok - alignment ok - startup ok"

start = source.index("def _build_compact_banner() -> str:")
end = source.index("# ============================================================================", start)
chunk = source[start:end]

ns = {}
import os as _os
import shutil as _shutil
ns["os"] = _os
ns["shutil"] = _shutil
ns["format_banner_version_label"] = lambda: "Hermes Agent vTEST (RHP-012.2)"
exec(chunk, ns)
banner = ns["_build_compact_banner"]()

checks = {
    "contains_rehydration_protocol": "Rehydration Protocol" in banner,
    "contains_evidence_rhp012": "evidence=RHP-012" in banner,
    "contains_locks": "locks: repo ok" in banner,
    "contains_gold_banner_title": "NOUS HERMES" in banner or "AI Agent Framework" in banner,
    "contains_box_border": "╔" in banner and "╚" in banner,
    "source_has_rhp_box_lines": "rhp_box_lines" in source,
}
payload = {
    "ok": all(checks.values()),
    "checks": checks,
    "rendered_banner_excerpt": banner[:1200],
}
print(json.dumps(payload, indent=2))
assert payload["ok"], payload