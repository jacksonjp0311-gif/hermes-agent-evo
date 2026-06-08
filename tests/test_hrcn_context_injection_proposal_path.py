from agent.agent_init import _maybe_append_hrcn_context


def test_hrcn_context_injection_disabled_by_default(monkeypatch):
    monkeypatch.delenv("HERMES_HRCN_CONTEXT", raising=False)
    assert _maybe_append_hrcn_context("base") == "base"


def test_hrcn_context_injection_appends_read_only_context(monkeypatch):
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "1")
    text = _maybe_append_hrcn_context("base")

    assert text is not None
    assert text.startswith("base")
    assert "[HRCN READ-ONLY RUNTIME CONTEXT]" in text
    assert "HRCN Runtime Bridge: READ ONLY" in text
    assert "hrcn-ops-v0.3.0" in text
    assert "OPS-027-final-evidence.json" in text
    assert "does not authorize tools" in text


def test_hrcn_context_injection_does_not_duplicate(monkeypatch):
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "1")
    once = _maybe_append_hrcn_context("base")
    twice = _maybe_append_hrcn_context(once)

    assert twice == once
    assert once.count("[HRCN READ-ONLY RUNTIME CONTEXT]") == 1


def test_hrcn_context_injection_can_create_prompt_from_none(monkeypatch):
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")
    text = _maybe_append_hrcn_context(None)

    assert text is not None
    assert text.startswith("[HRCN READ-ONLY RUNTIME CONTEXT]")
    assert "HRCN Runtime Bridge: READ ONLY" in text
    assert "read-only" in text.lower()
