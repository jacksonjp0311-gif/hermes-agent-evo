from rhp.repair_ci_reconciliation import reconcile_repair_ci


def test_rhp_016_4_green_repair_ci_reconciliation_closes_wound():
    data = reconcile_repair_ci(
        subject_commit="abc",
        observed_ci_status="green",
        ci_source="github-actions-verified",
        repaired_wound_class="browser_supervisor_websockets_dependency_api_drift",
    )
    assert data["integration_closed"] is True
    assert data["active_wound_class"] == "no_active_wound"
    assert data["state"] == "REPAIR_RECONCILED_GREEN"
    assert data["authority_granted"] is False
    assert data["execution_enabled"] is False


def test_rhp_016_4_red_repair_ci_reconciliation_re_wounds():
    data = reconcile_repair_ci(
        subject_commit="abc",
        observed_ci_status="red",
        ci_source="github-actions-verified",
        repaired_wound_class="browser_supervisor_websockets_dependency_api_drift",
    )
    assert data["integration_closed"] is False
    assert data["active_wound_class"] == "browser_supervisor_websockets_dependency_api_drift"
    assert data["state"] == "REPAIR_STILL_RED"


def test_rhp_016_4_pending_repair_ci_reconciliation_waits():
    data = reconcile_repair_ci(
        subject_commit="abc",
        observed_ci_status="pending",
        ci_source="operator-provided",
        repaired_wound_class="browser_supervisor_websockets_dependency_api_drift",
    )
    assert data["integration_closed"] is False
    assert data["active_wound_class"] == "remote_ci_pending"
    assert data["state"] == "REPAIR_CI_PENDING"
