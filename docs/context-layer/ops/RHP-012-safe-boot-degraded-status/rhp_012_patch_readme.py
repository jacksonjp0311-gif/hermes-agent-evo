from __future__ import annotations
import json
from pathlib import Path

root = Path(r"C:\Users\jacks\OneDrive\Desktop\hermes-agent-evo")
readme_path = root / "README.md"
rhp_readme_path = root / "rhp" / "README.md"
readme = readme_path.read_text(encoding="utf-8", errors="replace")
rhp = rhp_readme_path.read_text(encoding="utf-8", errors="replace")
orig_readme = readme
orig_rhp = rhp

readme = readme.replace("| Latest RHP proof | `docs/context-layer/ops/RHP-011-2-final-evidence.json` |", "| Latest RHP proof | `docs/context-layer/ops/RHP-012-final-evidence.json` |")
readme = readme.replace("| Current RHP status | `RHP-011.2 README geometry and evidence hygiene closure passed` |", "| Current RHP status | `RHP-012 safe boot failure mode and degraded startup status passed` |")
readme = readme.replace("| Next RHP gate | `RHP-012 safe boot failure mode and degraded startup status` |", "| Next RHP gate | `RHP-013 operator dashboard and status packet normalization` |")
readme = readme.replace("| RHP-012 | Safe boot failure mode and degraded startup status. | next |", "| RHP-012 | Safe boot failure mode and degraded startup status. | passed |\n| RHP-013 | Operator dashboard and status packet normalization. | next |")
readme = readme.replace("RHP is the active runtime-threshold track and is current through RHP-011.2.", "RHP is the active runtime-threshold track and is current through RHP-012.")
readme = readme.replace("HRCN v2.0 + OPS-027 + RHP-011.2 = read-only runtime-native boot orientation with persistent Rehydration Protocol visibility through direct Hermes executable startup.", "HRCN v2.0 + OPS-027 + RHP-012 = read-only runtime-native boot orientation with persistent Rehydration Protocol visibility and safe degraded startup status through direct Hermes executable startup.")
readme = readme.replace("| Next gate | `RHP-012 safe boot failure mode and degraded startup status` |", "| Next gate | `RHP-013 operator dashboard and status packet normalization` |")
readme = readme.replace("AI lock: No future AI thread may claim runtime authority, CMS write authority, memory write authority, API write authority, autonomous authority, production readiness, sentience, consciousness, AGI, ASI, or self-authorization from OPS-027/RHP-011.2.", "AI lock: No future AI thread may claim runtime authority, CMS write authority, memory write authority, API write authority, autonomous authority, production readiness, sentience, consciousness, AGI, ASI, or self-authorization from OPS-027/RHP-012.")

if "RHP-L-042" not in readme:
    readme = readme.replace(
        "| RHP-L-041 | Scratch proof files must be either intentionally tracked or cleaned before the next RHP gate. |",
        "| RHP-L-041 | Scratch proof files must be either intentionally tracked or cleaned before the next RHP gate. |\n| RHP-L-042 | Missing or invalid evidence must produce degraded visible startup status, not a crash, false-green state, or authority expansion. |\n| RHP-L-043 | Safe boot negative controls must prove authority remains false while status degrades. |",
    )

note = """
#### RHP-012 Safe Boot Degraded Status

RHP-012 adds safe degraded startup status. Missing or invalid evidence, failed alignment, or unavailable boundary evidence must render visibly degraded startup state without granting authority.

```text
green evidence -> verified startup
missing evidence -> degraded startup
degraded startup -> authority remains false
```

Boundary: startup safety/status only. No provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.
"""
if "#### RHP-012 Safe Boot Degraded Status" not in readme:
    readme = readme.replace("<!-- HERMES_RHP_RUNTIME_ACTIVATION_END -->", note + "\n<!-- HERMES_RHP_RUNTIME_ACTIVATION_END -->")

if "RHP-012 safe boot failure mode and degraded startup status" not in rhp:
    rhp += """

## RHP-012 safe boot failure mode and degraded startup status

RHP-012 ensures missing or invalid local evidence produces a visible degraded startup state instead of a crash, false-green state, or authority expansion.

Runtime boundary: degraded startup status remains read-only. It does not grant provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.
"""

readme_path.write_text(readme, encoding="utf-8")
rhp_readme_path.write_text(rhp, encoding="utf-8")
print(json.dumps({
    "ok": True,
    "readme_changed": readme != orig_readme,
    "rhp_readme_changed": rhp != orig_rhp,
    "rhp012_status_present": "RHP-012 safe boot failure mode and degraded startup status passed" in readme,
    "rhp013_next_present": "RHP-013 operator dashboard and status packet normalization" in readme,
    "lessons_042_043_present": "RHP-L-042" in readme and "RHP-L-043" in readme,
}, indent=2))