from pathlib import Path

from rhp.startup_context_packet import (
    RUNTIME_BOOT_STATE_SCHEMA,
    build_runtime_boot_state,
    runtime_boot_state_from_env,
    runtime_boot_state_json,
)

def test_rhp_013_runtime_boot_state_schema_and_boundary(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_BOOT_PREFLIGHT", "preflight")
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")

    state = build_runtime_boot_state(Path.cwd())
    data = state.as_dict()

    assert state.schema == RUNTIME_BOOT_STATE_SCHEMA
    assert state.schema == "RHP-RUNTIME-BOOT-STATE-v0.1"
    assert state.evidence == "RHP-013.4"
    assert state.phase == "pre-interaction"
    assert state.startup_context_packet_schema == "RHP-STARTUP-CONTEXT-PACKET-v0.4"
    assert state.boot_preflight_packet_schema == "RHP-BOOT-PREFLIGHT-PACKET-v0.3"
    assert state.boot_preflight_ok is True
    assert state.startup_packet_ok is True
    assert state.locks["authority_false"] is True
    assert state.authority["provider_call_executed"] is False
    assert state.authority["model_call_executed"] is False
    assert state.authority["tool_use_executed"] is False
    assert state.authority["cms_write"] is False
    assert state.authority["memory_write"] is False
    assert state.authority["api_write"] is False
    assert state.authority["external_ingestion"] is False
    assert state.authority["autonomous_authority"] is False
    assert state.authority["self_authorization"] is False
    assert "authority=false" in state.protocol_strip
    assert "RHP-013.4" in state.protocol_strip
    assert "RHP-RUNTIME-BOOT-STATE-v0.1" in state.prompt_context_json
    assert "locks" in data

def test_rhp_013_runtime_boot_state_json_contains_schema(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_BOOT_PREFLIGHT", "preflight")
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")

    text = runtime_boot_state_json(Path.cwd())
    assert "RHP-RUNTIME-BOOT-STATE-v0.1" in text
    assert '"provider_call_executed": false' in text
    assert '"self_authorization": false' in text

def test_rhp_013_runtime_boot_state_from_env(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_BOOT_PREFLIGHT", "preflight")
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")

    state = runtime_boot_state_from_env(Path.cwd())
    assert state.schema == RUNTIME_BOOT_STATE_SCHEMA
    assert state.env["HERMES_RHP_CONTEXT"] == "proposal"
    assert state.env["HERMES_HRCN_CONTEXT"] == "proposal"
