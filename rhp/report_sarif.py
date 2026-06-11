from __future__ import annotations
import argparse, json
from pathlib import Path

RHP_SARIF_REPORT_SCHEMA = "RHP-SARIF-REPORT-v0.2"

def load_json(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def build_sarif(evidence: dict) -> dict:
    op = str(evidence.get("operation", "unknown"))
    rules = [
        {
            "id": "RHP-AUTHORITY-LOCKS",
            "shortDescription": {"text": "Authority locks must remain false"},
            "fullDescription": {"text": "RHP evidence must not assert autonomous, self-authorized, provider, model, CMS, memory, API, or external-ingestion authority."},
        },
        {
            "id": "RHP-VALIDATION",
            "shortDescription": {"text": "Validation must pass"},
            "fullDescription": {"text": "Focused validation and evidence validation must pass before push."},
        },
        {
            "id": "RHP-SCRIPT-EVIDENCE",
            "shortDescription": {"text": "Operator script must be recorded"},
            "fullDescription": {"text": "Final evidence must record operator_script_name for current-script gate verification."},
        },
    ]
    results = []
    if evidence.get("self_authorization") or evidence.get("autonomous_authority"):
        results.append({"ruleId": "RHP-AUTHORITY-LOCKS", "level": "error", "message": {"text": f"Authority drift detected in {op}"}})
    if not evidence.get("validation_passed", False):
        results.append({"ruleId": "RHP-VALIDATION", "level": "error", "message": {"text": f"Validation not confirmed for {op}"}})
    if not evidence.get("operator_script_name"):
        results.append({"ruleId": "RHP-SCRIPT-EVIDENCE", "level": "error", "message": {"text": f"operator_script_name missing for {op}"}})
    return {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [
            {
                "tool": {"driver": {"name": "RHPLOAD Machine Report", "informationUri": "https://github.com/jacksonjp0311-gif/hermes-agent-evo", "rules": rules}},
                "results": results,
                "properties": {
                    "rhp_schema": RHP_SARIF_REPORT_SCHEMA,
                    "operation": op,
                    "next": evidence.get("next_recommended_operation", "unknown"),
                    "non_claim_lock": "SARIF report is evidence/report output only. It does not execute repairs, mutate CI, or grant authority.",
                },
            }
        ],
    }

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render RHP SARIF report")
    p.add_argument("--evidence", required=True)
    p.add_argument("--out", default="")
    args = p.parse_args(argv)
    data = build_sarif(load_json(args.evidence))
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
