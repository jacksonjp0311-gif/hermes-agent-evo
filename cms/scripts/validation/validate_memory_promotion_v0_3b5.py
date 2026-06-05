
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "outputs" / "memory" / "latest_memory_promotion_report.json"
VALIDATION_JSON = ROOT / "reports" / "memory" / "latest_memory_promotion_validation.json"
VALIDATION_MD = ROOT / "reports" / "memory" / "latest_memory_promotion_validation.md"

VALID_ACTIONS = {"promoted", "downgraded", "observe_only", "blocked", "promote", "downgrade"}


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def first_present(item: dict[str, Any], keys: tuple[str, ...]) -> Any:
    for key in keys:
        if key in item:
            return item.get(key)
    return None


def normalize_action(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "promote":
        return "promoted"
    if text == "downgrade":
        return "downgraded"
    return text


def int_field(obj: dict[str, Any], key: str) -> int:
    try:
        return int(obj.get(key, 0))
    except Exception:
        return 0


def main() -> int:
    findings: list[str] = []
    obj = load_json(REPORT)

    if not obj:
        findings.append("missing_outputs_memory_latest_memory_promotion_report_json")

    if obj.get("schema") != "CMS-SA-v0.3b5-memory-promotion-report":
        findings.append("schema_mismatch")

    if obj.get("version") != "v0.3b5":
        findings.append("version_mismatch")

    candidates = obj.get("candidates", [])
    if not isinstance(candidates, list) or not candidates:
        findings.append("missing_candidates")
        candidates = []

    summary_promoted = int_field(obj, "promoted_count")
    summary_downgraded = int_field(obj, "downgraded_count")
    summary_observe_only = int_field(obj, "observe_only_count")
    summary_candidate_count = int_field(obj, "candidate_count")

    per_candidate_actions_seen = False
    promoted = 0
    downgraded = 0
    observe_only = 0
    blocked = 0

    for item in candidates:
        if not isinstance(item, dict):
            findings.append("candidate_not_object")
            continue

        cid = str(first_present(item, ("candidate_id", "id", "memory_id", "source")) or "unknown_candidate")
        action = normalize_action(first_present(item, ("memory_action", "promotion_action", "action", "decision", "status")))
        non_claim_lock = str(first_present(item, ("non_claim_lock", "non_claim_boundary", "claim_boundary")) or obj.get("non_claim_lock", ""))

        if action is not None:
            per_candidate_actions_seen = True
            if action not in VALID_ACTIONS:
                findings.append(f"{cid}:invalid_action:{action}")
            elif action == "promoted":
                promoted += 1
            elif action == "downgraded":
                downgraded += 1
            elif action == "observe_only":
                observe_only += 1
            elif action == "blocked":
                blocked += 1

        if "does not prove" not in non_claim_lock:
            findings.append(f"{cid}:missing_non_claim_lock")

    validation_mode = "per_candidate_actions" if per_candidate_actions_seen else "summary_counts"

    if not per_candidate_actions_seen:
        promoted = summary_promoted
        downgraded = summary_downgraded
        observe_only = summary_observe_only

    if summary_candidate_count != len(candidates):
        findings.append(f"candidate_count_mismatch:{summary_candidate_count}!={len(candidates)}")

    if promoted < 1:
        findings.append("no_promoted_memory_candidates")
    if downgraded < 1:
        findings.append("no_downgraded_memory_candidates")
    if observe_only < 1:
        findings.append("no_observe_only_memory_candidates")

    if obj.get("promoted_count") != promoted:
        findings.append(f"promoted_count_mismatch:{obj.get('promoted_count')}!={promoted}")
    if obj.get("downgraded_count") != downgraded:
        findings.append(f"downgraded_count_mismatch:{obj.get('downgraded_count')}!={downgraded}")
    if obj.get("observe_only_count") != observe_only:
        findings.append(f"observe_only_count_mismatch:{obj.get('observe_only_count')}!={observe_only}")

    if not obj.get("promotion_hash"):
        findings.append("missing_promotion_hash")
    if "does not prove" not in str(obj.get("non_claim_lock", "")):
        findings.append("missing_report_non_claim_lock")

    passed = len(findings) == 0 and obj.get("passed") is True

    result = {
        "schema": "CMS-SA-v0.3b5-memory-promotion-validation",
        "passed": passed,
        "version": obj.get("version"),
        "errors": len(findings),
        "findings": findings,
        "validation_mode": validation_mode,
        "candidate_count": len(candidates),
        "promoted_count": promoted,
        "downgraded_count": downgraded,
        "observe_only_count": observe_only,
        "blocked_count": blocked,
        "promotion_hash": obj.get("promotion_hash"),
        "non_claim_lock": "Memory promotion validation is repository-bound and does not prove code correctness.",
    }

    VALIDATION_JSON.parent.mkdir(parents=True, exist_ok=True)
    VALIDATION_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# CMS-SA v0.3b5 Memory Promotion Validation",
        "",
        f"- passed: `{passed}`",
        f"- errors: `{len(findings)}`",
        f"- validation_mode: `{validation_mode}`",
        f"- candidate_count: `{result['candidate_count']}`",
        f"- promoted_count: `{promoted}`",
        f"- downgraded_count: `{downgraded}`",
        f"- observe_only_count: `{observe_only}`",
        f"- blocked_count: `{blocked}`",
        f"- promotion_hash: `{result['promotion_hash']}`",
        "",
        "## Findings",
        "",
    ]
    if findings:
        lines.extend(f"- `{finding}`" for finding in findings)
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## Non-Claim Lock",
        "",
        result["non_claim_lock"],
        "",
    ])
    VALIDATION_MD.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
