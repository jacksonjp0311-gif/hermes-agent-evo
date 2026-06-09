from __future__ import annotations
import json
from pathlib import Path

root = Path(r"C:\Users\jacks\OneDrive\Desktop\hermes-agent-evo")
readme_path = root / "README.md"
rhp_readme_path = root / "rhp" / "README.md"

readme = readme_path.read_text(encoding="utf-8", errors="replace")
rhp_readme = rhp_readme_path.read_text(encoding="utf-8", errors="replace")

original_readme = readme
original_rhp = rhp_readme

def repl_all(text: str, old: str, new: str) -> str:
    return text.replace(old, new)

# Current public metrics.
readme = repl_all(readme, "| Latest RHP proof | `docs/context-layer/ops/RHP-011-1-final-evidence.json` |", "| Latest RHP proof | `docs/context-layer/ops/RHP-011-2-final-evidence.json` |")
readme = repl_all(readme, "| Current RHP status | `RHP-011.1 gold interface Rehydration Protocol strip passed` |", "| Current RHP status | `RHP-011.2 README geometry and evidence hygiene closure passed` |")
readme = repl_all(readme, "| Next RHP gate | `RHP-012 safe boot failure mode and degraded startup status` |", "| Next RHP gate | `RHP-012 safe boot failure mode and degraded startup status` |")

# RHP activation and post-seal chart normalization.
readme = repl_all(
    readme,
    "| RHP-010 | Runtime-native boot interconnect. | passed |\n| RHP-011 | Operator-visible startup lock sequence. | passed |\n| RHP-012 | Safe boot failure mode and degraded startup status. | next |",
    "| RHP-010 | Runtime-native boot interconnect. | passed |\n| RHP-011 | Operator-visible startup lock sequence. | passed |\n| RHP-011.1 | Gold interface Rehydration Protocol strip. | passed |\n| RHP-011.2 | README geometry and evidence hygiene closure. | passed |\n| RHP-012 | Safe boot failure mode and degraded startup status. | next |",
)
readme = repl_all(
    readme,
    "| RHP-010 | Runtime-native boot interconnect. | passed |\n| next | RHP-011 installed launcher smoke and operator-visible startup status. | next |",
    "| RHP-010 | Runtime-native boot interconnect. | passed |\n| RHP-011 | Installed launcher smoke and operator-visible startup status. | passed |\n| RHP-011.1 | Gold interface Rehydration Protocol strip. | passed |\n| RHP-011.2 | README geometry and evidence hygiene closure. | passed |\n| next | RHP-012 safe boot failure mode and degraded startup status. | next |",
)
readme = repl_all(
    readme,
    "| RHP-010 | Runtime-native boot interconnect. | passed |\n| RHP-011 | Installed launcher smoke and operator-visible startup status. | next |",
    "| RHP-010 | Runtime-native boot interconnect. | passed |\n| RHP-011 | Installed launcher smoke and operator-visible startup status. | passed |\n| RHP-011.1 | Gold interface Rehydration Protocol strip. | passed |\n| RHP-011.2 | README geometry and evidence hygiene closure. | passed |\n| RHP-012 | Safe boot failure mode and degraded startup status. | next |",
)

# Narrative drift.
readme = repl_all(readme, "RHP is the active runtime-threshold track and is current through RHP-010.", "RHP is the active runtime-threshold track and is current through RHP-011.2.")
readme = repl_all(readme, "HRCN v2.0 + OPS-027 + RHP-010 = read-only runtime-native boot orientation through direct Hermes executable startup.", "HRCN v2.0 + OPS-027 + RHP-011.2 = read-only runtime-native boot orientation with persistent Rehydration Protocol visibility through direct Hermes executable startup.")
readme = repl_all(readme, "| Next gate | `RHP-011 installed launcher smoke and operator-visible startup status` |", "| Next gate | `RHP-012 safe boot failure mode and degraded startup status` |")
readme = repl_all(readme, "AI lock: No future AI thread may claim runtime authority, CMS write authority, memory write authority, API write authority, autonomous authority, production readiness, sentience, consciousness, AGI, ASI, or self-authorization from OPS-027/RHP-010.", "AI lock: No future AI thread may claim runtime authority, CMS write authority, memory write authority, API write authority, autonomous authority, production readiness, sentience, consciousness, AGI, ASI, or self-authorization from OPS-027/RHP-011.2.")

