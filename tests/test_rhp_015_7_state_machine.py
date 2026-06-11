from rhp.state_machine import derive_state


def test_rhp_015_7_state_machine_pending_after_push():
    data = derive_state(local_validation_ok=True, pushed=True, current_head_ci_status="pending")
    assert data["state"] == "REMOTE_PENDING"
    assert data["mutation_allowed"] is False


def test_rhp_015_7_state_machine_red_requires_wound():
    data = derive_state(local_validation_ok=True, pushed=True, current_head_ci_status="red")
    assert data["state"] == "REMOTE_RED"
    assert data["next_legal_operation"] == "create_ci_wound_packet_before_repair"


def test_rhp_015_7_state_machine_green():
    data = derive_state(local_validation_ok=True, pushed=True, current_head_ci_status="green")
    assert data["state"] == "REMOTE_GREEN"
