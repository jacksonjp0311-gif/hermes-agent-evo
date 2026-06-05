from __future__ import annotations

import json
from pathlib import Path

from cms.memory.actions import build_candidate_memory_actions


ROOT = Path(__file__).resolve().parents[2]


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# CMS-SA v0.4.1 Candidate Memory Actions",
        "",
        f"- passed: `{obj['passed']}`",
        f"- candidate_action_count: `{obj['candidate_action_count']}`",
        f"- action_hash: `{obj['action_hash']}`",
        "",
        "## Actions",
        "",
    ]
    for action in obj["actions"]:
        lines.append(f"- `{action['candidate_id']}` -> `{action['memory_decision']}` / `{action['allowed_next_action']}`")
    lines.extend(["", "## Primary Lock", "", obj["primary_lock"], "", "## Non-Claim Lock", "", obj["non_claim_lock"], ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    memory = load_json(ROOT / "outputs/memory/latest_memory_promotion_report.json")
    loop = load_json(ROOT / "outputs/loop/latest_cybernetic_memory_loop.json")
    obj = build_candidate_memory_actions(memory, loop)

    write_json(ROOT / "outputs/memory/latest_candidate_memory_actions.json", obj)
    write_json(ROOT / "reports/memory/latest_candidate_memory_actions.json", obj)
    write_md(ROOT / "reports/memory/latest_candidate_memory_actions.md", obj)

    print(json.dumps({
        "schema": "CMS-SA-v0.4.1-candidate-memory-action-emission",
        "passed": obj["passed"],
        "version": obj["version"],
        "candidate_action_count": obj["candidate_action_count"],
        "action_hash": obj["action_hash"],
        "non_claim_lock": obj["non_claim_lock"],
    }, indent=2, sort_keys=True))
    return 0 if obj["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
