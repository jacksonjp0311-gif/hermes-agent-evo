from agent.agent_init import _maybe_append_hrcn_context, _maybe_append_rhp_context


def test_rhp_context_appears_before_hrcn_context(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")

    text = _maybe_append_hrcn_context(
        _maybe_append_rhp_context("base-proposal")
    )

    assert "[RHP ORIGIN-ALIGNMENT CONTEXT]" in text
    assert "[HRCN READ-ONLY RUNTIME CONTEXT]" in text
    assert text.index("[RHP ORIGIN-ALIGNMENT CONTEXT]") < text.index("[HRCN READ-ONLY RUNTIME CONTEXT]")
    assert "does not authorize tools" in text
    assert "self-authorization" in text
