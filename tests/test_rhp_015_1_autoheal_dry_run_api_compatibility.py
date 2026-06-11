from pathlib import Path

from rhp.autoheal_executor_dry_run import (
    RHP_AUTOHEAL_DRY_RUN_SCHEMA,
    dry_run_for_packet,
)
from rhp.ci_pipeline_bridge import run_bridge


def test_rhp_015_1_autoheal_dry_run_legacy_api_compatibility():
    dry = dry_run_for_packet({"classification": "stream_output_leak_or_crlf_noise"})
    data = dry.as_dict()
    assert data["schema"] == RHP_AUTOHEAL_DRY_RUN_SCHEMA
    assert data["ok"] is True
    assert data["would_mutate"] is False
    assert data["would_commit"] is False
    assert data["allowed_paths"]


def test_rhp_015_1_bridge_still_consumes_dry_run_for_packet(tmp_path: Path):
    text = tmp_path / "ci.txt"
    text.write_text("ModuleNotFoundError: No module named 'rhp'", encoding="utf-8")
    evidence = tmp_path / "evidence.json"
    evidence.write_text(
        '{"operation":"RHP-015.1","next_recommended_operation":"next","schema":"evidence","self_authorization":false,"autonomous_authority":false}',
        encoding="utf-8",
    )
    out = tmp_path / "out"
    result = run_bridge(text, evidence, out)
    assert result["ok"] is True
    assert result["classification"] == "module_path_execution_bug"
    assert Path(result["autoheal_dry_run"]).exists()


def test_rhp_015_1_unknown_classification_fails_closed():
    dry = dry_run_for_packet({"classification": "unknown"})
    assert dry.ok is False
    assert dry.stop_reason
    assert dry.as_dict()["would_mutate"] is False
