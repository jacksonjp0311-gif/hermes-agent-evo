from rhp.rhpload_doctor import doctor


def test_rhp_015_7_doctor_reports_cockpit_without_mutation():
    data = doctor(".", current_head_ci_status="pending", ci_source="operator-provided", allow_operation_dirty=True)
    assert data["latest_operation"]
    assert data["evidence_api_ok"] is True
    assert data["replay_ok"] is True
    assert data["can_mutate"] is False
    assert "human_all_one_authorization_required_for_mutation" in data["blocked_reasons"]


def test_rhp_015_7_doctor_allows_operation_bootstrap_dirty_mode_without_granting_authority():
    data = doctor(".", current_head_ci_status="pending", ci_source="operator-provided", allow_operation_dirty=True)
    assert data["allow_operation_dirty"] is True
    assert data["can_mutate"] is False
    assert data["authority_required"] == "human_authorized_all_one_script"
