from pathlib import Path

from rhp.operator_startup_status import build_operator_startup_status, render_operator_startup_status
from rhp.startup_context_packet import build_runtime_boot_state

def test_rhp_013_4_operator_status_accepts_runtime_boot_state(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_BOOT_PREFLIGHT", "preflight")
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")

    state = build_runtime_boot_state(Path.cwd())
    status = build_operator_startup_status(state, evidence="RHP-013.5")

    assert status.evidence == "RHP-013.5"
    assert status.locks["authority_false"] is True
    assert status.locks["provider_model_tool_false"] is True
    assert status.locks["cms_memory_api_false"] is True
    assert status.locks["external_ingestion_false"] is True

def test_rhp_013_4_render_operator_status_mentions_runtime_evidence(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_BOOT_PREFLIGHT", "preflight")
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")

    state = build_runtime_boot_state(Path.cwd())
    text = render_operator_startup_status(state, evidence="RHP-013.5")
    assert "RHP rehydration complete:" in text
    assert "evidence=RHP-013.5" in text
    assert "provider/model/tool=false" in text
