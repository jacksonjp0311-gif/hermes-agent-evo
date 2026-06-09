from pathlib import Path

from rhp.startup_context_packet import build_startup_context_packet, packet_json

def test_rhp_010_runtime_native_packet_is_green_and_read_only(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_BOOT_PREFLIGHT", "preflight")
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")
    packet = build_startup_context_packet(Path.cwd())
    data = packet.as_dict()
    assert packet.ok is True
    assert packet.schema == "RHP-STARTUP-CONTEXT-PACKET-v0.2"
    assert packet.installed_launcher_exists is True
    assert packet.native_boot_hook_present is True
    assert packet.boot_preflight_ok is True
    assert packet.startup_context_packet_created is True
    for key in [
        "provider_call_executed",
        "model_call_executed",
        "tool_use_executed",
        "cms_runtime_execution",
        "cms_write",
        "memory_write",
        "memory_promotion",
        "api_write",
        "dependency_mutation_committed",
        "external_ingestion",
        "self_authorization",
        "autonomous_authority",
    ]:
        assert data[key] is False

def test_rhp_010_packet_json_contains_schema(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_BOOT_PREFLIGHT", "preflight")
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")
    text = packet_json(Path.cwd())
    assert "RHP-STARTUP-CONTEXT-PACKET-v0.2" in text
    assert '"ok": true' in text