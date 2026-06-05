from __future__ import annotations

from pathlib import Path
import re

ROOT = Path.cwd()
README = ROOT / "README.md"
text = README.read_text(encoding="utf-8", errors="replace")

VERSION = "v0.3b1a"
CHECKPOINT = "CMS-SA v0.3b1a - Surface Alignment Repair and File-Run Guard"
PREVIOUS = "CMS-SA v0.3b1 - README and Mini README Reflective Feedback Alignment Lock"

# Version/header normalization.
text = re.sub(r"CMS--SA-v0\.3b11-blue|CMS--SA-v0\.3b1-blue|CMS--SA-v0\.3b-blue", "CMS--SA-v0.3b1a-blue", text)
text = re.sub(r"Current checkpoint: \*\*CMS-SA v0\.3b1 .*?\*\*", f"Current checkpoint: **{CHECKPOINT}**", text)
text = re.sub(r"Current checkpoint: \*\*CMS-SA v0\.3b - Feedback Quality and Lifecycle Engine\*\*", f"Current checkpoint: **{CHECKPOINT}**", text)
text = re.sub(r"Previous seal: \*\*CMS-SA v0\.2b3 .*?\*\*", f"Previous seal: **{PREVIOUS}**", text)
text = re.sub(r"Previous seal: \*\*CMS-SA v0\.3b - Feedback Quality and Lifecycle Engine\*\*", f"Previous seal: **{PREVIOUS}**", text)
text = re.sub(r"\|\s*Current checkpoint\s*\|\s*CMS-SA v0\.3b1\s*\|", "| Current checkpoint | CMS-SA v0.3b1a |", text)
text = re.sub(r"\|\s*Current checkpoint\s*\|\s*CMS-SA v0\.3b\s*\|", "| Current checkpoint | CMS-SA v0.3b1a |", text)
text = re.sub(r"\|\s*Previous seal\s*\|\s*CMS-SA v0\.3b\s*\|", "| Previous seal | CMS-SA v0.3b1 |", text)
text = re.sub(r"\|\s*Previous seal\s*\|\s*CMS-SA v0\.3a2\s*\|", "| Previous seal | CMS-SA v0.3b1 |", text)
text = text.replace("|Current checkpoint | CMS-SA v0.3b1 |", "| Current checkpoint | CMS-SA v0.3b1a |")

# RCC echo location.
text = re.sub(r"CMS-RCC-N-v0\.3a1 / 180 days|CMS-RCC-N-v0\.3b1 / 180 days", "CMS-RCC-N-v0.3b1a / 180 days", text)

def ensure_after(anchor: str, row: str) -> None:
    global text
    if row in text:
        return
    if anchor in text:
        text = text.replace(anchor, anchor + "\n" + row, 1)
    else:
        text += "\n" + row + "\n"

def ensure_before_heading(heading: str, block: str) -> None:
    global text
    if block.strip() in text:
        return
    if heading in text:
        text = text.replace(heading, block.rstrip() + "\n\n" + heading, 1)
    else:
        text += "\n\n" + block.rstrip() + "\n"

# Current snapshot rows.
ensure_after("| v0.2b3a Validator Repair | Does Markdown structure validation avoid false positives on data rows? | `reports/markdown_structure/latest_markdown_structure.md` |",
             "| v0.3a Reflective Git Geometry | Can Git commits be interpreted as routed geometry events? | `reports/geometry/latest_reflective_git_geometry.md` |")
ensure_after("| v0.3a Reflective Git Geometry | Can Git commits be interpreted as routed geometry events? | `reports/geometry/latest_reflective_git_geometry.md` |",
             "| v0.3a2 Pure Geometry Validation Boundary | Can geometry be emitted intentionally and validated read-only? | `reports/geometry/latest_reflective_git_geometry_validation.md` |")
ensure_after("| v0.3a2 Pure Geometry Validation Boundary | Can geometry be emitted intentionally and validated read-only? | `reports/geometry/latest_reflective_git_geometry_validation.md` |",
             "| v0.3b Feedback Lifecycle Engine | Can findings become typed, scored, downgrade-safe feedback objects? | `reports/feedback/latest_feedback_lifecycle_report.md` |")
ensure_after("| v0.3b Feedback Lifecycle Engine | Can findings become typed, scored, downgrade-safe feedback objects? | `reports/feedback/latest_feedback_lifecycle_report.md` |",
             "| v0.3b1a Surface Alignment Repair | Does section-level README, mini README, validator, report, and registry alignment hold? | `reports/surface_alignment/latest_surface_alignment_report.md` |")

