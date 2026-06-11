import json
from pathlib import Path
from rhp.ci_pipeline_bridge import RHP_CI_PIPELINE_BRIDGE_SCHEMA, run_bridge

def test_rhp_014_4_bridge_builds_wound_dry_run_ui(tmp_path: Path):
    text = tmp_path / "ci.txt"
    text.write_text("ModuleNotFoundError: No module named 'rhp'", encoding="utf-8")
    evidence = tmp_path / "evidence.json"
    evidence.write_text(json.dumps({"operation": "RHP-014.4", "next_recommended_operation": "next", "schema": "evidence", "self_authorization": False, "autonomous_authority": False}), encoding="utf-8")
    out = tmp_path / "out"
    result = run_bridge(text, evidence, out)
    assert result["schema"] == RHP_CI_PIPELINE_BRIDGE_SCHEMA
    assert result["ok"] is True
    assert result["classification"] == "module_path_execution_bug"
    assert Path(result["human_ui_summary"]).exists()
