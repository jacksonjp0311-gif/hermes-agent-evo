# RHP-014.4 CI ingestion source router.
from __future__ import annotations
import argparse, json, subprocess, shutil, sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RHP_CI_INGEST_SCHEMA = "RHP-CI-INGEST-v0.1"

@dataclass(frozen=True)
class CIIngestPacket:
    schema: str
    ok: bool
    source_mode: str
    source_ref: str
    normalized_text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    non_claim_lock: str = (
        "CI ingest packets normalize local or read-only CI artifacts only. They do not mutate CI, rerun workflows, "
        "write remote APIs, grant authority, or execute repairs."
    )

    def as_dict(self) -> dict[str, Any]:
        data = dict(self.__dict__)
        data["normalized_text_preview"] = self.normalized_text[:800]
        data["normalized_text_length"] = len(self.normalized_text)
        data.pop("normalized_text", None)
        return data

def ingest_text(text: str, source_ref: str = "inline-text") -> CIIngestPacket:
    return CIIngestPacket(RHP_CI_INGEST_SCHEMA, True, "text", source_ref, text, {"bytes": len(text.encode("utf-8", errors="replace"))})

def ingest_file(path: str | Path) -> CIIngestPacket:
    p = Path(path)
    text = p.read_text(encoding="utf-8", errors="replace")
    return CIIngestPacket(RHP_CI_INGEST_SCHEMA, True, "file", str(p), text, {"bytes": p.stat().st_size})

def ingest_github_json(path: str | Path) -> CIIngestPacket:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
    lines: list[str] = []
    if isinstance(data, dict):
        for key in ("name", "displayTitle", "status", "conclusion", "event", "headSha", "url"):
            if key in data:
                lines.append(f"{key}: {data[key]}")
        jobs = data.get("jobs") or data.get("workflow_jobs") or []
        if isinstance(jobs, list):
            for job in jobs:
                if isinstance(job, dict):
                    lines.append(f"job: {job.get('name')} status={job.get('status')} conclusion={job.get('conclusion')}")
                    for step in job.get("steps", []) or []:
                        if isinstance(step, dict):
                            lines.append(f"step: {step.get('name')} status={step.get('status')} conclusion={step.get('conclusion')}")
    text = "\n".join(lines) if lines else json.dumps(data, indent=2, ensure_ascii=False)
    return CIIngestPacket(RHP_CI_INGEST_SCHEMA, True, "github-json", str(p), text, {"json_keys": list(data.keys()) if isinstance(data, dict) else []})

def gh_available() -> bool:
    return shutil.which("gh") is not None

def build_gh_command(run_id: str, repo: str = "") -> list[str]:
    cmd = ["gh", "run", "view", run_id, "--json", "name,displayTitle,status,conclusion,event,headSha,url,jobs"]
    if repo:
        cmd.extend(["--repo", repo])
    return cmd

def ingest_gh_run(run_id: str, repo: str = "") -> CIIngestPacket:
    if not gh_available():
        return CIIngestPacket(RHP_CI_INGEST_SCHEMA, False, "gh-run", run_id, "", {"error": "gh_cli_unavailable", "suggested_fallback": "export gh run view JSON to file and use --github-json"})
    cmd = build_gh_command(run_id, repo)
    p = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        return CIIngestPacket(RHP_CI_INGEST_SCHEMA, False, "gh-run", run_id, p.stdout, {"return_code": p.returncode, "command": cmd})
    tmp = json.loads(p.stdout)
    lines = []
    for key in ("name", "displayTitle", "status", "conclusion", "event", "headSha", "url"):
        if key in tmp:
            lines.append(f"{key}: {tmp[key]}")
    for job in tmp.get("jobs", []) or []:
        lines.append(f"job: {job.get('name')} status={job.get('status')} conclusion={job.get('conclusion')}")
        for step in job.get("steps", []) or []:
            lines.append(f"step: {step.get('name')} status={step.get('status')} conclusion={step.get('conclusion')}")
    return CIIngestPacket(RHP_CI_INGEST_SCHEMA, True, "gh-run", run_id, "\n".join(lines), {"command": cmd, "read_only": True})

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Ingest CI artifacts from local text/file/GitHub JSON/optional gh CLI")
    src = p.add_mutually_exclusive_group(required=True)
    src.add_argument("--text", default="")
    src.add_argument("--file", default="")
    src.add_argument("--github-json", default="")
    src.add_argument("--gh-run-id", default="")
    p.add_argument("--repo", default="")
    p.add_argument("--out-text", default="")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)
    if args.text:
        packet = ingest_text(args.text)
    elif args.file:
        packet = ingest_file(args.file)
    elif args.github_json:
        packet = ingest_github_json(args.github_json)
    else:
        packet = ingest_gh_run(args.gh_run_id, args.repo)
    if args.out_text:
        Path(args.out_text).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out_text).write_text(packet.normalized_text, encoding="utf-8", newline="\n")
    print(json.dumps(packet.as_dict(), indent=2, ensure_ascii=False))
    return 0 if packet.ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
