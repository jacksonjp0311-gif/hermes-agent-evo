from __future__ import annotations

import json
from pathlib import Path

ROOT = Path.cwd()
VERSION = "v0.3b2a3"
PREVIOUS = "v0.3b2a2"
CHECKPOINT = "CMS-SA v0.3b2a3 - Version Token Normalization Seal"
PREVIOUS_SEAL = "CMS-SA v0.3b2a2 - Surface Validator Compatibility Seal"
NEXT_ANCHOR = "CMS-SA v0.3b3 - Runtime Decision Kernel and Replay Ledger"
NOW = "2026-06-02T13:49:16.1065482-04:00"

FILES = [
    "README.md",
    "configs/alignment/README.md",
    "src/cms/alignment/README.md",
    "scripts/alignment/README.md",
    "outputs/alignment/README.md",
    "reports/alignment/README.md",
    "scripts/rcc/audit_readme_surface.py",
    "scripts/validation/validate_readme_render_hygiene_v0_2b2.py",
    "scripts/validation/validate_surface_alignment_v0_3b2.py",
    "scripts/validation/validate_multilevel_alignment_v0_3b2.py",
    "scripts/alignment/emit_multilevel_alignment_v0_3b2.py",
    "src/cms/alignment/multilevel.py",
    "configs/alignment/multilevel_alignment_contract.json",
]

def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")

def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def normalize_tokens(text: str) -> str:
    replacements = {
        "v0.3b2a2a22": VERSION,
        "v0.3b2a2a2": PREVIOUS,
        "v0.3b2a2": VERSION,
        "CMS--SA-v0.3b2a2a22-blue": f"CMS--SA-{VERSION}-blue",
        "CMS--SA-v0.3b2a2-blue": f"CMS--SA-{VERSION}-blue",
        "CMS-RCC-N-v0.3b2a2a22": f"CMS-RCC-N-{VERSION}",
        "CMS-RCC-N-v0.3b2a2": f"CMS-RCC-N-{VERSION}",
        "CMS-SA v0.3b2a2a22 - README Documentation Coherence Repair": CHECKPOINT,
        "CMS-SA v0.3b2a2 - Surface Validator Compatibility Seal": CHECKPOINT,
        "CMS-SA v0.3b2a2 - README Documentation Coherence Repair": CHECKPOINT,
        "CMS-SA v0.3b2a2 - Multi-Level Geometric Alignment Feedback Lock": CHECKPOINT,
        "CMS-SA v0.3b2a2": f"CMS-SA {VERSION}",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

for rel in FILES:
    path = ROOT / rel
    if not path.exists():
        continue
    s = normalize_tokens(read(path))

    # Re-pin previous seal/version expectations where validators explicitly check previous.
    if rel.endswith("validate_surface_alignment_v0_3b2.py"):
        s = s.replace(f'PREVIOUS_VERSION = "{VERSION}"', f'PREVIOUS_VERSION = "{PREVIOUS}"')
        s = s.replace(f'"| Previous seal | CMS-SA {VERSION} |"', f'"| Previous seal | CMS-SA {PREVIOUS} |"')
        s = s.replace(f'"| Previous seal | CMS-SA {PREVIOUS}a |"', f'"| Previous seal | CMS-SA {PREVIOUS} |"')

    write(path, s)

# README exact public header/table corrections.
readme = ROOT / "README.md"
s = read(readme)
lines = s.splitlines()
out = []
for line in lines:
    if line.startswith("Current checkpoint: **"):
        out.append(f"Current checkpoint: **{CHECKPOINT}**")
    elif line.startswith("Previous seal: **"):
        out.append(f"Previous seal: **{PREVIOUS_SEAL}**")
    elif line.startswith("| Current checkpoint |"):
        out.append(f"| Current checkpoint | CMS-SA {VERSION} |")
    elif line.startswith("| Previous seal |"):
        out.append(f"| Previous seal | CMS-SA {PREVIOUS} |")
    else:
        out.append(line)
s = "\n".join(out) + "\n"

section = f"""## CMS-SA v0.3b2a3 - Version Token Normalization Seal

v0.3b2a3 repairs a runaway version-token mutation discovered after v0.3b2a2.

Failure signature:

```text
v0.3b2a2 -> v0.3b2a2a22
```

Repair rule:

```text
Version advancement must use exact assigned constants, not broad replacement
passes that can rewrite already-updated tokens.
```

Non-claim lock: v0.3b2a3 repairs repository documentation and validator token coherence only. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
"""
if "## CMS-SA v0.3b2a3 - Version Token Normalization Seal" not in s:
    s += "\n\n" + section

lesson = "| CMS-L-024 | v0.3b2a2 produced validator expectations like v0.3b2a2a22. | Broad version-token replacement rewrote already-updated version strings instead of using exact assigned constants. | Version advancement scripts must replace exact stale tokens only and must assert that no generated version token contains duplicated suffix patterns. |"
if "CMS-L-024" not in s:
    if "CMS-L-023" in s:
        s = s.replace("\n| CMS-L-023 ", "\n" + lesson + "\n| CMS-L-023 ", 1)
    else:
        s += "\n\n" + lesson + "\n"

write(readme, s)

# Ensure mini README current token.
for rel in ["configs/alignment/README.md","src/cms/alignment/README.md","scripts/alignment/README.md","outputs/alignment/README.md","reports/alignment/README.md"]:
    path = ROOT / rel
    if not path.exists():
        continue
    s = read(path)
    if f"CMS-RCC-N-{VERSION}" not in s:
        s += f"\nRCC Nexus TTL: CMS-RCC-N-{VERSION} / 180 days\n"
    if f"CMS-SA {VERSION}" not in s:
        s += f"\nCurrent checkpoint: CMS-SA {VERSION}\n"
    write(path, s)

# Registry
p = ROOT / "outputs/version_registry/cms_version_registry.json"
reg = json.loads(read(p)) if p.exists() else {"schema":"CMS-SA-version-registry","repository":"cybernetic-memory-system","versions":[]}
reg["current_version"] = VERSION
reg["latest_version"] = VERSION
reg["current_checkpoint"] = CHECKPOINT
reg["previous_version"] = PREVIOUS
reg["next_anchor"] = NEXT_ANCHOR
reg["updated_at"] = NOW
versions = reg.setdefault("versions", [])
if not any(isinstance(x, dict) and x.get("version") == VERSION for x in versions):
    versions.append({
        "version": VERSION,
        "name": "Version Token Normalization Seal",
        "status": "version-token-repair",
        "previous": PREVIOUS,
        "next": "v0.3b3",
        "non_claim_lock": "Version token normalization is not code correctness."
    })
write(p, json.dumps(reg, indent=2) + "\n")

# Assert no bad runaway tokens remain in validator-bound text files.
bad = []
for rel in FILES:
    path = ROOT / rel
    if path.exists():
        content = read(path)
        for token in ["v0.3b2a2a22", "v0.3b2a2a2", "CMS-RCC-N-v0.3b2a2a22", "CMS--SA-v0.3b2a2a22-blue"]:
            if token in content:
                bad.append(f"{rel}:{token}")
if bad:
    raise SystemExit("Runaway version tokens remain: " + ", ".join(bad))