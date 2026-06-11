from rhp.browser_supervisor_websockets_proposal import build_browser_supervisor_websockets_proposal

def test_rhp_016_2_browser_supervisor_websockets_proposal_is_bounded():
    packet = build_browser_supervisor_websockets_proposal(subject_commit="abc", run_url="https://example.invalid/run")
    assert packet["wound_class"] == "browser_supervisor_websockets_dependency_api_drift"
    assert packet["execution_enabled"] is False
    assert packet["authority_granted"] is False
    assert "tools/browser_supervisor.py" in packet["allowed_paths"]
    assert any("test_browser_supervisor.py" in cmd for cmd in packet["test_commands"])
