from rhp.ci_green_reconciler import reconcile

def test_rhp_015_3_ci_green_reconciler_does_not_claim_unknown_ci_green():
    data = reconcile(".", "unknown")
    assert data["local_validation_ok"] is True
    assert data["integration_closed"] is False
    assert "verify remote CI" in data["next_action"]

def test_rhp_015_3_ci_green_reconciler_green_closes_only_when_local_ok():
    data = reconcile(".", "green")
    assert data["local_validation_ok"] is True
    assert data["integration_closed"] is True
