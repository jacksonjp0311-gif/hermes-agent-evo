import json
from pathlib import Path
from rhp.autoheal_executor_dry_run import build_plan

def test_autoheal_executor_dry_run_blocks_execution(tmp_path: Path):
    ops = tmp_path / "docs" / "context-layer" / "ops"
    ops.mkdir(parents=True)
    evidence = {"operation": "RHP-TEST", "validation_passed": True, "ci_red_wound_observed": True, "self_authorization": False, "autonomous_authority": False}
    (ops / "RHP-TEST-final-evidence.json").write_text(json.dumps(evidence), encoding="utf-8")
    ctx = tmp_path / "docs" / "context-layer"
    ctx.mkdir(parents=True, exist_ok=True)
    (ctx / "latest-rhp.json").write_text(json.dumps({"latest_operation": "RHP-TEST", "latest_evidence": "docs/context-layer/ops/RHP-TEST-final-evidence.json", "next_operation": "RHP-NEXT"}), encoding="utf-8")
    plan = build_plan(tmp_path, ci_status="red")
    assert plan["dry_run_only"] is True
    assert plan["autoheal_execution_enabled"] is False
    assert any(action["step"] == "execute_patch" and not action["allowed"] for action in plan["actions"])
