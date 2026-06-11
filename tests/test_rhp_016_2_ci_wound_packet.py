from rhp.ci_wound_packet import build_packet, validate_packet

def test_rhp_016_2_ci_wound_packet_is_non_executing():
    packet = build_packet(
        wound_class="browser_supervisor_websockets_dependency_api_drift",
        subject_commit="abc",
        workflow="Tests",
        run_url="https://example.invalid/run",
        failed_test_file="tests/tools/test_browser_supervisor.py",
        repro_command="python -m pytest tests/tools/test_browser_supervisor.py",
        source="github-actions-verified",
        root_cause="websockets dependency API drift",
    )
    assert packet["ci_status"] == "red"
    assert packet["integration_closed"] is False
    assert packet["authority_granted"] is False
    assert packet["execution_enabled"] is False
    assert validate_packet(packet)["ok"] is True
