# RHP-014.1 operator interface primitives.
from __future__ import annotations
import argparse, json
from dataclasses import dataclass
from typing import Any

RHP_OPERATOR_INTERFACE_SCHEMA = "RHP-OPERATOR-INTERFACE-v0.1"

@dataclass(frozen=True)
class BoxLine:
    percent: int
    loop: str
    operation: str
    title: str
    status: str
    detail: str = ""
    verified: bool = False

    def glyph(self) -> str:
        if self.status == "ok":
            return "[OK]"
        if self.status in {"running", "pending"}:
            return "[....]"
        if self.status == "warning":
            return "[WARN]"
        return "[BLOCKED]"

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": RHP_OPERATOR_INTERFACE_SCHEMA,
            "percent": self.percent,
            "loop": self.loop,
            "operation": self.operation,
            "title": self.title,
            "status": self.status,
            "detail": self.detail,
            "verified": self.verified,
            "glyph": self.glyph(),
        }

def render_box(line: BoxLine) -> str:
    return "\n".join([
        f"RHPLOAD [{line.percent:03d}%] loop={line.loop} operation={line.operation} | status={line.status} {line.glyph()}",
        f"`- {line.title}",
        f"   +- detail: {line.detail}",
        f"   `- verified: {str(line.verified).lower()} {line.glyph()}",
    ])

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render RHP operator interface box")
    p.add_argument("--percent", type=int, default=0)
    p.add_argument("--loop", default="DIAGNOSIS")
    p.add_argument("--operation", default="RHP")
    p.add_argument("--title", default="operator box")
    p.add_argument("--status", default="running")
    p.add_argument("--detail", default="")
    p.add_argument("--verified", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    line = BoxLine(args.percent, args.loop, args.operation, args.title, args.status, args.detail, args.verified)
    print(json.dumps(line.as_dict(), indent=2, ensure_ascii=False) if args.json else render_box(line))
    return 0 if args.status in {"ok", "running", "pending", "warning"} else 1

if __name__ == "__main__":
    raise SystemExit(main())
