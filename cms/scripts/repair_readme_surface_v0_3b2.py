from __future__ import annotations

from pathlib import Path
import re

ROOT = Path.cwd()
VERSION = "v0.3b2"
CHECKPOINT = "CMS-SA v0.3b2 - Multi-Level Geometric Alignment Feedback Lock"
PREVIOUS = "CMS-SA v0.3b1a - Surface Alignment Repair and File-Run Guard"

readme_path = ROOT / "README.md"
text = readme_path.read_text(encoding="utf-8", errors="replace")

text = re.sub(r"CMS--SA-v0\.3b1a-blue|CMS--SA-v0\.3b1-blue|CMS--SA-v0\.3b-blue", "CMS--SA-v0.3b2-blue", text)
text = re.sub(r"Current checkpoint: \*\*CMS-SA v0\.3b1a .*?\*\*", f"Current checkpoint: **{CHECKPOINT}**", text)
text = re.sub(r"Current checkpoint: \*\*CMS-SA v0\.3b1 .*?\*\*", f"Current checkpoint: **{CHECKPOINT}**", text)
text = re.sub(r"Previous seal: \*\*CMS-SA v0\.3b1a .*?\*\*", f"Previous seal: **{PREVIOUS}**", text)
text = re.sub(r"\|\s*Current checkpoint\s*\|\s*CMS-SA v0\.3b1a\s*\|", "| Current checkpoint | CMS-SA v0.3b2 |", text)
text = re.sub(r"\|\s*Previous seal\s*\|\s*CMS-SA v0\.3b1\s*\|", "| Previous seal | CMS-SA v0.3b1a |", text)
text = re.sub(r"CMS-RCC-N-v0\.3b1a / 180 days", "CMS-RCC-N-v0.3b2 / 180 days", text)

def ensure_after(anchor: str, row: str) -> None:
    global text
    if row in text:
        return
    if anchor in text:
        text = text.replace(anchor, anchor + "\n" + row, 1)
    else:
        text += "\n" + row + "\n"

def ensure_section(block: str) -> None:
    global text
    title = block.splitlines()[0]
    if title not in text:
        text += "\n\n" + block.rstrip() + "\n"

ensure_after("| v0.3b1a Surface Alignment Repair | Does section-level README, mini README, validator, report, and registry alignment hold? | `reports/surface_alignment/latest_surface_alignment_report.md` |",
             "| v0.3b2 Multi-Level Geometric Alignment | Do feedback items bind to geometry, validators, evidence, routes, registry, and public surfaces? | `reports/alignment/latest_multilevel_alignment_report.md` |")

ensure_after("| Surface alignment report | `reports/surface_alignment/latest_surface_alignment_report.md` |",
             "| Multi-level alignment report | `outputs/alignment/latest_multilevel_alignment_report.json` |")
ensure_after("| Multi-level alignment report | `outputs/alignment/latest_multilevel_alignment_report.json` |",
             "| Multi-level alignment validation | `reports/alignment/latest_multilevel_alignment_validation.md` |")

for command in [
    "python scripts/alignment/emit_multilevel_alignment_v0_3b2.py",
    "python scripts/validation/validate_multilevel_alignment_v0_3b2.py",
    "python scripts/validation/validate_surface_alignment_v0_3b2.py",
]:
    if command not in text:
        text = text.replace("python scripts/validation/validate_surface_alignment_v0_3b1a.py", "python scripts/validation/validate_surface_alignment_v0_3b1a.py\n" + command, 1)

ensure_after("| Feedback lifecycle | Typed feedback items, scoring, classification, downgrade paths, lifecycle reports | `configs/feedback/`, `src/cms/feedback/`, `scripts/feedback/`, `outputs/feedback/`, `reports/feedback/` |",
             "| Multi-level alignment | Binds README, mini READMEs, route maps, validators, reports, geometry, feedback, registry, public sync, and release state | `configs/alignment/`, `src/cms/alignment/`, `scripts/alignment/`, `outputs/alignment/`, `reports/alignment/` |")

ensure_after("| `reports/surface_alignment/latest_surface_alignment_report.md` | Current root/mini README alignment report |",
             "| `reports/alignment/latest_multilevel_alignment_report.md` | Current multi-level geometric feedback alignment report |")
