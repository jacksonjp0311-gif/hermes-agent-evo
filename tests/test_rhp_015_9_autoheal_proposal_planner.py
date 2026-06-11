from rhp.autoheal_proposal_planner import plan, select_wound_for_ci


def test_rhp_015_9_selects_pending_wound_from_pending_ci():
    assert select_wound_for_ci("pending") == "remote_ci_pending"


def test_rhp_015_9_planner_proposal_is_non_executing():
    data = plan(
        wound_class="remote_ci_pending",
        subject="commit:abc",
        current_head_ci_status="pending",
        source="operator-provided",
    )
    assert data["execution_enabled"] is False
    assert data["authority_granted"] is False
    assert data["proposal"]["execution_enabled"] is False
    assert data["proposal"]["authority_granted"] is False
    assert data["proposal_validation"]["ok"] is True
