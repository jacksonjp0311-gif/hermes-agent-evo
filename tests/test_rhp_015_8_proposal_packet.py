from rhp.proposal_packet import build_proposal, validate_proposal


def test_rhp_015_8_proposal_packet_is_non_executing_by_default():
    packet = build_proposal(
        wound_class="remote_ci_pending",
        subject="commit:abc",
        summary="wait for CI",
        allowed_paths=["docs/context-layer/ops/RHP-015-8*"],
        test_commands=["python -m pytest -q"],
    )
    assert packet["execution_enabled"] is False
    assert packet["authority_granted"] is False
    assert validate_proposal(packet)["ok"] is True
