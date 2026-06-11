from rhp.wound_queue import build_queue


def test_rhp_015_9_wound_queue_surfaces_pending_ci():
    data = build_queue(current_head="abcdef1234567890", current_head_ci_status="pending", source="operator-provided")
    assert data["has_active_wound"] is True
    assert data["open_count"] == 1
    assert data["items"][0]["wound_class"] == "remote_ci_pending"
    assert data["execution_enabled"] is False


def test_rhp_015_9_wound_queue_green_has_no_open_wound():
    data = build_queue(current_head="abcdef1234567890", current_head_ci_status="green", source="github-actions-verified")
    assert data["open_count"] == 0
    assert data["has_active_wound"] is False
    assert data["items"][0]["wound_class"] == "no_active_wound"