# Current metrics rows.
ensure_after("| Geometry validation report | `reports/geometry/latest_reflective_git_geometry_validation.md` |",
             "| Latest feedback lifecycle report | `outputs/feedback/latest_feedback_lifecycle_report.json` |")
ensure_after("| Latest feedback lifecycle report | `outputs/feedback/latest_feedback_lifecycle_report.json` |",
             "| Feedback validation report | `reports/feedback/latest_feedback_lifecycle_validation.md` |")
ensure_after("| Feedback validation report | `reports/feedback/latest_feedback_lifecycle_validation.md` |",
             "| Surface alignment report | `reports/surface_alignment/latest_surface_alignment_report.md` |")

# Quick Start / pre-push commands.
ensure_before_heading("python -m cms cycle --repo . --profile CMS-Core",
"""python scripts/feedback/emit_feedback_lifecycle_v0_3b.py
python scripts/validation/validate_feedback_lifecycle_v0_3b.py
python scripts/validation/validate_surface_alignment_v0_3b1a.py""")

# Repository layers.
ensure_after("| Reflection and process rules | Bounded process lessons, Law of Sufficient Form, badge/status discipline | `docs/reflection/`, `docs/process/` |",
             "| Reflective geometry | Git route geometry, geometry emission, read-only validation | `configs/geometry/`, `src/cms/geometry/`, `scripts/geometry/`, `outputs/geometry/`, `reports/geometry/` |")
ensure_after("| Reflective geometry | Git route geometry, geometry emission, read-only validation | `configs/geometry/`, `src/cms/geometry/`, `scripts/geometry/`, `outputs/geometry/`, `reports/geometry/` |",
             "| Feedback lifecycle | Typed feedback items, scoring, classification, downgrade paths, lifecycle reports | `configs/feedback/`, `src/cms/feedback/`, `scripts/feedback/`, `outputs/feedback/`, `reports/feedback/` |")

# Historical archive rows.
ensure_after("| `reports/release/latest_release_readiness.md` | Current release readiness report |",
             "| `reports/geometry/latest_reflective_git_geometry.md` | Current reflective Git geometry report |")
ensure_after("| `reports/geometry/latest_reflective_git_geometry.md` | Current reflective Git geometry report |",
             "| `reports/geometry/latest_reflective_git_geometry_validation.md` | Current reflective Git geometry validation |")
ensure_after("| `reports/geometry/latest_reflective_git_geometry_validation.md` | Current reflective Git geometry validation |",
             "| `reports/feedback/latest_feedback_lifecycle_report.md` | Current feedback lifecycle report |")
ensure_after("| `reports/feedback/latest_feedback_lifecycle_report.md` | Current feedback lifecycle report |",
             "| `reports/feedback/latest_feedback_lifecycle_validation.md` | Current feedback lifecycle validation |")
ensure_after("| `reports/feedback/latest_feedback_lifecycle_validation.md` | Current feedback lifecycle validation |",
             "| `reports/surface_alignment/latest_surface_alignment_report.md` | Current root/mini README alignment report |")

# Evidence artifact code fences: append missing surfaces in text form if necessary.
if "outputs/feedback/" not in text:
    text = text.replace("outputs/evidence/", "outputs/evidence/\noutputs/feedback/", 1)
if "reports/feedback/" not in text:
    text = text.replace("reports/release/", "reports/release/\nreports/feedback/\nreports/surface_alignment/", 1)

# Primary nexus files.
ensure_after("| `scripts/validation/validate_public_sync_v0_2b3.py` | Local/origin/version registry sync validator. |",
             "| `scripts/feedback/emit_feedback_lifecycle_v0_3b.py` | Feedback lifecycle emitter. |")
ensure_after("| `scripts/feedback/emit_feedback_lifecycle_v0_3b.py` | Feedback lifecycle emitter. |",
             "| `scripts/validation/validate_feedback_lifecycle_v0_3b.py` | Feedback lifecycle validator. |")
ensure_after("| `scripts/validation/validate_feedback_lifecycle_v0_3b.py` | Feedback lifecycle validator. |",
             "| `scripts/validation/validate_surface_alignment_v0_3b1a.py` | Root and mini README alignment validator. |")

# Patch routing matrix.
ensure_after("| Release/docs patch | `docs/`, `reports/release/`, version registry | release validation + README audit |",
             "| Feedback lifecycle patch | `configs/feedback/`, `src/cms/feedback/`, `scripts/feedback/`, feedback mini READMEs | feedback lifecycle validation + README audit + surface alignment |")

