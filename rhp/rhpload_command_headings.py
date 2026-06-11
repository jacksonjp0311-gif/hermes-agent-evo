from __future__ import annotations
import argparse
import json
from typing import Any

SCHEMA = "RHPLOAD-COMMAND-HEADINGS-v0.1"
COMMAND_HEADINGS = {
    "pull-rebase-preauth": {"heading": "Pre-authorization sync with remote main", "why": "Avoid building on a stale base before human authorization.", "command": "git pull --rebase origin main"},
    "git-reset-index": {"heading": "Reset index before staged boundary", "why": "Ensure only current operation files are staged.", "command": "git reset"},
    "git-add": {"heading": "Stage allowed operation surfaces", "why": "Commit only bounded RHP operation artifacts.", "command": "git add -- <allowed paths>"},
    "commit": {"heading": "Create local evidence commit", "why": "Seal validated evidence into Git history before push.", "command": "git commit -m <message>"},
    "pull-rebase": {"heading": "Final remote integration before push", "why": "Avoid non-fast-forward drift after local commit.", "command": "git pull --rebase origin main"},
    "push": {"heading": "Push sealed evidence to origin/main", "why": "Publish the human-authorized bounded delta.", "command": "git push origin main"},
}

def heading_for(stage: str) -> dict[str, str]:
    return COMMAND_HEADINGS.get(stage, {"heading": f"Run command stage {stage}", "why": "No stage-specific heading has been registered yet.", "command": stage})

def registry() -> dict[str, Any]:
    return {"schema": SCHEMA, "headings": COMMAND_HEADINGS, "non_claim_lock": "Command headings are display metadata only. They do not execute commands or grant authority."}

def markdown_table() -> str:
    rows = ["| Stage | Heading | Why | Command |", "|---|---|---|---|"]
    for stage, data in COMMAND_HEADINGS.items():
        rows.append(f"| {stage} | {data['heading']} | {data['why']} | `{data['command']}` |")
    return "\n".join(rows)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render RHPLOAD command headings")
    p.add_argument("--stage", default="")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    data = heading_for(a.stage) if a.stage else registry()
    print(json.dumps(data, indent=2, ensure_ascii=False) if a.json else (data.get("heading") if a.stage else markdown_table()))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
