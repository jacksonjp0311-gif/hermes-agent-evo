
# RHP-013.7 RHPLOAD live console renderer and transcript.
from __future__ import annotations
import argparse, datetime, json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

RHPLOAD_LIVE_SCHEMA = "RHPLOAD-LIVE-CONSOLE-TRANSCRIPT-v0.1"

@dataclass(frozen=True)
class LoadEvent:
    percent: int
    label: str
    status: str
    loop: str
    operation: str
    detail: str = ""
    timestamp_utc: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": RHPLOAD_LIVE_SCHEMA,
            "timestamp_utc": self.timestamp_utc or datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "percent": self.percent,
            "label": self.label,
            "status": self.status,
            "loop": self.loop,
            "operation": self.operation,
            "detail": self.detail,
        }

def render_event(event: LoadEvent, *, expanded: bool = True) -> str:
    line = f"RHPLOAD [{event.percent:03d}%] {event.label} | loop={event.loop} operation={event.operation} | status={event.status}"
    if event.detail:
        line += f" | {event.detail}"
    if not expanded:
        return line
    return "\n".join([
        line,
        "`- live feedback",
        f"   +- loaded: {event.detail or 'current process state'}",
        f"   +- active: {event.label}",
        "   `- transcript: jsonl append-ready",
    ])

def append_event(path: str | Path, event: LoadEvent) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event.as_dict(), ensure_ascii=False) + "\n")

def read_transcript(path: str | Path) -> list[dict[str, Any]]:
    p = Path(path)
    if not p.exists():
        return []
    rows = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def summarize_transcript(path: str | Path) -> dict[str, Any]:
    rows = read_transcript(path)
    statuses = {}
    for row in rows:
        key = row.get("status", "unknown")
        statuses[key] = statuses.get(key, 0) + 1
    return {
        "schema": RHPLOAD_LIVE_SCHEMA,
        "event_count": len(rows),
        "last_percent": rows[-1].get("percent") if rows else None,
        "last_status": rows[-1].get("status") if rows else None,
        "status_counts": statuses,
        "ok": bool(rows) and rows[-1].get("status") in {"ok", "complete"},
    }

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="RHPLOAD live console renderer")
    p.add_argument("--percent", type=int, default=0)
    p.add_argument("--label", default="process")
    p.add_argument("--status", default="running")
    p.add_argument("--loop", default="DIAGNOSIS")
    p.add_argument("--operation", default="RHP")
    p.add_argument("--detail", default="")
    p.add_argument("--transcript", default="")
    p.add_argument("--summary", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    if args.summary:
        summary = summarize_transcript(args.transcript)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0 if summary.get("ok") else 1
    event = LoadEvent(args.percent, args.label, args.status, args.loop, args.operation, args.detail)
    if args.transcript:
        append_event(args.transcript, event)
    print(json.dumps(event.as_dict(), indent=2, ensure_ascii=False) if args.json else render_event(event))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
