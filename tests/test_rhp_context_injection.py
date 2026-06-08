from agent.agent_init import _maybe_append_rhp_context


def test_rhp_context_disabled_by_default(monkeypatch):
    monkeypatch.delenv("HERMES_RHP_CONTEXT", raising=False)
    assert _maybe_append_rhp_context("base-proposal") == "base-proposal"


def test_rhp_context_enabled_by_proposal(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "proposal")
    text = _maybe_append_rhp_context("base-proposal")
    assert "[RHP ORIGIN-ALIGNMENT CONTEXT]" in text
    assert "orientation only" in text
    assert "does not authorize tools" in text


def test_rhp_context_unknown_env_value_does_not_enable(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "write")
    assert _maybe_append_rhp_context("base-proposal") == "base-proposal"


def test_rhp_context_preserves_existing_context_without_duplication(monkeypatch):
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "1")
    once = _maybe_append_rhp_context("base-proposal")
    twice = _maybe_append_rhp_context(once)
    assert twice == once
    assert once.count("[RHP ORIGIN-ALIGNMENT CONTEXT]") == 1


def test_rhp_context_fails_closed_when_bridge_raises(monkeypatch):
    import rhp_runtime_bridge as bridge
    monkeypatch.setenv("HERMES_RHP_CONTEXT", "1")

    def deny(_root):
        raise RuntimeError("negative-control-rhp-boundary")
    monkeypatch.setattr(bridge, "assert_read_only_boundary", deny)

    assert _maybe_append_rhp_context("base-proposal") == "base-proposal"
