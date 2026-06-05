
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from cms.controls import build_negative_control_harness  # noqa: E402

def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def write_md(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# CMS-SA v0.3b4 Negative Control and Downgrade Harness",
        "",
        f"- schema: `{obj['schema']}`",
        f"- version: `{obj['version']}`",
        f"- passed: `{obj['passed']}`",
        f"- control_count: `{obj['control_count']}`",
        f"- false_promote_rejected: `{obj['false_promote_rejected']}`",
        f"- downgrade_preserved: `{obj['downgrade_preserved']}`",
        f"- observe_only_preserved: `{obj['observe_only_preserved']}`",
        f"- harness_hash: `{obj['harness_hash']}`",
        "",
        "## Controls",
        "",
        "| Control | Class | Expected | Observed | Passed |",
        "|---|---|---:|---:|---:|",
    ]
    for item in obj["controls"]:
        lines.append(f"| `{item['control_id']}` | `{item['control_class']}` | `{item['expected_decision']}` | `{item['observed_decision']}` | `{item['passed']}` |")
    lines.extend(["", "## Non-Claim Lock", "", obj["non_claim_lock"], ""])
    path.write_text("\n".join(lines), encoding="utf-8")

def main() -> int:
    obj = build_negative_control_harness()
    write_json(ROOT / "outputs/controls/latest_negative_control_harness.json", obj)
    write_json(ROOT / "reports/controls/latest_negative_control_harness.json", obj)
    write_md(ROOT / "reports/controls/latest_negative_control_harness.md", obj)
    result = {
        "schema": "CMS-SA-v0.3b4-negative-control-emission",
        "passed": obj["passed"],
        "version": obj["version"],
        "control_count": obj["control_count"],
        "false_promote_rejected": obj["false_promote_rejected"],
        "downgrade_preserved": obj["downgrade_preserved"],
        "observe_only_preserved": obj["observe_only_preserved"],
        "harness_hash": obj["harness_hash"],
        "non_claim_lock": obj["non_claim_lock"],
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if obj["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
