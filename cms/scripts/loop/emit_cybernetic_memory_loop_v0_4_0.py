from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from cms.loop import build_cybernetic_memory_loop


ROOT = Path(__file__).resolve().parents[2]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, obj: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# CMS-SA v0.4.0 Cybernetic Memory Loop",
        "",
        f"- schema: `{obj['schema']}`",
        f"- version: `{obj['version']}`",
        f"- passed: `{obj['passed']}`",
        f"- loop_closed: `{obj['loop_closed']}`",
        f"- decision_state: `{obj['decision_state']}`",
        f"- loop_hash: `{obj['loop_hash']}`",
        "",
        "## Memory Counts",
        "",
        f"- candidate_count: `{obj['memory_counts']['candidate_count']}`",
        f"- promoted_count: `{obj['memory_counts']['promoted_count']}`",
        f"- downgraded_count: `{obj['memory_counts']['downgraded_count']}`",
        f"- observe_only_count: `{obj['memory_counts']['observe_only_count']}`",
        "",
        "## Next-Cycle Influence",
        "",
        f"- allowed: `{obj['next_cycle_influence']['allowed']}`",
        f"- mode: `{obj['next_cycle_influence']['mode']}`",
        f"- hard_boundary: `{obj['next_cycle_influence']['hard_boundary']}`",
        "",
        "## Core Law",
        "",
        obj["core_law"],
        "",
        "## Non-Claim Lock",
        "",
        obj["non_claim_lock"],
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    memory = load_json(ROOT / "outputs/memory/latest_memory_promotion_report.json")
    decision = load_json(ROOT / "outputs/decision/latest_runtime_decision.json")
    controls = load_json(ROOT / "outputs/controls/latest_negative_control_harness.json")
    obj = build_cybernetic_memory_loop(memory, decision, controls)
    write_json(ROOT / "outputs/loop/latest_cybernetic_memory_loop.json", obj)
    write_json(ROOT / "reports/loop/latest_cybernetic_memory_loop.json", obj)
    write_md(ROOT / "reports/loop/latest_cybernetic_memory_loop.md", obj)
    print(json.dumps({
        "schema": "CMS-SA-v0.4.0-cybernetic-memory-loop-emission",
        "passed": obj["passed"],
        "version": obj["version"],
        "loop_closed": obj["loop_closed"],
        "loop_hash": obj["loop_hash"],
        "next_cycle_influence_allowed": obj["next_cycle_influence"]["allowed"],
        "non_claim_lock": obj["non_claim_lock"],
    }, indent=2, sort_keys=True))
    return 0 if obj["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
