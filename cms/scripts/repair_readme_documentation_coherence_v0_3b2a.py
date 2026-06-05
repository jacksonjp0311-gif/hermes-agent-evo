from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path.cwd()
README = ROOT / "README.md"
TEXT = README.read_text(encoding="utf-8", errors="replace")

VERSION = "v0.3b2a"
PREVIOUS = "v0.3b2"
CHECKPOINT = "CMS-SA v0.3b2a - README Documentation Coherence Seal"
PREVIOUS_SEAL = "CMS-SA v0.3b2 - Multi-Level Geometric Alignment Feedback Lock"


def replace_all(text: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        text = text.replace(old, new)
    return text


text = TEXT

# Badge and checkpoint.
text = re.sub(r"CMS--SA-v0\.3b2-blue", "CMS--SA-v0.3b2a-blue", text)
text = re.sub(
    r"Current checkpoint: \*\*CMS-SA v0\.3b2 .*?\*\*",
    f"Current checkpoint: **{CHECKPOINT}**",
    text,
)
text = re.sub(
    r"Previous seal: \*\*CMS-SA v0\.3b1 .*?\*\*",
    f"Previous seal: **{PREVIOUS_SEAL}**",
    text,
)
text = re.sub(
    r"Previous seal: \*\*CMS-SA v0\.3b2 .*?\*\*",
    f"Previous seal: **{PREVIOUS_SEAL}**",
    text,
)

# Table state.
text = re.sub(r"\|\s*Current checkpoint\s*\|\s*CMS-SA v0\.3b2\s*\|", "| Current checkpoint | CMS-SA v0.3b2a |", text)
text = re.sub(r"\|\s*Previous seal\s*\|\s*CMS-SA v0\.3b1a\s*\|", "| Previous seal | CMS-SA v0.3b2 |", text)
text = re.sub(r"\|\s*Previous seal\s*\|\s*CMS-SA v0\.3b1\s*\|", "| Previous seal | CMS-SA v0.3b2 |", text)

# RCC TTL.
text = text.replace("CMS-RCC-N-v0.3b2 / 180 days", "CMS-RCC-N-v0.3b2a / 180 days")

# Fix malformed multiline paths seen in README preview.
text = replace_all(text, [
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
])

# Remove accidental duplicated directory row if both old and corrected rows exist.
text = re.sub(
    r"\n\| `outputs/evidence/`, `outputs/feedback/` \| Latest evidence packages emitted by the runtime\. \|",
    "",
    text,
)

# Quick Start cleanup.
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

text = re.sub(
    r"## Quick Start\n\nRun the local validation stack:\n\n```powershell.*?```",
    "## Quick Start\n\nRun the local validation stack:\n\n" + quick_start,
    text,
    flags=re.S,
)

# Pre-push checklist cleanup.
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

text = re.sub(
    r"### Pre-Push Checklist\n\n```powershell.*?```",
    "### Pre-Push Checklist\n\n" + prepush,
    text,
    flags=re.S,
)

# Update Primary Nexus file entry for surface alignment to latest validator.
text = text.replace(
    "`scripts/validation/validate_surface_alignment_v0_3b1a.py` | Root and mini README alignment validator.",
    "`scripts/validation/validate_surface_alignment_v0_3b2.py` | Root and mini README alignment validator.",
)

# Update Pre-API wording.
text = text.replace(
    "API is not active in v0.3b1a. API work begins only after multi-level geometric alignment confirms root README, mini READMEs, route maps, validators, reports, geometry, feedback lifecycle, and release surfaces agree.",
    "API is not active in v0.3b2a. API work begins only after runtime decision, replay, dry-run, authorization, and negative-control gates are implemented after the multi-level geometric alignment lock.",
)
text = text.replace(
    "API is not active in v0.3b2. API work begins only after multi-level geometric alignment confirms root README, mini READMEs, route maps, validators, reports, geometry, feedback lifecycle, and release surfaces agree.",
    "API is not active in v0.3b2a. API work begins only after runtime decision, replay, dry-run, authorization, and negative-control gates are implemented after the multi-level geometric alignment lock.",
)

# Ensure metrics rows for v0.3b2 alignment are public.
metric_rows = [
    "| Feedback items checked | `3` |",
    "| Feedback items aligned | `3` |",
    "| Alignment layer count | `10` |",
    "| Runtime decision kernel | `planned: v0.3b3` |",
]
for row in metric_rows:
    if row not in text:
        anchor = "| Multi-level alignment validation | `reports/alignment/latest_multilevel_alignment_validation.md` |"
        text = text.replace(anchor, anchor + "\n" + row, 1)

# Add v0.3b2a to snapshot table.
row = "| v0.3b2a README Documentation Coherence | Does the public README cleanly document the v0.3b2 lock without path/render drift or stale validator references? | `reports/readme/latest_readme_mini_repo_audit.md` |"
if row not in text:
    anchor = "| v0.3b2 Multi-Level Geometric Alignment | Do feedback items bind to geometry, validators, evidence, routes, registry, and public surfaces? | `reports/alignment/latest_multilevel_alignment_report.md` |"
    text = text.replace(anchor, anchor + "\n" + row, 1)

# Add documentation moment section.
section = """## CMS-SA v0.3b2a - README Documentation Coherence Seal

v0.3b2a is a documentation and public-surface coherence patch. It does not add a new runtime law. It records the v0.3b2 breakthrough clearly in the README and repairs stale or malformed README surfaces.

What v0.3b2 proved inside the repository boundary:

```text
feedback item -> route -> files -> geometry -> evidence -> validators
-> README/public surface -> version registry -> release tag/public sync
```

v0.3b2a public documentation rules:

- no stale v0.3b1 / v0.3b1a validator references in Quick Start,
- no multiline path fragments in metrics or directory rows,
- no API activation language before the runtime decision/replay layer,
- v0.3b2 alignment metrics must be visible in the public README,
- documentation coherence is not code correctness.

Non-claim lock: v0.3b2a improves public readability and repository navigation. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
"""
if "## CMS-SA v0.3b2a - README Documentation Coherence Seal" not in text:
    text += "\n\n" + section

# Add lesson.
lesson = "| CMS-L-021 | v0.3b2 locked runtime alignment but README still carried malformed multiline paths and stale validator references. | Runtime correctness and public explanation are separate surfaces; a sealed runtime can still have public documentation drift. | After a major lock, run a documentation coherence seal that repairs README path render, Quick Start commands, public metrics, and future-boundary language. |"
if "CMS-L-021" not in text:
    text = text.replace(
        "| CMS-L-020 | Multi-level alignment was evaluated before the new version's public-sync report could exist. | Internal alignment and post-tag public synchronization are different temporal phases. | Multi-level alignment must require public-sync report presence, while the dedicated public-sync validator verifies HEAD/origin/tag/registry agreement after commit/tag/push. |",
        "| CMS-L-020 | Multi-level alignment was evaluated before the new version's public-sync report could exist. | Internal alignment and post-tag public synchronization are different temporal phases. | Multi-level alignment must require public-sync report presence, while the dedicated public-sync validator verifies HEAD/origin/tag/registry agreement after commit/tag/push. |\n" + lesson,
    )

README.write_text(text, encoding="utf-8")

# Patch validators that pin expected checkpoint tokens.
for rel in [
    "scripts/rcc/audit_readme_surface.py",
    "scripts/validation/validate_readme_render_hygiene_v0_2b2.py",
    "scripts/validation/validate_surface_alignment_v0_3b2.py",
]:
    path = ROOT / rel
    if path.exists():
        s = path.read_text(encoding="utf-8", errors="replace")
        s = s.replace("v0.3b2a2", "v0.3b2a")
        s = s.replace("v0.3b2", "v0.3b2a")
        s = s.replace("CMS-SA v0.3b2a - Multi-Level Geometric Alignment Feedback Lock", CHECKPOINT)
        s = s.replace("CMS-SA v0.3b2 - Multi-Level Geometric Alignment Feedback Lock", CHECKPOINT)
        s = s.replace("CMS--SA-v0.3b2a-blue", "CMS--SA-v0.3b2a-blue")
        path.write_text(s, encoding="utf-8")

# Surface validator should still know previous seal.
surface = ROOT / "scripts/validation/validate_surface_alignment_v0_3b2.py"
if surface.exists():
    s = surface.read_text(encoding="utf-8", errors="replace")
    s = s.replace('PREVIOUS_VERSION = "v0.3b1a"', 'PREVIOUS_VERSION = "v0.3b2"')
    s = s.replace('"| Previous seal | CMS-SA v0.3b1a |"', '"| Previous seal | CMS-SA v0.3b2 |"')
    s = s.replace(
        '"Current checkpoint: **CMS-SA v0.3b2a - Multi-Level Geometric Alignment Feedback Lock**"',
        '"Current checkpoint: **CMS-SA v0.3b2a - README Documentation Coherence Seal**"',
    )
    s = s.replace(
        '"Current checkpoint: **CMS-SA v0.3b2 - Multi-Level Geometric Alignment Feedback Lock**"',
        '"Current checkpoint: **CMS-SA v0.3b2a - README Documentation Coherence Seal**"',
    )
    s = s.replace(
        '"API remains inactive"',
        '"API is not active in v0.3b2a"',
    )
    surface.write_text(s, encoding="utf-8")

# Patch registry.
registry_path = ROOT / "outputs" / "version_registry" / "cms_version_registry.json"
if registry_path.exists():
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
else:
    registry = {
        "schema": "CMS-SA-version-registry",
        "repository": "cybernetic-memory-system",
        "versions": [],
    }

registry["current_version"] = VERSION
registry["latest_version"] = VERSION
registry["current_checkpoint"] = CHECKPOINT
registry["previous_version"] = PREVIOUS
registry["next_anchor"] = "CMS-SA v0.3b3 - Runtime Decision Kernel and Replay Ledger"
registry["updated_at"] = "2026-06-02T11:39:22.7271528-04:00"

versions = registry.setdefault("versions", [])
if not any(isinstance(item, dict) and item.get("version") == VERSION for item in versions):
    versions.append({
        "version": VERSION,
        "name": "README Documentation Coherence Seal",
        "status": "documentation-coherence-patch",
        "previous": PREVIOUS,
        "next": "v0.3b3",
        "non_claim_lock": "Documentation coherence is not code correctness."
    })

registry_path.parent.mkdir(parents=True, exist_ok=True)
registry_path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")