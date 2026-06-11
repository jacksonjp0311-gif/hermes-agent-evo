from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

RHP_OPERATOR_QUICKSTART_SCHEMA = "RHP-OPERATOR-QUICKSTART-v0.1"
READ_ORDER = [
    "docs/context-layer/latest-rhp.json",
    "docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md",
    "docs/context-layer/operator-dashboard.txt",
    "docs/context-layer/hermes-operator-context.json",
    "AGENTS.md",
    "README.md",
    "rhp/README.md",
]
OUTPUT_GRAMMAR = {
    "RHPLOAD": "major gate/audit box",
    "RHPWAIT": "single-line fill/loading surface",
    "RHPDROP": "closed compact summary for repetitive command groups",
    "RHPDIAG": "runtime diagnosis/failure box",
}
AUTHORITY_RULES = [
    "Hermes/RHP never self-authorizes.",
    "All mutation requires one human-authorized All-One script.",
    "Unknown dirty paths block.",
    "Autoheal remains dry-run/proposal-only unless a later human-authorized operation changes the contract.",
    "Remote CI is the integration truth surface; local validation is a bounded proof surface.",
]

def build_quickstart(repo_root: str | Path = ".") -> dict[str, Any]:
    root = Path(repo_root)
    latest = json.loads((root / "docs/context-layer/latest-rhp.json").read_text(encoding="utf-8"))
    evidence = json.loads((root / latest["latest_evidence"]).read_text(encoding="utf-8"))
    return {
        "schema": RHP_OPERATOR_QUICKSTART_SCHEMA,
        "latest_operation": latest.get("latest_operation"),
        "latest_evidence": latest.get("latest_evidence"),
        "next_operation": latest.get("next_operation"),
        "authority_ok": latest.get("authority_ok") is True,
        "evidence_operation": evidence.get("operation"),
        "evidence_validation_passed": evidence.get("validation_passed") is True,
        "read_order": READ_ORDER,
        "output_grammar": OUTPUT_GRAMMAR,
        "authority_rules": AUTHORITY_RULES,
        "run_pattern": ["cd \"$env:USERPROFILE\\Downloads\"", "powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\\<NEXT_ALL_ONE>.ps1"],
        "non_claim_lock": "Quickstart is orientation only. It does not mutate files, execute repairs, call remote APIs, rerun CI, or grant authority.",
    }

def render_markdown(data: dict[str, Any]) -> str:
    read_rows = "\n".join(f"{idx}. `{item}`" for idx, item in enumerate(data["read_order"], start=1))
    grammar_rows = "\n".join(f"- `{key}`: {value}" for key, value in data["output_grammar"].items())
    authority_rows = "\n".join(f"- {item}" for item in data["authority_rules"])
    run_rows = "\n".join(data["run_pattern"])
    return "# RHP Operator Quickstart\n\n" + f"Schema: `{data['schema']}`\n\n" + f"Latest operation: `{data['latest_operation']}`\n" + f"Latest evidence: `{data['latest_evidence']}`\n" + f"Next operation: `{data['next_operation']}`\n\n" + "## Read order\n\n" + read_rows + "\n\n" + "## Output grammar\n\n" + grammar_rows + "\n\n" + "## Authority rules\n\n" + authority_rows + "\n\n" + "## Run pattern\n\n```powershell\n" + run_rows + "\n```\n\n" + f"Non-claim lock: {data['non_claim_lock']}\n"

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Render RHP operator quickstart")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--out-json", default="")
    parser.add_argument("--out-md", default="")
    args = parser.parse_args(argv)
    data = build_quickstart(args.repo_root)
    if args.out_json:
        out = Path(args.out_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.out_md:
        out = Path(args.out_md)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(data), encoding="utf-8", newline="\n")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    return 0 if data["authority_ok"] and data["evidence_validation_passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
