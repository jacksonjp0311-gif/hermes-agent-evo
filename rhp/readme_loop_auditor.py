from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

RHP_README_LOOP_AUDITOR_SCHEMA = "RHP-README-LOOP-AUDITOR-v0.1"
REQUIRED_README_PHRASES = ["RHPLOAD = major gate/audit box", "RHPDROP [closed]", "Any AI continuing this repo must first read", "The system does not self-authorize"]
REQUIRED_AGENT_PHRASES = ["Stable API symbols and evidence keys must be extended additively", "RHPDROP [closed]"]
REQUIRED_RHP_README_PHRASES = ["rhp/api_surface_auditor.py", "RHPDROP [closed]"]

def audit(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    readme = (root / "README.md").read_text(encoding="utf-8", errors="replace")
    agents = (root / "AGENTS.md").read_text(encoding="utf-8", errors="replace")
    rhp_readme = (root / "rhp/README.md").read_text(encoding="utf-8", errors="replace")
    checks: list[dict[str, Any]] = []
    for phrase in REQUIRED_README_PHRASES:
        checks.append({"file": "README.md", "phrase": phrase, "ok": phrase in readme})
    for phrase in REQUIRED_AGENT_PHRASES:
        checks.append({"file": "AGENTS.md", "phrase": phrase, "ok": phrase in agents})
    for phrase in REQUIRED_RHP_README_PHRASES:
        checks.append({"file": "rhp/README.md", "phrase": phrase, "ok": phrase in rhp_readme})
    missing = [check for check in checks if check["ok"] is not True]
    return {"schema": RHP_README_LOOP_AUDITOR_SCHEMA, "ok": len(missing) == 0, "checks": checks, "missing": missing, "non_claim_lock": "README loop auditor reads local docs only. It does not mutate files, execute repairs, call remote APIs, or grant authority."}

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Audit README/AGENTS/RHP README for RHP operator-loop clarity")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = audit(args.repo_root)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if data["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
