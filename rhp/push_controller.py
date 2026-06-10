
# RHP-014.0 GitHub Push Box controller.
from __future__ import annotations
import argparse, json
from dataclasses import dataclass, field
from typing import Any

RHP_PUSH_CONTROLLER_SCHEMA = "RHP-GITHUB-PUSH-BOX-v0.1"

@dataclass(frozen=True)
class PushStage:
    stage: str
    status: str
    detail: str
    verified: bool
    glyph: str

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

@dataclass(frozen=True)
class PushBox:
    schema: str
    ok: bool
    operation: str
    stages: list[PushStage] = field(default_factory=list)
    non_claim_lock: str = (
        "GitHub Push Box is operator-visible push sequencing only. It does not bypass tests, evidence, secret scans, human authorization, or CI gates."
    )

    def as_dict(self) -> dict[str, Any]:
        return {"schema": self.schema, "ok": self.ok, "operation": self.operation, "stages": [s.as_dict() for s in self.stages], "non_claim_lock": self.non_claim_lock}

def stage(stage: str, status: str, detail: str = "") -> PushStage:
    glyph = "[OK]" if status == "ok" else "[....]" if status == "running" else "[BLOCKED]" if status == "blocked" else "[FAIL]"
    return PushStage(stage, status, detail, status == "ok", glyph)

def render_stage(operation: str, item: PushStage, percent: int) -> str:
    lines = [
        f"RHPLOAD [{percent:03d}%] GITHUB PUSH | stage={item.stage} | operation={operation} | status={item.status} {item.glyph}",
        "`- github push box",
        f"   +- stage: {item.stage}",
        f"   +- detail: {item.detail}",
        "   +- stream: compressed",
        f"   `- verified: {str(item.verified).lower()} {item.glyph}",
    ]
    return "\n".join(lines)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Render a GitHub push box stage")
    p.add_argument("--operation", default="RHP")
    p.add_argument("--stage", required=True)
    p.add_argument("--status", required=True)
    p.add_argument("--detail", default="")
    p.add_argument("--percent", type=int, default=90)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    item = stage(args.stage, args.status, args.detail)
    box = PushBox(RHP_PUSH_CONTROLLER_SCHEMA, item.status == "ok", args.operation, [item])
    print(json.dumps(box.as_dict(), indent=2, ensure_ascii=False) if args.json else render_stage(args.operation, item, args.percent))
    return 0 if item.status == "ok" else 1

if __name__ == "__main__":
    raise SystemExit(main())
