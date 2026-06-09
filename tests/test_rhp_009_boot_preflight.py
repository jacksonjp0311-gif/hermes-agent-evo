from pathlib import Path

from rhp.boot_preflight import format_boot_context_for_prompt, run_boot_preflight

def test_rhp_009_boot_preflight_packet_is_green_and_read_only(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")

    packet = run_boot_preflight(Path.cwd())
    data = packet.as_dict()

    assert packet.ok is True
    assert packet.boot_phase == "pre_interaction"
    assert packet.rhp_evidence_green is True
    assert packet.hrcn_boundary_green is True
    assert packet.alignment_guard_green is True
    assert packet.rhp_context_requested is True
    assert packet.hrcn_context_requested is True
    assert packet.startup_context_packet_created is True

    for key in [
        "provider_call_executed", "model_call_executed", "tool_use_executed",
        "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
        "api_write", "dependency_mutation_committed", "external_ingestion",
        "self_authorization", "autonomous_authority",
    ]:
        assert data[key] is False

def test_rhp_009_boot_context_format_contains_compact_packet(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")
    text = format_boot_context_for_prompt(Path.cwd())
    assert "RHP-BOOT-PREFLIGHT-PACKET-v0.3" in text
    assert '"ok": true' in text
    assert "external_ingestion" in text