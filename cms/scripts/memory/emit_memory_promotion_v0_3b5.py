
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from cms.memory import build_memory_promotion_report  # noqa: E402


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# CMS-SA v0.3b5 Memory Promotion Report",
        "",
        f"- schema: `{obj['schema']}`",
        f"- version: `{obj['version']}`",
        f"- passed: `{obj['passed']}`",
        f"- candidate_count: `{obj['candidate_count']}`",
        f"- promoted_count: `{obj['promoted_count']}`",
        f"- downgraded_count: `{obj['downgraded_count']}`",
        f"- observe_only_count: `{obj['observe_only_count']}`",
        f"- blocked_count: `{obj['blocked_count']}`",
        f"- promotion_hash: `{obj['promotion_hash']}`",
        "",
        "## Candidates",
        "",
        "| Candidate | Decision | Utility | Source |",
        "|---|---|---:|---|",
    ]
    for item in obj["candidates"]:
        lines.append(
            f"| `{item['candidate_id']}` | `{item['memory_decision']}` | "
            f"`{item['evidence_utility']}` | {item['source']} |"
        )
    lines.extend([
        "",
        "## Core Rule",
        "",
        obj["core_rule"],
        "",
        "## Non-Claim Lock",
        "",
        obj["non_claim_lock"],
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    obj = build_memory_promotion_report()
    write_json(ROOT / "outputs/memory/latest_memory_promotion_report.json", obj)
    write_json(ROOT / "reports/memory/latest_memory_promotion_report.json", obj)
    write_md(ROOT / "reports/memory/latest_memory_promotion_report.md", obj)
    print(json.dumps({
        "schema": "CMS-SA-v0.3b5-memory-promotion-emission",
        "passed": obj["passed"],
        "version": obj["version"],
        "candidate_count": obj["candidate_count"],
        "promoted_count": obj["promoted_count"],
        "downgraded_count": obj["downgraded_count"],
        "observe_only_count": obj["observe_only_count"],
        "promotion_hash": obj["promotion_hash"],
        "non_claim_lock": obj["non_claim_lock"],
    }, indent=2, sort_keys=True))
    return 0 if obj["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
