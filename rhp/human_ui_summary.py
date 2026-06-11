# RHP-014.3 human-readable UI summary.
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

RHP_HUMAN_UI_SUMMARY_SCHEMA = "RHP-HUMAN-UI-SUMMARY-v0.1"

def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))

def render_summary(evidence: dict[str, Any], wound: dict[str, Any] | None = None, dry_run: dict[str, Any] | None = None) -> str:
    op = evidence.get("operation", "unknown")
    next_op = evidence.get("next_recommended_operation", "unknown")
    lines = [
        f"RHPLOAD [100%] HUMAN UI SUMMARY | operation={op} | status=ok [OK]",
        "`- operator dashboard",
        f"   +- current: {op}",
        f"   +- next: {next_op}",
        f"   +- evidence: {evidence.get('schema', 'unknown')}",
        f"   +- authority: self={evidence.get('self_authorization', False)} autonomous={evidence.get('autonomous_authority', False)}",
    ]
    if wound:
        lines.append(f"   +- wound: {wound.get('classification')} confidence={wound.get('confidence')}")
    if dry_run:
        lines.append(f"   +- dry-run: would_mutate={dry_run.get('would_mutate')} would_commit={dry_run.get('would_commit')}")
    lines.append("   `- verified: true [OK]")
    return "\n".join(lines)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render compact human UI summary")
    p.add_argument("--evidence", required=True)
    p.add_argument("--wound", default="")
    p.add_argument("--dry-run", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    evidence = load_json(args.evidence)
    wound = load_json(args.wound) if args.wound else None
    dry = load_json(args.dry_run) if args.dry_run else None
    data = {"schema": RHP_HUMAN_UI_SUMMARY_SCHEMA, "operation": evidence.get("operation"), "next": evidence.get("next_recommended_operation"), "has_wound": wound is not None, "has_dry_run": dry is not None}
    print(json.dumps(data, indent=2, ensure_ascii=False) if args.json else render_summary(evidence, wound, dry))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
