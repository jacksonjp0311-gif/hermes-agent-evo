from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path.cwd()
README = ROOT / "README.md"
text = README.read_text(encoding="utf-8", errors="replace")

VERSION = "v0.3b2a1"
PREVIOUS = "v0.3b2a"
CHECKPOINT = "CMS-SA v0.3b2a1 - README Documentation Coherence Repair"
PREVIOUS_SEAL = "CMS-SA v0.3b2a - README Documentation Coherence Seal"
NEXT_ANCHOR = "CMS-SA v0.3b3 - Runtime Decision Kernel and Replay Ledger"
NOW = "2026-06-02T13:34:23.6082341-04:00"


def sub_literal(pattern: str, replacement: str, source: str) -> str:
    return re.sub(pattern, lambda _m: replacement, source, flags=re.S)


text = re.sub(r"CMS--SA-v0\.3b2[a-zA-Z0-9]*-blue", "CMS--SA-v0.3b2a1-blue", text)
text = re.sub(r"CMS--SA-v0\.3b2-blue", "CMS--SA-v0.3b2a1-blue", text)

text = sub_literal(
    r"Current checkpoint: \*\*CMS-SA v0\.3b2.*?\*\*",
    f"Current checkpoint: **{CHECKPOINT}**",
    text,
)
text = sub_literal(
    r"Previous seal: \*\*CMS-SA v0\.3b.*?\*\*",
    f"Previous seal: **{PREVIOUS_SEAL}**",
    text,
)

text = re.sub(r"\|\s*Current checkpoint\s*\|\s*CMS-SA v0\.3b2[a-zA-Z0-9]*\s*\|", "| Current checkpoint | CMS-SA v0.3b2a1 |", text)
text = re.sub(r"\|\s*Current checkpoint\s*\|\s*CMS-SA v0\.3b2\s*\|", "| Current checkpoint | CMS-SA v0.3b2a1 |", text)
text = re.sub(r"\|\s*Previous seal\s*\|\s*CMS-SA v0\.3b.*?\s*\|", "| Previous seal | CMS-SA v0.3b2a |", text)

text = re.sub(r"CMS-RCC-N-v0\.3b2[a-zA-Z0-9]* / 180 days", "CMS-RCC-N-v0.3b2a1 / 180 days", text)
text = text.replace("CMS-RCC-N-v0.3b2 / 180 days", "CMS-RCC-N-v0.3b2a1 / 180 days")

pairs = [
    ("`outputs/evidence/\noutputs/feedback/latest_evidence_package.json`", "`outputs/evidence/latest_evidence_package.json`"),
    ("`outputs/evidence/\r\noutputs/feedback/latest_evidence_package.json`", "`outputs/evidence/latest_evidence_package.json`"),
    ("`outputs/evidence/\noutputs/feedback/`", "`outputs/evidence/`, `outputs/feedback/`"),
    ("`outputs/evidence/\r\noutputs/feedback/`", "`outputs/evidence/`, `outputs/feedback/`"),
    ("| `outputs/evidence/\noutputs/feedback/` | Latest evidence packages emitted by the runtime. |", "| `outputs/evidence/` | Latest evidence packages emitted by the runtime. |"),
    ("| `outputs/evidence/\r\noutputs/feedback/` | Latest evidence packages emitted by the runtime. |", "| `outputs/evidence/` | Latest evidence packages emitted by the runtime. |"),
    ("`reports/release/\nreports/feedback/\nreports/surface_alignment/latest_release_readiness.md`", "`reports/release/latest_release_readiness.md`"),
    ("`reports/release/\r\nreports/feedback/\r\nreports/surface_alignment/latest_release_readiness.md`", "`reports/release/latest_release_readiness.md`"),
    ("`reports/release/\nreports/feedback/\nreports/surface_alignment/`", "`reports/release/`, `reports/feedback/`, `reports/surface_alignment/`"),
    ("`reports/release/\r\nreports/feedback/\r\nreports/surface_alignment/`", "`reports/release/`, `reports/feedback/`, `reports/surface_alignment/`"),
    ("| `reports/release/\nreports/feedback/\nreports/surface_alignment/` | Release readiness reports and checkpoint validation outputs. |", "| `reports/release/` | Release readiness reports and checkpoint validation outputs. |"),
    ("| `reports/release/\r\nreports/feedback/\r\nreports/surface_alignment/` | Release readiness reports and checkpoint validation outputs. |", "| `reports/release/` | Release readiness reports and checkpoint validation outputs. |"),
]
for old, new in pairs:
    text = text.replace(old, new)

