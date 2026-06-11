import json
from pathlib import Path

from rhp.operator_dashboard_bundle import build_bundle, render_markdown


def test_operator_dashboard_bundle_from_latest_pointer(tmp_path: Path):
    ops = tmp_path / "docs" / "context-layer" / "ops"
    ops.mkdir(parents=True)
    evidence = {
        "schema": "RHP-014.7-final-evidence",
        "operation": "RHP-014.7",
        "validation_passed": True,
        "focused_tests_passed": True,
        "next_recommended_operation": "RHP-014.8",
        "self_authorization": False,
        "autonomous_authority": False,
    }
    (ops / "RHP-014-7-final-evidence.json").write_text(json.dumps(evidence), encoding="utf-8")
    (tmp_path / "docs" / "context-layer").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "context-layer" / "latest-rhp.json").write_text(
        json.dumps({"latest_operation": "RHP-014.7", "latest_evidence": "docs/context-layer/ops/RHP-014-7-final-evidence.json"}),
        encoding="utf-8",
    )
    bundle = build_bundle(tmp_path)
    assert bundle["operation"] == "RHP-014.7"
    assert bundle["authority"]["ok"] is True
    assert "evidence" in bundle["geometry"]["axes"]
    assert "Operator Dashboard Bundle" in render_markdown(bundle)
