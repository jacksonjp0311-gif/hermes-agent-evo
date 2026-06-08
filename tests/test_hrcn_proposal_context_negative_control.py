import pytest

from agent.agent_init import _maybe_append_hrcn_context


def test_proposal_context_refuses_when_bridge_boundary_raises(monkeypatch):
    import hrcn_runtime_bridge as bridge
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "1")
    def deny(_root):
        raise RuntimeError("negative-control-forged-authority")
    monkeypatch.setattr(bridge, "assert_read_only_boundary", deny)
    assert _maybe_append_hrcn_context("base-proposal") == "base-proposal"


def test_proposal_context_refuses_when_formatter_raises(monkeypatch):
    import hrcn_runtime_bridge as bridge
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "proposal")
    def bad_format(_root):
        raise RuntimeError("negative-control-format-failure")
    monkeypatch.setattr(bridge, "format_context_for_prompt", bad_format)
    assert _maybe_append_hrcn_context("base-proposal") == "base-proposal"


def test_proposal_context_does_not_enable_by_unknown_env_value(monkeypatch):
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "write")
    assert _maybe_append_hrcn_context("base-proposal") == "base-proposal"


def test_proposal_context_contains_non_authority_lock(monkeypatch):
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "1")
    text = _maybe_append_hrcn_context("base-proposal")
    assert "[HRCN READ-ONLY RUNTIME CONTEXT]" in text
    assert "This context is orientation only." in text
    assert "does not authorize tools" in text
    assert "self-authorization" in text


def test_proposal_context_preserves_existing_context_without_duplication(monkeypatch):
    monkeypatch.setenv("HERMES_HRCN_CONTEXT", "1")
    once = _maybe_append_hrcn_context("base-proposal")
    twice = _maybe_append_hrcn_context(once)
    assert twice == once
    assert once.count("[HRCN READ-ONLY RUNTIME CONTEXT]") == 1
