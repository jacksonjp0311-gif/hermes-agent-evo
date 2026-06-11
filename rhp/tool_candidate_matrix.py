# RHP-014.2 tool candidate matrix.
from __future__ import annotations
import argparse, json
from typing import Any

RHP_TOOL_CANDIDATE_MATRIX_SCHEMA = "RHP-TOOL-CANDIDATE-MATRIX-v0.1"

CANDIDATES = [
    {
        "name": "GitHub Actions workflow commands",
        "loop_box": "CI-ANNOTATION-BOX",
        "purpose": "group logs, emit warnings/errors/notices, and write job summaries",
        "integration": "future CI workflow hardening",
        "authority": "ci_output_only",
    },
    {
        "name": "OpenTelemetry-style signals",
        "loop_box": "OBSERVABILITY-SIGNAL-BOX",
        "purpose": "represent RHPLOAD events as traces/logs/metrics",
        "integration": "future telemetry export",
        "authority": "local_evidence_only",
    },
    {
        "name": "Rich/Textual-style terminal UI",
        "loop_box": "OPERATOR-TUI-BOX",
        "purpose": "upgrade PowerShell boxes into richer local interface when available",
        "integration": "optional local UX",
        "authority": "display_only",
    },
    {
        "name": "SARIF/JUnit artifact outputs",
        "loop_box": "MACHINE-REPORT-BOX",
        "purpose": "make failures parseable by CI and future autoheal tools",
        "integration": "future CI red-job artifact extractor",
        "authority": "evidence_only",
    },
    {
        "name": "GitHub CLI / API watcher",
        "loop_box": "CI-WATCH-BOX",
        "purpose": "watch run IDs, jobs, annotations, and artifacts",
        "integration": "RHP-014.x CI wound packets",
        "authority": "read_only_until_authorized",
    },
]

def matrix() -> dict[str, Any]:
    return {"schema": RHP_TOOL_CANDIDATE_MATRIX_SCHEMA, "candidates": CANDIDATES}

def markdown_table() -> str:
    rows = ["| Candidate | Loop box | Purpose | Integration | Authority |", "|---|---|---|---|---|"]
    for item in CANDIDATES:
        rows.append(f"| {item['name']} | {item['loop_box']} | {item['purpose']} | {item['integration']} | {item['authority']} |")
    return "\n".join(rows)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render RHP tool candidate matrix")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    print(json.dumps(matrix(), indent=2, ensure_ascii=False) if args.json else markdown_table())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
