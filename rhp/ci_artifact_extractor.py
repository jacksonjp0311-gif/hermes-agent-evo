# RHP-014.3 CI artifact extractor.
from __future__ import annotations
import argparse, json, re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RHP_CI_WOUND_PACKET_SCHEMA = "RHP-CI-WOUND-PACKET-v0.1"

@dataclass(frozen=True)
class CIWoundPacket:
    schema: str
    ok: bool
    classification: str
    confidence: float
    source_kind: str
    summary: str
    evidence_lines: list[str] = field(default_factory=list)
    suggested_loop: str = "AUTOHEAL-PLAN"
    non_claim_lock: str = "CI wound packets classify CI artifacts only. They do not mutate files, call remote APIs, grant authority, or execute repairs."

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def _interesting_lines(text: str, limit: int = 12) -> list[str]:
    needles = ("error", "failed", "failure", "assert", "modulenotfounderror", "keyerror", "traceback", "current-script", "warning", "timeout", "no module named")
    out = []
    for line in text.splitlines():
        s = line.strip()
        if any(n in s.lower() for n in needles):
            out.append(s[:240])
        if len(out) >= limit:
            break
    return out

def classify_ci_text(text: str, source_kind: str = "pasted-log") -> CIWoundPacket:
    lower = text.lower()
    lines = _interesting_lines(text)
    if "modulenotfounderror" in lower or "no module named" in lower:
        return CIWoundPacket(RHP_CI_WOUND_PACKET_SCHEMA, True, "module_path_execution_bug", 0.92, source_kind, "Python package/module execution path failure.", lines)
    if "current-script" in lower or "actual_script_mismatch" in lower or "evidence_script_mismatch" in lower:
        return CIWoundPacket(RHP_CI_WOUND_PACKET_SCHEMA, True, "current_script_identity_mismatch", 0.93, source_kind, "Current script gate or evidence identity mismatch.", lines)
    if "lf will be replaced by crlf" in lower or "stream collapse" in lower:
        return CIWoundPacket(RHP_CI_WOUND_PACKET_SCHEMA, True, "stream_output_leak_or_crlf_noise", 0.87, source_kind, "Noisy command stream or CRLF warning leakage.", lines)
    if "assertionerror" in lower or "assert " in lower or "assertion failed" in lower:
        return CIWoundPacket(RHP_CI_WOUND_PACKET_SCHEMA, True, "assertion_failure", 0.84, source_kind, "Test assertion failure requiring bounded diagnosis.", lines)
    if "keyerror" in lower:
        return CIWoundPacket(RHP_CI_WOUND_PACKET_SCHEMA, True, "stale_evidence_key_surface", 0.86, source_kind, "Stale evidence key or guard/test surface mismatch.", lines)
    if "timed out" in lower or "timeout" in lower:
        return CIWoundPacket(RHP_CI_WOUND_PACKET_SCHEMA, True, "timeout_or_flaky_suspected", 0.72, source_kind, "Timeout or flaky execution suspected.", lines)
    if "failed" in lower or "error" in lower:
        return CIWoundPacket(RHP_CI_WOUND_PACKET_SCHEMA, True, "unknown_ci_failure", 0.55, source_kind, "CI failed but no known bounded class matched.", lines, "DIAGNOSIS")
    return CIWoundPacket(RHP_CI_WOUND_PACKET_SCHEMA, True, "no_failure_detected", 0.66, source_kind, "No failure signature detected.", lines, "NO-OP")

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Extract RHP CI wound packet from CI text")
    p.add_argument("--text", default="")
    p.add_argument("--file", default="")
    p.add_argument("--source-kind", default="pasted-log")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    text = args.text
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8", errors="replace")
    packet = classify_ci_text(text, args.source_kind)
    print(json.dumps(packet.as_dict(), indent=2, ensure_ascii=False))
    return 0 if packet.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
