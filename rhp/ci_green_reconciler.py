from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import Any

RHP_CI_GREEN_RECONCILER_SCHEMA = "RHP-CI-GREEN-RECONCILER-v0.1"
VALID_STATUSES = {"green", "red", "unknown", "pending"}

def reconcile(repo_root: str | Path = ".", ci_status: str = "unknown") -> dict[str, Any]:
    if ci_status not in VALID_STATUSES:
        raise ValueError(f"ci_status must be one of {sorted(VALID_STATUSES)}")
    root = Path(repo_root)
    latest = json.loads((root / "docs/context-layer/latest-rhp.json").read_text(encoding="utf-8"))
    evidence = json.loads((root / latest["latest_evidence"]).read_text(encoding="utf-8"))
    local_ok = evidence.get("validation_passed") is True and evidence.get("focused_tests_passed") is True
    if ci_status == "green":
        next_action = "record remote green confirmation and proceed to next bounded evolution"
    elif ci_status == "red":
        next_action = "harvest failing CI log and create a wound packet before repair"
    elif ci_status == "pending":
        next_action = "wait for remote CI completion; do not patch blindly"
    else:
        next_action = "verify remote CI manually or via connector before declaring integration closure"
    return {
        "schema": RHP_CI_GREEN_RECONCILER_SCHEMA,
        "latest_operation": latest.get("latest_operation"),
        "latest_evidence": latest.get("latest_evidence"),
        "local_validation_ok": local_ok,
        "ci_status": ci_status,
        "integration_closed": local_ok and ci_status == "green",
        "next_action": next_action,
        "non_claim_lock": "CI reconciler records/operator-provided status only. It does not call GitHub, rerun CI, mutate workflows, or grant authority.",
    }

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Reconcile local RHP proof with operator-provided remote CI status")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--ci-status", default="unknown", choices=sorted(VALID_STATUSES))
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = reconcile(args.repo_root, args.ci_status)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if data["local_validation_ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
