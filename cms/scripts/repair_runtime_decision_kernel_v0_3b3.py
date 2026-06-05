from __future__ import annotations
import hashlib, json, re, subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path.cwd()
VERSION = "v0.3b3"
PREVIOUS = "v0.3b2a3"
CHECKPOINT = "CMS-SA v0.3b3 - Runtime Decision Kernel and Replay Ledger"
PREVIOUS_SEAL = "CMS-SA v0.3b2a3 - Version Token Normalization Seal"
NEXT_ANCHOR = "CMS-SA v0.3b4 - Negative Control and Downgrade Harness"
NOW = "2026-06-02T14:01:01.5611526-04:00"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write(p: Path, s: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def sublit(pattern: str, repl: str, src: str) -> str:
    return re.sub(pattern, lambda _m: repl, src, flags=re.S)

# Runtime package
write(ROOT / "src/cms/decision/__init__.py", '"""CMS runtime decision kernel."""\n\nfrom .kernel import build_decision, stable_hash\n\n__all__ = ["build_decision", "stable_hash"]\n')

kernel = r'''
from __future__ import annotations
import hashlib, json, subprocess
from pathlib import Path
from typing import Any

VERSION = "v0.3b3"
REQUIRED_SIGNALS = [
    ("readme_audit", "reports/readme/latest_readme_mini_repo_audit.json"),
    ("readme_render_hygiene", "reports/render_hygiene/latest_readme_render_hygiene.json"),
    ("markdown_structure", "reports/markdown_structure/latest_markdown_structure.json"),
    ("reflective_git_geometry", "reports/geometry/latest_reflective_git_geometry_validation.json"),
    ("feedback_lifecycle", "reports/feedback/latest_feedback_lifecycle_validation.json"),
    ("surface_alignment", "reports/surface_alignment/latest_surface_alignment_report.json"),
    ("multilevel_alignment", "reports/alignment/latest_multilevel_alignment_validation.json"),
    ("release_validator", "reports/release/latest_release_validation.json"),
]
OPTIONAL_SIGNALS = [("public_sync", "reports/public_sync/latest_public_sync_report.json")]


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def stable_hash(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _signal(root: Path, name: str, rel: str, required: bool) -> dict[str, Any]:
    path = root / rel
    if not path.exists():
        return {"name": name, "path": rel, "required": required, "present": False, "passed": False, "errors": ["missing_signal_file"]}
    try:
        data = load_json(path)
    except Exception as exc:
        return {"name": name, "path": rel, "required": required, "present": True, "passed": False, "errors": [f"unreadable_json:{type(exc).__name__}"]}
    passed = data.get("passed") is True
    return {"name": name, "path": rel, "required": required, "present": True, "passed": passed, "schema": data.get("schema"), "errors": [] if passed else data.get("findings", ["passed_not_true"])}


def _git_state(root: Path) -> dict[str, Any]:
    try:
        proc = subprocess.run(["git", "status", "--short"], cwd=str(root), check=True, capture_output=True, text=True)
        lines = [x.strip() for x in proc.stdout.splitlines() if x.strip()]
        unexpected = [x for x in lines if "_repo_dump/" not in x]
        return {"available": True, "dirty": bool(unexpected), "unexpected_dirty": unexpected, "ignored_untracked": [x for x in lines if "_repo_dump/" in x]}
    except Exception:
        return {"available": False, "dirty": True, "unexpected_dirty": ["git_status_failed"], "ignored_untracked": []}


def build_decision(root: Path, include_git_state: bool = False) -> dict[str, Any]:
    root = root.resolve()
    signals = [_signal(root, n, r, True) for n, r in REQUIRED_SIGNALS]
    signals += [_signal(root, n, r, False) for n, r in OPTIONAL_SIGNALS]
    failures = [x["name"] for x in signals if x.get("required") and x.get("passed") is not True]
    decision = "block" if failures else "promote"
    reason = "required_validation_surface_failed" if failures else "all_required_repository_bound_validation_surfaces_passed"
    body = {
        "schema": "CMS-SA-v0.3b3-runtime-decision",
        "version": VERSION,
        "decision": decision,
        "reason": reason,
        "required_failures": failures,
        "signals": signals,
        "git_state": _git_state(root) if include_git_state else {"available": False, "dirty": None, "unexpected_dirty": [], "note": "volatile git status is checked by final release gate"},
        "next_allowed_action": "CMS-SA v0.3b4 - Negative Control and Downgrade Harness" if decision == "promote" else "repair_failed_surfaces_before_promotion",
        "non_claim_lock": "Runtime decision checks repository-bound validation surfaces only. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.",
    }
    body["decision_hash"] = stable_hash({k: v for k, v in body.items() if k != "decision_hash"})
    return body
'''
write(ROOT / "src/cms/decision/kernel.py", kernel)

emitter = r'''
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from cms.decision.kernel import VERSION, build_decision

ROOT = Path.cwd()
OUT_JSON = ROOT / "outputs/decision/latest_runtime_decision.json"
OUT_MD = ROOT / "outputs/decision/latest_runtime_decision.md"
REPORT_JSON = ROOT / "reports/decision/latest_runtime_decision.json"
REPORT_MD = ROOT / "reports/decision/latest_runtime_decision.md"
LEDGER = ROOT / "outputs/replay/runtime_decision_replay_ledger.jsonl"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    failures = data.get("required_failures") or []
    lines = ["# CMS Runtime Decision", "", f"- Version: `{data['version']}`", f"- Decision: `{data['decision']}`", f"- Reason: `{data['reason']}`", f"- Next allowed action: `{data['next_allowed_action']}`", f"- Decision hash: `{data['decision_hash']}`", "", "## Required failures", ""]
    lines += [f"- `{x}`" for x in failures] if failures else ["- none"]
    lines += ["", "## Non-claim lock", "", data.get("non_claim_lock", ""), ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def last_hash(path: Path) -> str | None:
    if not path.exists(): return None
    lines = [x for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines: return None
    try: return json.loads(lines[-1]).get("decision_hash")
    except Exception: return None


def append_ledger(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "version": data["version"], "decision": data["decision"], "reason": data["reason"], "decision_hash": data["decision_hash"], "next_allowed_action": data["next_allowed_action"]}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def main() -> None:
    decision = build_decision(ROOT, include_git_state=False)
    write_json(OUT_JSON, decision); write_json(REPORT_JSON, decision)
    write_md(OUT_MD, decision); write_md(REPORT_MD, decision)
    if last_hash(LEDGER) != decision["decision_hash"]:
        append_ledger(LEDGER, decision)
    print(json.dumps({"schema": "CMS-SA-v0.3b3-runtime-decision-emission", "passed": True, "version": VERSION, "decision": decision["decision"], "reason": decision["reason"], "decision_hash": decision["decision_hash"], "non_claim_lock": "Decision emission writes repository decision artifacts only."}, indent=2))

if __name__ == "__main__": main()
'''
write(ROOT / "scripts/decision/emit_runtime_decision_v0_3b3.py", emitter)

validator = r'''
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path.cwd(); VERSION = "v0.3b3"
DECISION = ROOT / "outputs/decision/latest_runtime_decision.json"
LEDGER = ROOT / "outputs/replay/runtime_decision_replay_ledger.jsonl"
REPORT_JSON = ROOT / "reports/decision/latest_runtime_decision_validation.json"
REPORT_MD = ROOT / "reports/decision/latest_runtime_decision_validation.md"
ALLOWED = {"promote", "block", "downgrade", "observe_only"}


def write_reports(result: dict) -> None:
    REPORT_JSON.parent.mkdir(parents=True, exist_ok=True)
    REPORT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    findings = result.get("findings") or []
    lines = ["# Runtime Decision Validation", "", f"- Passed: `{result['passed']}`", f"- Errors: `{result['errors']}`", "", "## Findings", ""]
    lines += [f"- `{x}`" for x in findings] if findings else ["- none"]
    lines += ["", result["non_claim_lock"], ""]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    findings = []
    if not DECISION.exists():
        findings.append("missing_runtime_decision")
        data = {}
    else:
        data = json.loads(DECISION.read_text(encoding="utf-8"))
    if data:
        if data.get("schema") != "CMS-SA-v0.3b3-runtime-decision": findings.append("schema_mismatch")
        if data.get("version") != VERSION: findings.append(f"version_mismatch:{data.get('version')}")
        if data.get("decision") not in ALLOWED: findings.append(f"invalid_decision:{data.get('decision')}")
        if not data.get("decision_hash"): findings.append("missing_decision_hash")
        for item in data.get("signals", []):
            if item.get("required") and item.get("passed") is not True:
                findings.append(f"required_signal_failed:{item.get('name')}")
        if data.get("decision") == "promote" and data.get("required_failures"):
            findings.append("promote_with_required_failures")
        if not LEDGER.exists() or data.get("decision_hash") not in LEDGER.read_text(encoding="utf-8", errors="replace"):
            findings.append("decision_hash_missing_from_replay_ledger")
    result = {"schema": "CMS-SA-v0.3b3-runtime-decision-validation", "passed": len(findings) == 0, "version": VERSION, "errors": len(findings), "findings": findings, "decision": data.get("decision"), "decision_hash": data.get("decision_hash"), "non_claim_lock": "Runtime decision validation is repository-bound and does not prove code correctness."}
    write_reports(result)
    print(json.dumps(result, indent=2))
    if findings: raise SystemExit(1)

if __name__ == "__main__": main()
'''
write(ROOT / "scripts/validation/validate_runtime_decision_v0_3b3.py", validator)

# Mini READMEs and contract
for rel, title in {
    "configs/decision/README.md": "Decision contracts for action classification.",
    "src/cms/decision/README.md": "Runtime Decision Kernel and decision hashing logic.",
    "scripts/decision/README.md": "Decision emitters.",
    "outputs/decision/README.md": "Latest runtime decision artifacts.",
    "outputs/replay/README.md": "Append-only runtime decision replay ledger.",
    "reports/decision/README.md": "Runtime decision reports and validation outputs.",
}.items():
    write(ROOT / rel, f"# {Path(rel).parent}\n\n{title}\n\nRCC Nexus TTL: CMS-RCC-N-v0.3b3 / 180 days\nCurrent checkpoint: CMS-SA v0.3b3\n")
write(ROOT / "configs/decision/runtime_decision_contract.json", json.dumps({"schema":"CMS-SA-v0.3b3-runtime-decision-contract","version":VERSION,"allowed_decisions":["promote","block","downgrade","observe_only"],"non_claim_lock":"Decision contracts are repository-bound and do not prove correctness."}, indent=2) + "\n")

# README
readme = ROOT / "README.md"
s = read(readme)
s = re.sub(r"CMS--SA-v0\.3b2[a-zA-Z0-9]*-blue", "CMS--SA-v0.3b3-blue", s)
s = sublit(r"Current checkpoint: \*\*CMS-SA v0\.3b.*?\*\*", f"Current checkpoint: **{CHECKPOINT}**", s)
s = sublit(r"Previous seal: \*\*CMS-SA v0\.3b.*?\*\*", f"Previous seal: **{PREVIOUS_SEAL}**", s)
s = re.sub(r"\|\s*Current checkpoint\s*\|\s*CMS-SA v0\.3b[a-zA-Z0-9.]*\s*\|", "| Current checkpoint | CMS-SA v0.3b3 |", s)
s = re.sub(r"\|\s*Previous seal\s*\|\s*CMS-SA v0\.3b[a-zA-Z0-9.]*\s*\|", "| Previous seal | CMS-SA v0.3b2a3 |", s)
s = re.sub(r"CMS-RCC-N-v0\.3b[a-zA-Z0-9.]* / 180 days", "CMS-RCC-N-v0.3b3 / 180 days", s)
s = re.sub(r"API is not active in v0\.3b[a-zA-Z0-9.]*\.", "API is not active in v0.3b3.", s)
if "| v0.3b3 Runtime Decision Kernel |" not in s:
    s = s.replace("| v0.3b2 Multi-Level Geometric Alignment | Do feedback items bind to geometry, validators, evidence, routes, registry, and public surfaces? | `reports/alignment/latest_multilevel_alignment_report.md` |", "| v0.3b2 Multi-Level Geometric Alignment | Do feedback items bind to geometry, validators, evidence, routes, registry, and public surfaces? | `reports/alignment/latest_multilevel_alignment_report.md` |\n| v0.3b3 Runtime Decision Kernel | Can validation signals produce one replayable runtime decision? | `reports/decision/latest_runtime_decision.md` |")
s = s.replace("| Runtime decision kernel | `planned: v0.3b3` |", "| Runtime decision kernel | `active: v0.3b3` |")
for row in ["| Runtime decision | `outputs/decision/latest_runtime_decision.json` |", "| Runtime decision validation | `reports/decision/latest_runtime_decision_validation.md` |", "| Replay ledger | `outputs/replay/runtime_decision_replay_ledger.jsonl` |"]:
    if row not in s and "| Runtime decision kernel | `active: v0.3b3` |" in s:
        s = s.replace("| Runtime decision kernel | `active: v0.3b3` |", "| Runtime decision kernel | `active: v0.3b3` |\n" + row, 1)
if "python scripts/decision/emit_runtime_decision_v0_3b3.py" not in s:
    s = s.replace("python scripts/validation/validate_multilevel_alignment_v0_3b2.py", "python scripts/validation/validate_multilevel_alignment_v0_3b2.py\npython scripts/decision/emit_runtime_decision_v0_3b3.py\npython scripts/validation/validate_runtime_decision_v0_3b3.py")
section = """## CMS-SA v0.3b3 - Runtime Decision Kernel and Replay Ledger

v0.3b3 adds a bounded runtime decision layer. It converts repository-bound validation surfaces into one typed decision object.

Decision states:

```text
promote | block | downgrade | observe_only
```

Decision rule:

```text
Validators do not merely pass individually; they are aggregated into a replayable
decision surface with a decision hash and ledger entry.
```

Non-claim lock: v0.3b3 decides repository-bound next action only. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
"""
if "## CMS-SA v0.3b3 - Runtime Decision Kernel and Replay Ledger" not in s:
    s += "\n\n" + section
lesson = "| CMS-L-025 | v0.3b2a3 showed validator truth, public sync truth, and volatile latest-run artifacts can diverge. | Latest runtime/evidence artifacts can rewrite during validation even when stable public release state is true. | Runtime decisions must distinguish validator truth, public sync truth, stable release evidence, volatile latest-run evidence, dirty-state blockers, and next allowed action. |"
if "CMS-L-025" not in s:
    s = s.replace("\n| CMS-L-024 ", "\n" + lesson + "\n| CMS-L-024 ", 1) if "CMS-L-024" in s else s + "\n\n" + lesson + "\n"
for row in ["| `configs/decision/` | Runtime decision contracts for action classification. |", "| `src/cms/decision/` | Runtime Decision Kernel and decision hashing logic. |", "| `scripts/decision/` | Decision emitters that produce replayable decision artifacts. |", "| `outputs/decision/` | Latest runtime decision artifacts. |", "| `outputs/replay/` | Append-only runtime decision replay ledger. |", "| `reports/decision/` | Runtime decision validation reports. |"]:
    if row not in s and "| `tests/` | Unit tests" in s:
        s = s.replace("| `tests/` |", row + "\n| `tests/` |", 1)
write(readme, s)

# Patch validators with exact current version. Then re-pin previous in surface validator.
for rel in ["scripts/rcc/audit_readme_surface.py", "scripts/validation/validate_readme_render_hygiene_v0_2b2.py", "scripts/validation/validate_surface_alignment_v0_3b2.py"]:
    p = ROOT / rel
    if not p.exists(): continue
    t = read(p)
    t = t.replace("v0.3b2a3", VERSION)
    t = t.replace("CMS-SA v0.3b3 - Version Token Normalization Seal", CHECKPOINT)
    t = t.replace("CMS-SA v0.3b3 - README Documentation Coherence Repair", CHECKPOINT)
    if rel.endswith("validate_surface_alignment_v0_3b2.py"):
        t = t.replace(f'PREVIOUS_VERSION = "{VERSION}"', f'PREVIOUS_VERSION = "{PREVIOUS}"')
        t = t.replace(f'"| Previous seal | CMS-SA {VERSION} |"', f'"| Previous seal | CMS-SA {PREVIOUS} |"')
    write(p, t)

# Registry
regp = ROOT / "outputs/version_registry/cms_version_registry.json"
reg = json.loads(read(regp)) if regp.exists() else {"schema":"CMS-SA-version-registry","repository":"cybernetic-memory-system","versions":[]}
reg["current_version"] = VERSION; reg["latest_version"] = VERSION; reg["current_checkpoint"] = CHECKPOINT; reg["previous_version"] = PREVIOUS; reg["next_anchor"] = NEXT_ANCHOR; reg["updated_at"] = NOW
versions = reg.setdefault("versions", [])
if not any(isinstance(x, dict) and x.get("version") == VERSION for x in versions):
    versions.append({"version": VERSION, "name": "Runtime Decision Kernel and Replay Ledger", "status": "runtime-decision-kernel", "previous": PREVIOUS, "next": "v0.3b4", "non_claim_lock": "Runtime decisions are repository-bound and do not prove correctness."})
write(regp, json.dumps(reg, indent=2) + "\n")