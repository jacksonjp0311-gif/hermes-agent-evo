from rhp.wait_state_packet import build_packet


def test_rhp_015_5_wait_state_pending_not_green():
    data = build_packet(operation="RHP-X", observed_commit="abc", remote_ci_status="pending", next_operation="next")
    assert data["wait_state"] is True
    assert data["green_seal_ready"] is False
    assert data["wound_packet_required"] is False


def test_rhp_015_5_wait_state_red_requires_wound_packet():
    data = build_packet(operation="RHP-X", observed_commit="abc", remote_ci_status="red", next_operation="next")
    assert data["wait_state"] is False
    assert data["wound_packet_required"] is True
