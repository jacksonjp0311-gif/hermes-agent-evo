from rhp.ci_observation import observe


def test_rhp_016_1_ci_observation_green_scopes_subject_commit():
    data = observe(subject_commit="abc", ci_status="green", source="github-actions-verified", prior_operation="RHP-016.0")
    assert data["subject_commit"] == "abc"
    assert data["integration_closed"] is True
    assert data["state"] == "RECONCILED"
    assert data["authority_granted"] is False
    assert data["execution_enabled"] is False


def test_rhp_016_1_ci_observation_pending_does_not_close():
    data = observe(subject_commit="abc", ci_status="pending", source="operator-provided")
    assert data["integration_closed"] is False
    assert data["state"] == "REMOTE_PENDING"
