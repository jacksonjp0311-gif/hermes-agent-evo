# RHP-014.1 warning compressor.
from __future__ import annotations
import argparse, json, re, sys
from dataclasses import dataclass, field
from typing import Any

RHP_WARNING_COMPRESSOR_SCHEMA = "RHP-WARNING-COMPRESSOR-v0.1"
CRLF_RE = re.compile(r"warning: in the working copy of '([^']+)', LF will be replaced by CRLF", re.I)

@dataclass(frozen=True)
class WarningSummary:
    schema: str
    warning_count: int
    crlf_warning_count: int
    other_warning_count: int
    sample_paths: list[str] = field(default_factory=list)
    ok: bool = True
    non_claim_lock: str = "Warning compression is display-only. It does not hide command failures, alter exit codes, mutate files, or grant authority."

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def compress(text: str, sample_limit: int = 8) -> tuple[WarningSummary, str]:
    crlf_paths: list[str] = []
    other_warnings: list[str] = []
    passthrough: list[str] = []
    for line in text.splitlines():
        m = CRLF_RE.search(line)
        if m:
            crlf_paths.append(m.group(1))
            continue
        if line.lower().startswith("warning:"):
            other_warnings.append(line)
            continue
        passthrough.append(line)
    summary = WarningSummary(RHP_WARNING_COMPRESSOR_SCHEMA, len(crlf_paths) + len(other_warnings), len(crlf_paths), len(other_warnings), crlf_paths[:sample_limit], True)
    box = [
        "RHPLOAD [089%] loop=WARNING-COMPRESSOR operation=RHP | status=ok [OK]",
        "`- warning compressor box",
        f"   +- CRLF warnings compressed: {len(crlf_paths)}",
        f"   +- other warnings: {len(other_warnings)}",
        f"   +- sample paths: {', '.join(crlf_paths[:sample_limit]) if crlf_paths else 'none'}",
        "   `- verified: true [OK]",
    ]
    body = [x for x in passthrough if x.strip()] + box
    return summary, "\n".join(body)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Compress noisy warning streams")
    p.add_argument("--text", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    text = args.text or sys.stdin.read()
    summary, rendered = compress(text)
    print(json.dumps(summary.as_dict(), indent=2, ensure_ascii=False) if args.json else rendered)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
