from pathlib import Path

from rhp.operator_startup_status import build_operator_startup_status, render_operator_startup_status
from rhp.startup_context_packet import build_startup_context_packet

def test_rhp_011_operator_visible_status_lists_all_locks(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_BOOT_PREFLIGHT", "preflight")
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")
    packet = build_startup_context_packet(Path.cwd())
    status = build_operator_startup_status(packet)
    text = "\n".join(status.lines)
    assert status.ok is True
    assert "[OK] repo root found" in text
    assert "[OK] RHP-010 evidence green" in text
    assert "[OK] HRCN boundary green" in text
    assert "[OK] alignment guard green" in text
    assert "[OK] startup packet created" in text
    assert "[OK] authority=false" in text
    assert "[OK] external_ingestion=false" in text
    assert "[OK] provider/model/tool execution=false" in text
    assert "[OK] CMS/memory/API write=false" in text
    assert "RHP rehydration complete: ok | phase=pre-interaction | evidence=RHP-010" in text
    assert text.isascii()

def test_rhp_011_render_is_ascii_safe(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_BOOT_PREFLIGHT", "preflight")
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")
    packet = build_startup_context_packet(Path.cwd())
    text = render_operator_startup_status(packet)
    assert text.isascii()
    assert "authority=false" in text