text = text.replace("python scripts/feedback/emit_feedback_lifecycle_v0_3b.py\npython scripts/feedback/emit_feedback_lifecycle_v0_3b.py", "python scripts/feedback/emit_feedback_lifecycle_v0_3b.py")
text = text.replace("python scripts/validation/validate_surface_alignment_v0_3b1a.py", "python scripts/validation/validate_surface_alignment_v0_3b2.py")
text = text.replace("python scripts/validation/validate_surface_alignment_v0_3b1.py", "python scripts/validation/validate_surface_alignment_v0_3b2.py")

quick_start = """```powershell
cd "$env:USERPROFILE\\OneDrive\\Desktop\\cybernetic-memory-system"
$env:PYTHONPATH = ".\\src"

python scripts/rcc/audit_readme_surface.py
python scripts/rcc/check_rcc_nexus.py
python scripts/validation/validate_architecture_contracts.py
python scripts/validation/validate_runtime_observation_v0_2.py
python scripts/validation/validate_directory_box_v0_2b.py
python scripts/validation/validate_readme_render_hygiene_v0_2b2.py
python scripts/validation/validate_markdown_structure_v0_2b3.py
python scripts/geometry/emit_reflective_git_geometry.py
python scripts/feedback/emit_feedback_lifecycle_v0_3b.py
python scripts/alignment/emit_multilevel_alignment_v0_3b2.py
python scripts/validation/validate_reflective_git_geometry_v0_3.py
python scripts/validation/validate_feedback_lifecycle_v0_3b.py
python scripts/validation/validate_surface_alignment_v0_3b2.py
python scripts/validation/validate_multilevel_alignment_v0_3b2.py
python scripts/validation/validate_public_sync_v0_2b3.py
python -m cms cycle --repo . --profile CMS-Core
python -m unittest discover -s tests
python scripts/validate_release.py
```"""
text = sub_literal(
    r"## Quick Start\n\nRun the local validation stack:\n\n```powershell.*?```",
    "## Quick Start\n\nRun the local validation stack:\n\n" + quick_start,
    text,
)

prepush = """```powershell
$env:PYTHONPATH = ".\\src"
python scripts/rcc/audit_readme_surface.py
python scripts/rcc/check_rcc_nexus.py
python scripts/validation/validate_architecture_contracts.py
python scripts/validation/validate_runtime_observation_v0_2.py
python scripts/validation/validate_directory_box_v0_2b.py
python scripts/validation/validate_readme_render_hygiene_v0_2b2.py
python scripts/validation/validate_markdown_structure_v0_2b3.py
python scripts/geometry/emit_reflective_git_geometry.py
python scripts/feedback/emit_feedback_lifecycle_v0_3b.py
python scripts/alignment/emit_multilevel_alignment_v0_3b2.py
python scripts/validation/validate_reflective_git_geometry_v0_3.py
python scripts/validation/validate_feedback_lifecycle_v0_3b.py
python scripts/validation/validate_surface_alignment_v0_3b2.py
python scripts/validation/validate_multilevel_alignment_v0_3b2.py
python scripts/validation/validate_public_sync_v0_2b3.py
python -m cms cycle --repo . --profile CMS-Core
python -m unittest discover -s tests
python scripts/validate_release.py
```"""
text = sub_literal(
    r"### Pre-Push Checklist\n\n```powershell.*?```",
    "### Pre-Push Checklist\n\n" + prepush,
    text,
)

