from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path.cwd()
VERSION = "v0.3b2a2"
PREVIOUS = "v0.3b2a1"
CHECKPOINT = "CMS-SA v0.3b2a2 - Surface Validator Compatibility Seal"
PREVIOUS_SEAL = "CMS-SA v0.3b2a1 - README Documentation Coherence Repair"
NEXT_ANCHOR = "CMS-SA v0.3b3 - Runtime Decision Kernel and Replay Ledger"
NOW = "2026-06-02T13:47:09.1152279-04:00"

def read(p): return Path(p).read_text(encoding="utf-8", errors="replace")
def write(p, s):
    p = Path(p); p.parent.mkdir(parents=True, exist_ok=True); p.write_text(s, encoding="utf-8")
def sublit(pattern, repl, src): return re.sub(pattern, lambda _m: repl, src, flags=re.S)

# README
p = ROOT / "README.md"
s = read(p)
s = re.sub(r"CMS--SA-v0\.3b2[a-zA-Z0-9]*-blue", "CMS--SA-v0.3b2a2-blue", s)
s = sublit(r"Current checkpoint: \*\*CMS-SA v0\.3b2.*?\*\*", f"Current checkpoint: **{CHECKPOINT}**", s)
s = sublit(r"Previous seal: \*\*CMS-SA v0\.3b2.*?\*\*", f"Previous seal: **{PREVIOUS_SEAL}**", s)
s = re.sub(r"\|\s*Current checkpoint\s*\|\s*CMS-SA v0\.3b2[a-zA-Z0-9]*\s*\|", "| Current checkpoint | CMS-SA v0.3b2a2 |", s)
s = re.sub(r"\|\s*Previous seal\s*\|\s*CMS-SA v0\.3b2[a-zA-Z0-9]*\s*\|", "| Previous seal | CMS-SA v0.3b2a1 |", s)
s = re.sub(r"CMS-RCC-N-v0\.3b2[a-zA-Z0-9]* / 180 days", "CMS-RCC-N-v0.3b2a2 / 180 days", s)
section = """## CMS-SA v0.3b2a2 - Surface Validator Compatibility Seal

v0.3b2a2 repairs the remaining documentation-seal compatibility boundary after v0.3b2a1.

The remaining failures were validator-surface mismatches, not runtime collapse:

```text
surface alignment failed because alignment mini READMEs did not carry CMS-RCC-N-v0.3b2a1
multi-level alignment failed because the registry advanced beyond the alignment report version
```

Repair rule:

```text
If a documentation patch advances the public checkpoint, all validator-bound mini
README tokens and alignment report version surfaces must advance with it, or the
seal is incomplete.
```

Non-claim lock: v0.3b2a2 repairs repository documentation and validator compatibility only. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
"""
if "## CMS-SA v0.3b2a2 - Surface Validator Compatibility Seal" not in s: s += "\n\n" + section
lesson = "| CMS-L-023 | v0.3b2a1 advanced README/registry but alignment mini READMEs and multi-level alignment version surfaces still pointed at earlier lock tokens. | Documentation patches changed public version state without updating every validator-bound mini README and alignment report version surface. | A documentation checkpoint is not sealed until mini README tokens, registry version, alignment report version, and validator expectations all agree. |"
if "CMS-L-023" not in s:
    if "CMS-L-022" in s:
        s = re.sub(r"(\| CMS-L-022 \|[^\n]+)", lambda m: m.group(1) + "\n" + lesson, s, count=1)
    else:
        s += "\n\n" + lesson + "\n"
write(p, s)

# Alignment mini READMEs
for rel in ["configs/alignment/README.md","src/cms/alignment/README.md","scripts/alignment/README.md","outputs/alignment/README.md","reports/alignment/README.md"]:
    p = ROOT / rel
    if p.exists():
        s = read(p)
        s = re.sub(r"CMS-RCC-N-v0\.3b2[a-zA-Z0-9]*", "CMS-RCC-N-v0.3b2a2", s)
        s = re.sub(r"CMS-SA v0\.3b2[a-zA-Z0-9]*", "CMS-SA v0.3b2a2", s)
        if "CMS-RCC-N-v0.3b2a2" not in s: s += "\n\nRCC Nexus TTL: CMS-RCC-N-v0.3b2a2 / 180 days\n"
        if "CMS-SA v0.3b2a2" not in s: s += "\nCurrent checkpoint: CMS-SA v0.3b2a2\n"
        write(p, s)

# Validators + alignment runtime/report version surfaces
for rel in ["scripts/rcc/audit_readme_surface.py","scripts/validation/validate_readme_render_hygiene_v0_2b2.py","scripts/validation/validate_surface_alignment_v0_3b2.py","scripts/validation/validate_multilevel_alignment_v0_3b2.py","scripts/alignment/emit_multilevel_alignment_v0_3b2.py","src/cms/alignment/multilevel.py","configs/alignment/multilevel_alignment_contract.json"]:
    p = ROOT / rel
    if not p.exists(): continue
    s = read(p)
    s = re.sub(r"v0\.3b2a2a2", "v0.3b2a2", s)
    s = re.sub(r"v0\.3b2a1", "v0.3b2a2", s)
    s = re.sub(r"v0\.3b2a", "v0.3b2a2", s)
    s = re.sub(r"v0\.3b2", "v0.3b2a2", s)
    s = s.replace("CMS-SA v0.3b2a2 - README Documentation Coherence Repair", CHECKPOINT)
    s = s.replace("CMS-SA v0.3b2a2 - Multi-Level Geometric Alignment Feedback Lock", CHECKPOINT)
    s = s.replace("CMS-SA v0.3b2 - Multi-Level Geometric Alignment Feedback Lock", CHECKPOINT)
    s = s.replace('PREVIOUS_VERSION = "v0.3b1a"', 'PREVIOUS_VERSION = "v0.3b2a1"')
    s = s.replace('PREVIOUS_VERSION = "v0.3b2"', 'PREVIOUS_VERSION = "v0.3b2a1"')
    s = s.replace('PREVIOUS_VERSION = "v0.3b2a"', 'PREVIOUS_VERSION = "v0.3b2a1"')
    s = s.replace('PREVIOUS_VERSION = "v0.3b2a2"', 'PREVIOUS_VERSION = "v0.3b2a1"')
    s = s.replace('"| Previous seal | CMS-SA v0.3b1a |"', '"| Previous seal | CMS-SA v0.3b2a1 |"')
    s = s.replace('"| Previous seal | CMS-SA v0.3b2 |"', '"| Previous seal | CMS-SA v0.3b2a1 |"')
    s = s.replace('"| Previous seal | CMS-SA v0.3b2a2 |"', '"| Previous seal | CMS-SA v0.3b2a1 |"')
    write(p, s)

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
    versions.append({"version":VERSION,"name":"Surface Validator Compatibility Seal","status":"validator-compatibility-repair","previous":PREVIOUS,"next":"v0.3b3","non_claim_lock":"Documentation validator compatibility is not code correctness."})
write(p, json.dumps(reg, indent=2) + "\n")