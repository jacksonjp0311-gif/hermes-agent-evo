import inspect

from agent import agent_init


def test_init_agent_source_contains_rhp_before_hrcn_startup_order():
    source = inspect.getsource(agent_init.init_agent)
    expected = (
        "agent.ephemeral_system_prompt = _maybe_append_hrcn_context(\n"
        "        _maybe_append_rhp_context(ephemeral_system_prompt)\n"
        "    )"
    )
    assert expected in source


def test_startup_proposal_context_path_preserves_rhp_before_hrcn(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")

    text = agent_init._maybe_append_hrcn_context(
        agent_init._maybe_append_rhp_context("base-startup-proposal")
    )

    assert "[RHP ORIGIN-ALIGNMENT CONTEXT]" in text
    assert "[HRCN READ-ONLY RUNTIME CONTEXT]" in text
    assert text.index("[RHP ORIGIN-ALIGNMENT CONTEXT]") < text.index("[HRCN READ-ONLY RUNTIME CONTEXT]")
    assert "RHP Runtime Bridge: READ ONLY PROPOSAL ORIENTATION" in text
    assert "Compounding Permitted: False" in text
    assert "This context is orientation only." in text
    assert "self-authorization" in text


def test_startup_context_path_is_disabled_by_default(monkeypatch):
    monkeypatch.delenv("HERMES_RHP_CONTEXT", raising=False)
    monkeypatch.delenv("HERMES_HRCN_CONTEXT", raising=False)

    assert agent_init._maybe_append_rhp_context("base") == "base"
    assert agent_init._maybe_append_hrcn_context("base") == "base"


def test_startup_context_path_rejects_unknown_rhp_mode(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "write")
    assert agent_init._maybe_append_rhp_context("base") == "base"
