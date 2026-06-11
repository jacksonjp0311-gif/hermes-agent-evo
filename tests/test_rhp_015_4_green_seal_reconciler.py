
from rhp.green_seal_reconciler import reconcile

def test_rhp_015_4_green_seal_unknown_not_closed():
    data = reconcile(local_validation_ok=True, ci_status="unknown", previous_sealed_commit="prev", operation_base_commit="base")
    assert data["integration_closed"] is False
    assert "wait for CI" in data["next_action"]

def test_rhp_015_4_green_seal_green_closed_when_local_ok():
    data = reconcile(local_validation_ok=True, ci_status="green", previous_sealed_commit="prev", operation_base_commit="base")
    assert data["integration_closed"] is True
