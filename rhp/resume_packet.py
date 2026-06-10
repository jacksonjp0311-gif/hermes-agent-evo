
# RHP-013.8 transcript-backed resume packet.
from __future__ import annotations
import argparse, json
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from rhp.loop_registry import build_registry

RHP_RESUME_PACKET_SCHEMA = "RHP-RESUME-PACKET-v0.1"

@dataclass(frozen=True)
class ResumePacket:
    schema: str
    repo_root: str
    latest_evidence: str
    latest_operation: str
    latest_next: str
    latest_transcript: str
    transcript_event_count: int
    transcript_last_percent: int | None
    transcript_last_status: str | None
    recommended_loop: str
    allowed_next_loops: list[str]
    authority: dict[str, bool]
    non_claim_lock: str = "Resume packets summarize state only. They grant no runtime, tool, CMS, memory, API, external-ingestion, autonomous, or self-authorization authority."

    def as_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)

def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def _version_key(path: Path) -> tuple[int, int, int]:
    stem = path.name.replace("RHP-", "").replace("-final-evidence.json", "")
    out = []
    for item in stem.split("-"):
        try:
            out.append(int(item))
        except ValueError:
            out.append(0)
    while len(out) < 3:
        out.append(0)
    return tuple(out[:3])

def find_latest_evidence(root: str | Path) -> Path:
    base = Path(root)
    candidates = sorted((base / "docs" / "context-layer" / "ops").glob("RHP-*-final-evidence.json"), key=_version_key)
    if not candidates:
        raise FileNotFoundError("no RHP final evidence found")
    return candidates[-1]

def find_latest_transcript(root: str | Path) -> Path | None:
    base = Path(root)
    matches = sorted(base.glob("docs/context-layer/ops/RHP-*/**/rhpload-transcript.jsonl"))
    return matches[-1] if matches else None

def read_transcript(path: Path | None) -> list[dict[str, Any]]:
    if path is None or not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def recommend_loop(evidence: dict[str, Any], rows: list[dict[str, Any]]) -> str:
    next_text = str(evidence.get("next_recommended_operation", "")).lower()
    if "autoheal" in next_text:
        return "AUTOHEAL-PLAN"
    if "ci" in next_text:
        return "CI-WATCH"
    if rows and rows[-1].get("status") not in {"ok", "complete"}:
        return "DIAGNOSIS"
    return "EVOLUTION"

def build_resume_packet(root: str | Path) -> ResumePacket:
    root_path = Path(root).resolve()
    evidence_path = find_latest_evidence(root_path)
    evidence = _load_json(evidence_path)
    transcript_path = find_latest_transcript(root_path)
    rows = read_transcript(transcript_path)
    loop = recommend_loop(evidence, rows)
    reg = build_registry()
    allowed_next = reg[loop].allowed_next if loop in reg else ["DIAGNOSIS"]
    authority = {key: bool(evidence.get(key, False)) for key in [
        "provider_call_executed", "model_call_executed", "tool_use_executed",
        "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
        "api_write", "external_ingestion", "autonomous_authority", "self_authorization"
    ]}
    return ResumePacket(
        schema=RHP_RESUME_PACKET_SCHEMA,
        repo_root=str(root_path),
        latest_evidence=str(evidence_path.relative_to(root_path)),
        latest_operation=str(evidence.get("operation", "")),
        latest_next=str(evidence.get("next_recommended_operation", "")),
        latest_transcript=str(transcript_path.relative_to(root_path)) if transcript_path else "",
        transcript_event_count=len(rows),
        transcript_last_percent=rows[-1].get("percent") if rows else None,
        transcript_last_status=rows[-1].get("status") if rows else None,
        recommended_loop=loop,
        allowed_next_loops=allowed_next,
        authority=authority,
    )

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Build transcript-backed RHP resume packet")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    packet = build_resume_packet(args.repo_root)
    print(json.dumps(packet.as_dict(), indent=2, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
