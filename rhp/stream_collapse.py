# RHP-014.2 stream collapse.
from __future__ import annotations
import argparse, json, re, sys
from dataclasses import dataclass, field
from typing import Any

RHP_STREAM_COLLAPSE_SCHEMA = "RHP-STREAM-COLLAPSE-v0.1"
CRLF_RE = re.compile(r"warning: in the working copy of '([^']+)', LF will be replaced by CRLF", re.I)

@dataclass(frozen=True)
class StreamCollapse:
    schema: str
    total_lines: int
    visible_lines: int
    suppressed_lines: int
    crlf_warning_count: int
    git_status_count: int
    git_summary_count: int
    return_code: int = 0
    sample: list[str] = field(default_factory=list)
    ok: bool = True
    non_claim_lock: str = "Stream collapse is display-only. Raw output must remain available in evidence artifacts."

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def classify_line(line: str) -> str:
    s = line.strip()
    if not s:
        return "empty"
    if CRLF_RE.search(s):
        return "crlf_warning"
    if re.match(r"^[ MADRCU?!]{1,2}\s+.+", s):
        return "git_status"
    if "files changed" in s or "insertions" in s or "deletions" in s or s.startswith("[main "):
        return "git_summary"
    if s.startswith("To https://") or s.startswith("From https://") or " -> " in s or "FETCH_HEAD" in s:
        return "git_remote"
    return "normal"

def collapse(text: str, return_code: int = 0, sample_limit: int = 6) -> tuple[StreamCollapse, str]:
    lines = text.splitlines()
    visible: list[str] = []
    suppressed = 0
    crlf = 0
    status = 0
    summary = 0
    for line in lines:
        kind = classify_line(line)
        if kind in {"empty"}:
            suppressed += 1
            continue
        if kind == "crlf_warning":
            crlf += 1
            suppressed += 1
            continue
        if kind == "git_status":
            status += 1
            suppressed += 1
            continue
        if kind in {"git_summary", "git_remote"}:
            summary += 1
            suppressed += 1
            continue
        visible.append(line)
    result = StreamCollapse(
        RHP_STREAM_COLLAPSE_SCHEMA,
        len(lines),
        len(visible),
        suppressed,
        crlf,
        status,
        summary,
        return_code,
        visible[:sample_limit],
        return_code == 0,
    )
    box = [
        f"RHPLOAD [089%] loop=STREAM-COLLAPSE operation=RHP | status={'ok' if return_code == 0 else 'failed'} {'[OK]' if return_code == 0 else '[FAIL]'}",
        "`- stream collapse box",
        f"   +- total lines: {result.total_lines}",
        f"   +- suppressed lines: {result.suppressed_lines}",
        f"   +- CRLF warnings: {result.crlf_warning_count}",
        f"   +- git status lines: {result.git_status_count}",
        f"   +- git summary lines: {result.git_summary_count}",
        "   +- raw: evidence artifact",
        f"   `- verified: {str(result.ok).lower()} {'[OK]' if result.ok else '[FAIL]'}",
    ]
    if visible:
        box.append("   +- visible sample:")
        for item in visible[:sample_limit]:
            box.append(f"      | {item}")
    return result, "\n".join(box)

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Collapse noisy command output into a box")
    p.add_argument("--text", default="")
    p.add_argument("--return-code", type=int, default=0)
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    text = args.text or sys.stdin.read()
    result, rendered = collapse(text, args.return_code)
    print(json.dumps(result.as_dict(), indent=2, ensure_ascii=False) if args.json else rendered)
    return 0 if result.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