ensure_after("| `reports/alignment/latest_multilevel_alignment_report.md` | Current multi-level geometric feedback alignment report |",
             "| `reports/alignment/latest_multilevel_alignment_validation.md` | Current multi-level alignment validation |")

dir_rows = [
"| `configs/alignment/` | Multi-level alignment contracts for runtime coherence. |",
"| `src/cms/alignment/` | Multi-level alignment runtime. |",
"| `scripts/alignment/` | Multi-level alignment emitters separated from validators. |",
"| `outputs/alignment/` | Latest machine-readable multi-level alignment reports. |",
"| `reports/alignment/` | Multi-level alignment reports and validation outputs. |",
]
for row in dir_rows:
    if row not in text:
        anchor = "| `reports/surface_alignment/` | Root README and mini README alignment validation reports. |"
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + row, 1)
        else:
            text += "\n" + row + "\n"

ensure_after("| Feedback lifecycle patch | `configs/feedback/`, `src/cms/feedback/`, `scripts/feedback/`, feedback mini READMEs | feedback lifecycle validation + README audit + surface alignment |",
             "| Multi-level alignment patch | `configs/alignment/`, `src/cms/alignment/`, `scripts/alignment/`, alignment mini READMEs | multi-level alignment validation + geometry + feedback + surface alignment |")

lesson = "| CMS-L-019 | Feedback lifecycle and reflective Git geometry existed as adjacent surfaces but were not yet bound into one runtime alignment check. | Geometry, feedback, README, mini READMEs, reports, registry, route maps, and release state could each pass locally without proving cross-surface binding. | No feedback item is valid unless it can be located in repository geometry and tied to evidence, validators, and current public surfaces. |"
if "CMS-L-019" not in text:
    text = text.replace("| CMS-L-018 | v0.3b1 alignment repair was pasted line-by-line and the expected version token self-mutated to v0.3b11 while section rows drifted. | The script was not run as a file, regex replacement was not idempotent, and section-level currentness was not fully normalized before validation. | Alignment repair scripts must be file-run, version-token updates must be idempotent, and stale root/mini README surfaces must fail surface alignment before release. |",
                        "| CMS-L-018 | v0.3b1 alignment repair was pasted line-by-line and the expected version token self-mutated to v0.3b11 while section rows drifted. | The script was not run as a file, regex replacement was not idempotent, and section-level currentness was not fully normalized before validation. | Alignment repair scripts must be file-run, version-token updates must be idempotent, and stale root/mini README surfaces must fail surface alignment before release. |\n" + lesson)

section = """## CMS-SA v0.3b2 - Multi-Level Geometric Alignment Feedback Lock

v0.3b2 keeps API inactive and strengthens the core/runtime by binding root README, mini READMEs, route maps, validators, reports, reflective Git geometry, feedback lifecycle, version registry, public sync, and release state into one internal alignment surface.

Core rule:

```text
No feedback item is valid unless it can be located in repository geometry and tied to evidence, validators, and current public surfaces.
```

API remains inactive. This layer is internal runtime coherence only.

Non-claim lock: multi-level alignment improves repository-bound cybernetic runtime coherence. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
"""
ensure_section(section)

readme_path.write_text(text, encoding="utf-8")

# Patch audit/render validators to current checkpoint.
for rel in ["scripts/rcc/audit_readme_surface.py", "scripts/validation/validate_readme_render_hygiene_v0_2b2.py"]:
    path = ROOT / rel
    if path.exists():
        s = path.read_text(encoding="utf-8", errors="replace")
        s = s.replace("v0.3b11", "v0.3b2")
        s = s.replace("v0.3b1a", "v0.3b2")
        s = s.replace("v0.3b1", "v0.3b2")
        s = s.replace("CMS--SA-v0.3b11", "CMS--SA-v0.3b2")
        s = s.replace("CMS--SA-v0.3b1a", "CMS--SA-v0.3b2")
        s = s.replace("CMS--SA-v0.3b1", "CMS--SA-v0.3b2")
        s = s.replace("CMS-SA v0.3b1a", "CMS-SA v0.3b2")
        s = s.replace("CMS-SA v0.3b1", "CMS-SA v0.3b2")
        path.write_text(s, encoding="utf-8")