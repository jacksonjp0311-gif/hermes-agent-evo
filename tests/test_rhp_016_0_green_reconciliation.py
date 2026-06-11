from rhp.green_reconciliation import reconcile


def test_rhp_016_0_green_reconciliation_closes_subject_commit_only():
    data = reconcile(
        subject_commit="abc123",
        remote_ci_status="green",
        source="github-actions-verified",
    )
    assert data["integration_closed"] is True
    assert data["subject_commit"] == "abc123"
    assert data["state"] == "RECONCILED"
    assert data["authority_granted"] is False
    assert data["execution_enabled"] is False


def test_rhp_016_0_green_reconciliation_pending_does_not_close():
    data = reconcile(
        subject_commit="abc123",
        remote_ci_status="pending",
        source="operator-provided",
    )
    assert data["integration_closed"] is False
    assert data["state"] == "REMOTE_PENDING"