# Pre-API framing.
text = text.replace("## Two-Way API Transmission Readiness Box", "## Pre-API Transmission Constraint Box")
pre_api_sentence = "API is not active in v0.3b1a. API work begins only after multi-level geometric alignment confirms root README, mini READMEs, route maps, validators, reports, geometry, feedback lifecycle, and release surfaces agree."
if pre_api_sentence not in text:
    text = text.replace("CMS is preparing for an eventual two-way API transmission process:", "CMS is preparing for an eventual two-way API transmission process.\n\n" + pre_api_sentence)

# Alignment rules.
ensure_after("| Boundary rule | Process alignment is repository hygiene. It is not code correctness, external validation, AGI, consciousness, security, or production readiness. |",
             "| Stale-section lock rule | If root README sections, mini README surfaces, version registry, and validation reports disagree, surface alignment must fail. |")

# Full Directory Box durable rows.
dir_rows = [
"| `configs/feedback/` | Feedback lifecycle contracts and promotion/downgrade rules. |",
"| `schemas/` | JSON schemas for geometry nodes, feedback items, and future typed CMS exchange objects. |",
"| `scripts/geometry/` | Reflective geometry emitters separated from read-only validators. |",
"| `scripts/feedback/` | Feedback lifecycle emitters separated from validators. |",
"| `outputs/geometry/` | Latest reflective Git geometry outputs. |",
"| `outputs/feedback/` | Latest typed feedback lifecycle reports. |",
"| `reports/geometry/` | Reflective Git geometry reports and validation outputs. |",
"| `reports/feedback/` | Feedback lifecycle reports and validation outputs. |",
"| `reports/surface_alignment/` | Root README and mini README alignment validation reports. |",
]
for row in dir_rows:
    if row not in text:
        # Place before first runtime observation report row if possible.
        anchor = "| `reports/runtime_observation/` | Human-readable and JSON runtime observation reports. |"
        if anchor in text:
            text = text.replace(anchor, row + "\n" + anchor, 1)
        else:
            text += "\n" + row + "\n"

# Ensure rows that previous mutation broke exist.
required_existing_rows = [
"| `outputs/evidence/` | Latest evidence packages emitted by the runtime. |",
"| `reports/release/` | Release readiness reports and checkpoint validation outputs. |",
]
for row in required_existing_rows:
    if row not in text:
        anchor = "| `outputs/drift/` | Latest CMS drift reports and K/D coherence measures. |"
        if "outputs/evidence" in row and anchor in text:
            text = text.replace(anchor, anchor + "\n" + row, 1)
        else:
            anchor2 = "| `reports/public_sync/` | Public sync validation reports. |"
            if anchor2 in text:
                text = text.replace(anchor2, anchor2 + "\n" + row, 1)
            else:
                text += "\n" + row + "\n"

# Lesson.
lesson = "| CMS-L-018 | v0.3b1 alignment repair was pasted line-by-line and the expected version token self-mutated to v0.3b11 while section rows drifted. | The script was not run as a file, regex replacement was not idempotent, and section-level currentness was not fully normalized before validation. | Alignment repair scripts must be file-run, version-token updates must be idempotent, and stale root/mini README surfaces must fail surface alignment before release. |"
if "CMS-L-018" not in text:
    text = text.replace("| CMS-L-017 | v0.3b added feedback lifecycle surfaces while root README sections and mini README surfaces still carried stale or incomplete state. | Existing validators checked badges and broad README anchors but did not enforce section-level currentness across root README, mini READMEs, reports, and registry. | If a version adds a durable surface, root README sections, affected mini READMEs, reports, validators, and version registry must advance together or surface alignment must fail. |",
                        "| CMS-L-017 | v0.3b added feedback lifecycle surfaces while root README sections and mini README surfaces still carried stale or incomplete state. | Existing validators checked badges and broad README anchors but did not enforce section-level currentness across root README, mini READMEs, reports, and registry. | If a version adds a durable surface, root README sections, affected mini READMEs, reports, validators, and version registry must advance together or surface alignment must fail. |\n" + lesson)

section = """## CMS-SA v0.3b1a - Surface Alignment Repair and File-Run Guard

v0.3b1a repairs the v0.3b1 alignment attempt by making version-token checks idempotent, restoring missing README section surfaces, restoring durable directory rows, and keeping API work explicitly inactive.

New rule:

```text
Surface alignment must fail stale sections, but expected version tokens must not self-mutate.
```

Non-claim lock: surface alignment repair improves repository navigation and reflective feedback alignment. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
"""
if "CMS-SA v0.3b1a - Surface Alignment Repair and File-Run Guard" not in text:
    text += "\n\n" + section

README.write_text(text, encoding="utf-8")