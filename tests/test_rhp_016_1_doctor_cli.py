from rhp.doctor_cli import run_cli


def test_rhp_016_1_doctor_cli_wraps_read_only_doctor():
    data = run_cli(".", current_head_ci_status="pending", ci_source="operator-provided", allow_operation_dirty=True)
    assert data["schema"] == "RHP-DOCTOR-CLI-v0.2"
    assert data["doctor"]["can_mutate"] is False
    assert data["human_summary"]["can_mutate"] is False
    assert data["allow_operation_dirty"] is True
    assert "non_claim_lock" in data


def test_rhp_016_1_doctor_cli_bootstrap_dirty_does_not_grant_authority():
    data = run_cli(".", current_head_ci_status="pending", ci_source="operator-provided", allow_operation_dirty=True)
    assert data["doctor"]["can_mutate"] is False
    assert data["doctor"]["authority_required"] == "human_authorized_all_one_script"
