from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

RHP_GITHUB_SUMMARY_SCHEMA = "RHP-GITHUB-SUMMARY-v0.2"

def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def render_summary(evidence: dict[str, Any]) -> str:
    op = evidence.get("operation", "unknown")
    next_op = evidence.get("next_recommended_operation", "unknown")
    rows = [
        "| Field | Value |",
        "|---|---|",
        f"| Operation | `{op}` |",
        f"| Evidence schema | `{evidence.get('schema', 'unknown')}` |",
        f"| Focused tests | `{evidence.get('focused_tests_passed', False)}` |",
        f"| Validation | `{evidence.get('validation_passed', False)}` |",
        f"| Post-seal residue observer | `{evidence.get('post_seal_residue_observer_added', False)}` |",
        f"| Generated-source escape repair | `{evidence.get('generated_source_escape_repair', False)}` |",
        f"| Machine reports | `{evidence.get('machine_reports_are_evidence_only', False)}` |",
        f"| Authority: self | `{evidence.get('self_authorization', False)}` |",
        f"| Authority: autonomous | `{evidence.get('autonomous_authority', False)}` |",
        f"| Next | `{next_op}` |",
    ]
    return "\n".join([
        "# RHPLOAD GitHub Job Summary",
        "",
        f"Schema: `{RHP_GITHUB_SUMMARY_SCHEMA}`",
        "",
        *rows,
        "",
        "```text",
        f"RHPLOAD [100%] operation={op} status=ok [OK]",
        "machine-report box: GitHub summary rendered",
        "```",
        "",
        "Non-claim lock: this file is an evidence/report surface only. It does not mutate GitHub Actions, rerun workflows, grant authority, or execute repairs.",
        "",
    ])

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render RHP GitHub Actions job summary Markdown")
    p.add_argument("--evidence", required=True)
    p.add_argument("--out", default="")
    args = p.parse_args(argv)
    text = render_summary(load_json(args.evidence))
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text, encoding="utf-8", newline="\n")
    print(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
