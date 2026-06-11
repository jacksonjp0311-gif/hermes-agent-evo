# RHP platform tool registry.
from __future__ import annotations
import argparse, json
from typing import Any

RHP_PLATFORM_TOOL_REGISTRY_SCHEMA = "RHP-PLATFORM-TOOL-REGISTRY-v0.3"

TOOLS = [
    {"tool": "local-paste-fallback", "box": "CI-INGEST-BOX", "status": "active", "authority": "local_file_read", "purpose": "accept copied CI logs/screenshots text as wound-packet input"},
    {"tool": "github-json-file", "box": "CI-INGEST-BOX", "status": "active", "authority": "local_file_read", "purpose": "accept exported GitHub run/job JSON without network dependency"},
    {"tool": "gh-cli-run-view", "box": "CI-INGEST-BOX", "status": "optional_read_only", "authority": "read_only_when_user_has_gh_auth", "purpose": "read workflow run metadata when GitHub CLI is installed"},
    {"tool": "github-actions-summary", "box": "CI-ANNOTATION-BOX", "status": "active", "authority": "evidence_output_only", "purpose": "write RHPLOAD boxes into GitHub job summaries when a workflow later calls the report module"},
    {"tool": "sarif-junit-export", "box": "MACHINE-REPORT-BOX", "status": "active", "authority": "evidence_output_only", "purpose": "emit parseable machine reports for CI and autoheal diagnosis"},
    {"tool": "post-seal-residue", "box": "POST-SEAL-RESIDUE-BOX", "status": "active", "authority": "classification_only", "purpose": "classify bounded command streams that are created after commit/push boundaries"},
    {"tool": "operator-dashboard-bundle", "box": "OPERATOR-DASHBOARD-BOX", "status": "active", "authority": "orientation_only", "purpose": "join evidence, transcript, wound, dry-run, residue, authority, tools, and geometry into one operator bundle"},
    {"tool": "loop-geometry", "box": "GEOMETRY-BOX", "status": "active", "authority": "orientation_only", "purpose": "make the RHP loop shape readable without granting autonomy"},
    {"tool": "rhpwait-fill-progress", "box": "UI-WAIT-BOX", "status": "active", "authority": "display_only", "purpose": "show single-line fill progress while RHPLOAD remains stable audit output"},
]

def registry() -> dict[str, Any]:
    return {"schema": RHP_PLATFORM_TOOL_REGISTRY_SCHEMA, "tools": TOOLS}

def markdown_table() -> str:
    rows = ["| Tool | Box | Status | Authority | Purpose |", "|---|---|---|---|---|"]
    for item in TOOLS:
        rows.append(f"| {item['tool']} | {item['box']} | {item['status']} | {item['authority']} | {item['purpose']} |")
    return "\n".join(rows)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render platform tool registry")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    print(json.dumps(registry(), indent=2, ensure_ascii=False) if args.json else markdown_table())
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