text = text.replace(
    "`scripts/validation/validate_surface_alignment_v0_3b1a.py` | Root and mini README alignment validator.",
    "`scripts/validation/validate_surface_alignment_v0_3b2.py` | Root and mini README alignment validator.",
)

text = re.sub(
    r"API is not active in v0\.3b1a\..*?release surfaces agree\.",
    "API is not active in v0.3b2a1. API work begins only after runtime decision, replay, dry-run, authorization, and negative-control gates are implemented after the multi-level geometric alignment lock.",
    text,
)
text = re.sub(
    r"API is not active in v0\.3b2[a-zA-Z0-9]*\..*?runtime decision/replay layer\.",
    "API is not active in v0.3b2a1. API work begins only after runtime decision, replay, dry-run, authorization, and negative-control gates are implemented after the multi-level geometric alignment lock.",
    text,
)

metric_anchor = "| Multi-level alignment validation | `reports/alignment/latest_multilevel_alignment_validation.md` |"
metric_rows = [
    "| Feedback items checked | `3` |",
    "| Feedback items aligned | `3` |",
    "| Alignment layer count | `10` |",
    "| Runtime decision kernel | `planned: v0.3b3` |",
]
if metric_anchor in text:
    for row in metric_rows:
        if row not in text:
            text = text.replace(metric_anchor, metric_anchor + "\n" + row, 1)

snapshot_anchor = "| v0.3b2 Multi-Level Geometric Alignment | Do feedback items bind to geometry, validators, evidence, routes, registry, and public surfaces? | `reports/alignment/latest_multilevel_alignment_report.md` |"
snapshot_row = "| v0.3b2a1 README Documentation Coherence Repair | Does the public README cleanly document the v0.3b2 lock after the incomplete v0.3b2a seal? | `reports/readme/latest_readme_mini_repo_audit.md` |"
if snapshot_anchor in text and snapshot_row not in text:
    text = text.replace(snapshot_anchor, snapshot_anchor + "\n" + snapshot_row, 1)

section = """## CMS-SA v0.3b2a1 - README Documentation Coherence Repair

v0.3b2a1 repairs the incomplete v0.3b2a documentation seal. The v0.3b2a attempt created version docs and a tag, but the README normalizer failed before updating README, registry, and validator expectations.

Repair rule:

```text
A documentation seal is not complete unless README, registry, validators,
reports, public sync, and release tag all agree.
```

What v0.3b2 remains responsible for:

```text
feedback item -> route -> files -> geometry -> evidence -> validators
-> README/public surface -> version registry -> release tag/public sync
```

What v0.3b2a1 repairs:

- stale README checkpoint and previous-seal text,
- stale Quick Start validation commands,
- malformed multiline README paths,
- documentation seal ledger continuity,
- public checkpoint/tag agreement for the documentation repair.

Non-claim lock: v0.3b2a1 improves public readability and repository navigation. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
"""
if "## CMS-SA v0.3b2a1 - README Documentation Coherence Repair" not in text:
    text += "\n\n" + section

lesson_021 = "| CMS-L-021 | v0.3b2 locked runtime alignment but README still carried malformed multiline paths and stale validator references. | Runtime correctness and public explanation are separate surfaces; a sealed runtime can still have public documentation drift. | After a major lock, run a documentation coherence seal that repairs README path render, Quick Start commands, public metrics, and future-boundary language. |"
lesson_022 = "| CMS-L-022 | v0.3b2a was pasted/run interactively and the README normalizer failed on a regex replacement escape before README/registry updates landed. | Python regex replacement strings treated backslashes in PowerShell paths as escape templates, while the script continued after a blocked step. | Documentation coherence scripts must use literal replacement functions for README code blocks and must not continue after a failed normalizer. |"

