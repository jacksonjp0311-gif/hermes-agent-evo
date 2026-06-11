from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

RHP_COMPACT_OUTPUT_SCHEMA = "RHP-COMPACT-OUTPUT-v0.1"


def summarize(records: list[dict[str, Any]], *, operation: str, group: str) -> dict[str, Any]:
    failed = [record for record in records if int(record.get("exit", 1)) != 0]
    return {
        "schema": RHP_COMPACT_OUTPUT_SCHEMA,
        "operation": operation,
        "group": group,
        "total": len(records),
        "ok": len(records) - len(failed),
        "failed": len(failed),
        "records": records,
        "terminal_contract": "Use RHPDROP [closed] for repetitive command groups; keep raw command output in files and expose raw-index path.",
    }


def render_closed(summary: dict[str, Any]) -> str:
    status = "ok" if summary.get("failed") == 0 else "failed"
    glyph = "[OK]" if status == "ok" else "[FAIL]"
    return "\n".join([
        f"RHPDROP [closed] group={summary['group']} operation={summary['operation']} | status={status} {glyph}",
        "`- compact command summary",
        f"   +- commands: {summary['total']}",
        f"   +- ok: {summary['ok']}",
        f"   +- failed: {summary['failed']}",
        "   `- expand: open raw-index for full command details",
    ])


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Render an RHP compact output summary")
    parser.add_argument("--records", required=True)
    parser.add_argument("--operation", required=True)
    parser.add_argument("--group", required=True)
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    records = json.loads(Path(args.records).read_text(encoding="utf-8"))
    summary = summarize(records, operation=args.operation, group=args.group)
    text = json.dumps(summary, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(render_closed(summary))
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
