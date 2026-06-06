from pathlib import Path

import hrcn_runtime_bridge as bridge


def test_hrcn_bridge_boundary_is_read_only():
    assert bridge.assert_read_only_boundary(Path.cwd()) is True


def test_hrcn_bridge_status_exposes_v02_anchor():
    status = bridge.get_bridge_status(Path.cwd())
    assert status.enabled is True
    assert status.mode == "read_only"
    assert status.sealed_anchor_tag == "hrcn-ops-v0.2.0"
    assert status.authority["runtime_source_mutation"] is False
    assert status.authority["cms_write"] is False
    assert status.authority["memory_write"] is False
    assert status.authority["api_write"] is False
    assert status.authority["autonomous_authority"] is False
    assert status.authority["self_authorization"] is False


def test_hrcn_context_packet_is_interface_safe():
    packet = bridge.make_gui_context_packet(Path.cwd())
    assert packet["packet_schema"] == "HRCN-GUI-RUNTIME-CONTEXT-PACKET-v0.1"
    assert "mutate runtime source" in packet["forbidden_runtime_use"]
    assert "write memory" in packet["forbidden_runtime_use"]
    assert "display HRCN status" in packet["allowed_runtime_use"]


def test_hrcn_prompt_context_contains_lock():
    text = bridge.format_context_for_prompt(Path.cwd())
    assert "HRCN Runtime Bridge: READ ONLY" in text
    assert "hrcn-ops-v0.2.0" in text
    assert "does not authorize tools" in text