# Add failure-learning lessons if absent.
lesson_block = """| RHP-L-034 | Managed-region replacement must use marker-safe or regex-safe block replacement; PowerShell Split is not safe for source surgery. |
| RHP-L-035 | Never commit raw broken-file debug captures unless they pass the same credential/trigger scan; prefer sanitized failure summaries. |
| RHP-L-036 | Every All-One, smoke, repair, and seal script must include progress telemetry with percent, branch, command, output, timeout, and copy-back failure block. |
| RHP-L-037 | Large generated scripts must run as files with `powershell.exe -NoProfile -ExecutionPolicy Bypass -File`, not as pasted interactive bodies. |
| RHP-L-038 | PowerShell script runners must avoid `$Args` / `$args` parameter names because they collide with automatic variables and can erase argv surfaces. |
| RHP-L-039 | Pytest absence is not a failing gate unless pytest is declared as a repo dependency; use focused direct smoke as the governed fallback. |
| RHP-L-040 | External command runners must print `argv_count`, command, output path, and timeout before execution. |
| RHP-L-041 | Scratch proof files must be either intentionally tracked or cleaned before the next RHP gate. |"""
if "RHP-L-036" not in readme:
    readme = repl_all(
        readme,
        "| RHP-L-033 | When encoded banner text survives exact-string replacement, replace the whole managed hook region from markers instead of patching a single line. |",
        "| RHP-L-033 | When encoded banner text survives exact-string replacement, replace the whole managed hook region from markers instead of patching a single line. |\n" + lesson_block,
    )

# Add concise RHP-011.2 note.
closure_note = """
#### RHP-011.2 Geometry Closure

RHP-011.2 closes README geometry and evidence hygiene after the RHP-011.1 gold-interface Rehydration Protocol phase transition.

```text
RHP-011.1 made the runtime truth visible.
RHP-011.2 makes the repository truth agree everywhere.
```

Boundary: documentation/evidence alignment only. No provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.
"""
if "#### RHP-011.2 Geometry Closure" not in readme:
    marker = "<!-- HERMES_RHP_RUNTIME_ACTIVATION_END -->"
    readme = readme.replace(marker, closure_note + "\n" + marker)

# RHP README closure.
if "RHP-011.2 README geometry and evidence hygiene closure" not in rhp_readme:
    rhp_readme += """

## RHP-011.2 README geometry and evidence hygiene closure

RHP-011.2 aligns the root README, RHP README, alignment guard, public metrics, RHP activation chart, post-seal chart, failure-learning locks, and evidence hygiene after RHP-011.1.

Current runtime-visible strip remains RHP-011.1. Current repository evidence closure is RHP-011.2.

Non-claim lock: RHP-011.2 is documentation/evidence hygiene only. It does not grant provider/model/tool authority, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.
"""

readme_path.write_text(readme, encoding="utf-8")
rhp_readme_path.write_text(rhp_readme, encoding="utf-8")

report = {
    "ok": True,
    "readme_changed": readme != original_readme,
    "rhp_readme_changed": rhp_readme != original_rhp,
    "rhp_011_2_note_present": "RHP-011.2 Geometry Closure" in readme,
    "progress_telemetry_lessons_present": all(f"RHP-L-0{n}" in readme for n in range(36, 42)),
    "latest_rhp_proof_present": "docs/context-layer/ops/RHP-011-2-final-evidence.json" in readme,
    "current_status_present": "RHP-011.2 README geometry and evidence hygiene closure passed" in readme,
}
print(json.dumps(report, indent=2))