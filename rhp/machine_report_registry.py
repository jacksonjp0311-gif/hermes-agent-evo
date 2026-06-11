from __future__ import annotations
import argparse, json

RHP_MACHINE_REPORT_REGISTRY_SCHEMA = "RHP-MACHINE-REPORT-REGISTRY-v0.2"

REPORTS = [
    {"name": "github-summary", "module": "rhp.report_github_summary", "output": "github-step-summary.md", "status": "active", "purpose": "Human-readable GitHub Actions job summary Markdown.", "authority": "evidence_output_only"},
    {"name": "junit", "module": "rhp.report_junit", "output": "rhp-junit.xml", "status": "active", "purpose": "CI-readable test report surface.", "authority": "evidence_output_only"},
    {"name": "sarif", "module": "rhp.report_sarif", "output": "rhp-report.sarif.json", "status": "active", "purpose": "Machine-readable analysis/gate report surface.", "authority": "evidence_output_only"},
    {"name": "post-seal-residue", "module": "rhp.post_seal_residue", "output": "post-seal-residue-report.json", "status": "active", "purpose": "Classify bounded command residue created after seal/push boundaries.", "authority": "classification_only"},
]

def registry() -> dict:
    return {"schema": RHP_MACHINE_REPORT_REGISTRY_SCHEMA, "reports": REPORTS, "non_claim_lock": "Machine reports are evidence/report surfaces only. They do not mutate GitHub Actions, rerun workflows, execute repairs, or grant authority."}

def markdown_table() -> str:
    rows = ["| Report | Module | Output | Status | Authority |", "|---|---|---|---|---|"]
    for r in REPORTS:
        rows.append(f"| {r['name']} | `{r['module']}` | `{r['output']}` | {r['status']} | {r['authority']} |")
    return "\n".join(rows)

def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    print(json.dumps(registry(), indent=2, ensure_ascii=False) if args.json else markdown_table())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
