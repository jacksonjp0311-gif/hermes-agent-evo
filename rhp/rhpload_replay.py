from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

RHPLOAD_REPLAY_SCHEMA = "RHPLOAD-REPLAY-v0.1"


def _find_evidence_for_operation(root: Path, operation: str) -> Path | None:
    for path in sorted((root / "docs/context-layer/ops").glob("RHP-*-final-evidence.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if data.get("operation") == operation:
            return path
    return None


def replay(repo_root: str | Path = ".", operation: str = "") -> dict[str, Any]:
    root = Path(repo_root)
    pointer_path = root / "docs/context-layer/latest-rhp.json"
    pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
    if not operation:
        operation = pointer.get("latest_operation", "")
        evidence_rel = pointer.get("latest_evidence", "")
        evidence_path = root / evidence_rel
    else:
        evidence_path = _find_evidence_for_operation(root, operation) or Path("")

    required: dict[str, bool] = {
        "latest_pointer": pointer_path.exists(),
        "final_evidence": evidence_path.exists(),
        "zero_context": (root / "docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md").exists(),
        "operator_dashboard": (root / "docs/context-layer/operator-dashboard.txt").exists(),
    }
    evidence = {}
    command_summaries: list[str] = []
    if evidence_path.exists():
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        op_number = operation.replace(".", "-")
        ops_root = root / "docs/context-layer/ops"
        for path in sorted(ops_root.rglob("*command-summary.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if data.get("operation") == operation:
                command_summaries.append(str(path.relative_to(root)))
    required["command_summary"] = bool(command_summaries)
    found = sum(1 for ok in required.values() if ok)
    total = len(required)
    return {
        "schema": RHPLOAD_REPLAY_SCHEMA,
        "operation": operation,
        "ok": found == total,
        "replay_completeness": found / total,
        "required": required,
        "latest_pointer": str(pointer_path.relative_to(root)),
        "final_evidence": str(evidence_path.relative_to(root)) if evidence_path.exists() else "",
        "command_summaries": command_summaries,
        "evidence_summary": {
            "operation": evidence.get("operation"),
            "validation_passed": evidence.get("validation_passed"),
            "focused_tests_passed": evidence.get("focused_tests_passed"),
            "next": evidence.get("next_recommended_operation"),
        },
        "non_claim_lock": "Replay reconstructs local evidence references only. It does not execute commands, call remote APIs, rerun CI, mutate files, or grant authority.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Replay/reconstruct an RHP operation from local evidence")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--operation", default="")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = replay(args.repo_root, args.operation)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
