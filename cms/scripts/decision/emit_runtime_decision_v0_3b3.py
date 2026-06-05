
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from cms.decision.kernel import VERSION, build_decision

ROOT = Path.cwd()
OUT_JSON = ROOT / "outputs/decision/latest_runtime_decision.json"
OUT_MD = ROOT / "outputs/decision/latest_runtime_decision.md"
REPORT_JSON = ROOT / "reports/decision/latest_runtime_decision.json"
REPORT_MD = ROOT / "reports/decision/latest_runtime_decision.md"
LEDGER = ROOT / "outputs/replay/runtime_decision_replay_ledger.jsonl"


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def write_md(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    failures = data.get("required_failures") or []
    lines = ["# CMS Runtime Decision", "", f"- Version: `{data['version']}`", f"- Decision: `{data['decision']}`", f"- Reason: `{data['reason']}`", f"- Next allowed action: `{data['next_allowed_action']}`", f"- Decision hash: `{data['decision_hash']}`", "", "## Required failures", ""]
    lines += [f"- `{x}`" for x in failures] if failures else ["- none"]
    lines += ["", "## Non-claim lock", "", data.get("non_claim_lock", ""), ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def last_hash(path: Path) -> str | None:
    if not path.exists(): return None
    lines = [x for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    if not lines: return None
    try: return json.loads(lines[-1]).get("decision_hash")
    except Exception: return None


def append_ledger(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    entry = {"timestamp": datetime.now(timezone.utc).isoformat(), "version": data["version"], "decision": data["decision"], "reason": data["reason"], "decision_hash": data["decision_hash"], "next_allowed_action": data["next_allowed_action"]}
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(entry, sort_keys=True) + "\n")


def main() -> None:
    decision = build_decision(ROOT, include_git_state=False)
    write_json(OUT_JSON, decision); write_json(REPORT_JSON, decision)
    write_md(OUT_MD, decision); write_md(REPORT_MD, decision)
    if last_hash(LEDGER) != decision["decision_hash"]:
        append_ledger(LEDGER, decision)
    print(json.dumps({"schema": "CMS-SA-v0.3b3-runtime-decision-emission", "passed": True, "version": VERSION, "decision": decision["decision"], "reason": decision["reason"], "decision_hash": decision["decision_hash"], "non_claim_lock": "Decision emission writes repository decision artifacts only."}, indent=2))

if __name__ == "__main__": main()