if "CMS-L-021" not in text:
    text = text.replace(
        "| CMS-L-020 | Multi-level alignment was evaluated before the new version's public-sync report could exist. | Internal alignment and post-tag public synchronization are different temporal phases. | Multi-level alignment must require public-sync report presence, while the dedicated public-sync validator verifies HEAD/origin/tag/registry agreement after commit/tag/push. |",
        "| CMS-L-020 | Multi-level alignment was evaluated before the new version's public-sync report could exist. | Internal alignment and post-tag public synchronization are different temporal phases. | Multi-level alignment must require public-sync report presence, while the dedicated public-sync validator verifies HEAD/origin/tag/registry agreement after commit/tag/push. |\n" + lesson_021,
    )
if "CMS-L-022" not in text:
    text = text.replace(lesson_021, lesson_021 + "\n" + lesson_022)

README.write_text(text, encoding="utf-8")

for rel in [
    "scripts/rcc/audit_readme_surface.py",
    "scripts/validation/validate_readme_render_hygiene_v0_2b2.py",
    "scripts/validation/validate_surface_alignment_v0_3b2.py",
]:
    path = ROOT / rel
    if not path.exists():
        continue
    s = path.read_text(encoding="utf-8", errors="replace")

    s = re.sub(r"v0\.3b2a1a1", "v0.3b2a1", s)
    s = re.sub(r"v0\.3b2a1", "v0.3b2a1", s)
    s = re.sub(r"v0\.3b2a", "v0.3b2a1", s)
    s = re.sub(r"v0\.3b2", "v0.3b2a1", s)

    s = s.replace("CMS-SA v0.3b2a1 - Multi-Level Geometric Alignment Feedback Lock", CHECKPOINT)
    s = s.replace("CMS-SA v0.3b2a - README Documentation Coherence Seal", CHECKPOINT)
    s = s.replace("CMS-SA v0.3b2 - Multi-Level Geometric Alignment Feedback Lock", CHECKPOINT)
    s = s.replace("CMS--SA-v0.3b2a1-blue", "CMS--SA-v0.3b2a1-blue")

    s = s.replace('PREVIOUS_VERSION = "v0.3b1a"', 'PREVIOUS_VERSION = "v0.3b2a"')
    s = s.replace('PREVIOUS_VERSION = "v0.3b2"', 'PREVIOUS_VERSION = "v0.3b2a"')
    s = s.replace('"| Previous seal | CMS-SA v0.3b1a |"', '"| Previous seal | CMS-SA v0.3b2a |"')
    s = s.replace('"| Previous seal | CMS-SA v0.3b2 |"', '"| Previous seal | CMS-SA v0.3b2a |"')
    s = s.replace('"API remains inactive"', '"API is not active in v0.3b2a1"')
    s = s.replace('"API is not active in v0.3b2a1a1"', '"API is not active in v0.3b2a1"')

    path.write_text(s, encoding="utf-8")

registry_path = ROOT / "outputs" / "version_registry" / "cms_version_registry.json"
if registry_path.exists():
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
else:
    registry = {"schema": "CMS-SA-version-registry", "repository": "cybernetic-memory-system", "versions": []}

registry["current_version"] = VERSION
registry["latest_version"] = VERSION
registry["current_checkpoint"] = CHECKPOINT
registry["previous_version"] = PREVIOUS
registry["next_anchor"] = NEXT_ANCHOR
registry["updated_at"] = NOW

versions = registry.setdefault("versions", [])
if not any(isinstance(item, dict) and item.get("version") == VERSION for item in versions):
    versions.append({
        "version": VERSION,
        "name": "README Documentation Coherence Repair",
        "status": "documentation-coherence-repair",
        "previous": PREVIOUS,
        "next": "v0.3b3",
        "non_claim_lock": "Documentation coherence is not code correctness."
    })

registry_path.parent.mkdir(parents=True, exist_ok=True)
registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")