import pytest

from rhp.ci_observation_loop import (
    build_loop_evidence,
    render_hermes_operator_context,
    render_latest_pointer,
    render_operator_dashboard,
    render_zero_context_rebuild_json,
    transition_for_observation,
)


def _packet(status="green"):
    return build_loop_evidence(
        operation="RHP-017.0",
        subject_commit="abc123",
        observed_ci_status=status,
        ci_source="operator-provided",
        prior_operation="RHP-016.4",
        latest_operation="RHP-016.4",
        latest_evidence="docs/context-layer/ops/RHP-016-4-final-evidence.json",
        prior_state="REPAIR_CI_PENDING",
        prior_integration_closed=False,
        prior_active_wound_class="remote_ci_pending",
        repaired_wound_class="browser_supervisor_websockets_dependency_api_drift",
        operation_base_commit="base",
        operator_script_name="RHP_017_0_V3_CI_OBSERVATION_LOOP_KERNEL_SINGLE_ALL_ONE.ps1",
    )


def test_green_closes_named_subject_wound():
    data = transition_for_observation(
        subject_commit="abc123",
        observed_ci_status="green",
        ci_source="operator-provided",
        prior_operation="RHP-016.4",
        repaired_wound_class="browser_supervisor_websockets_dependency_api_drift",
        prior_state="REPAIR_CI_PENDING",
    )
    assert data["to_state"] == "CI_RECONCILED_GREEN"
    assert data["integration_closed"] is True
    assert data["active_wound_class"] == "no_active_wound"
    assert data["wound_queue_action"] == "close_named_subject_wound"
    assert data["authority_granted"] is False
    assert data["execution_enabled"] is False


def test_green_does_not_claim_current_operation_commit():
    packet = _packet("green")
    assert packet["current_operation_commit"] == "unobservable-from-inside-same-commit"
    assert packet["current_operation_remote_ci_status"] == "unknown_until_next_observation"
    assert packet["transition"]["current_operation_commit"] == "unobservable-from-inside-same-commit"


def test_pending_is_named_wait_state_not_failure():
    packet = _packet("pending")
    assert packet["transition"]["to_state"] == "CI_PENDING"
    assert packet["transition"]["terminal"] is False
    assert packet["transition"]["pass"] is False
    assert packet["transition"]["active_wound_class"] == "remote_ci_pending"
    assert packet["transition"]["next_legal_operation"] == "wait_or_ingest_final_ci_status_before_green_claim"


def test_unknown_is_not_pass():
    packet = _packet("unknown")
    assert packet["transition"]["to_state"] == "CI_UNKNOWN"
    assert packet["transition"]["pass"] is False
    assert packet["transition"]["integration_closed"] is False


def test_red_opens_wound_and_routes_to_packet():
    packet = _packet("red")
    assert packet["transition"]["to_state"] == "CI_RED_WOUND_OPEN"
    assert packet["transition"]["integration_closed"] is False
    assert packet["transition"]["active_wound_class"] == "browser_supervisor_websockets_dependency_api_drift"
    assert packet["transition"]["proposal_route"] == "ci_wound_packet_required"
    assert packet["transition"]["next_legal_operation"] == "create_ci_wound_packet_before_repair"


def test_cancelled_is_terminal_non_green_not_pending():
    packet = _packet("cancelled")
    assert packet["transition"]["to_state"] == "CI_CANCELLED_NON_GREEN_TERMINAL"
    assert packet["transition"]["terminal"] is True
    assert packet["transition"]["pass"] is False
    assert packet["transition"]["integration_closed"] is False
    assert packet["transition"]["active_wound_class"] == "remote_ci_red"


def test_skipped_is_terminal_non_green_not_pending():
    packet = _packet("skipped")
    assert packet["transition"]["to_state"] == "CI_SKIPPED_NON_GREEN_TERMINAL"
    assert packet["transition"]["terminal"] is True
    assert packet["transition"]["pass"] is False
    assert packet["transition"]["integration_closed"] is False
    assert packet["transition"]["active_wound_class"] == "remote_ci_red"


def test_authority_locks_remain_false():
    packet = _packet("green")
    assert packet["validation"]["authority_ok"] is True
    assert all(value is False for value in packet["authority_locks"].values())


def test_subject_commit_required():
    with pytest.raises(ValueError):
        transition_for_observation(
            subject_commit="",
            observed_ci_status="green",
            ci_source="operator-provided",
            prior_operation="RHP-016.4",
        )


def test_invalid_status_rejected():
    with pytest.raises(ValueError):
        transition_for_observation(
            subject_commit="abc",
            observed_ci_status="blue",
            ci_source="operator-provided",
            prior_operation="RHP-016.4",
        )


def test_context_renderers_emit_latest_pointer_zero_context_dashboard():
    packet = _packet("green")
    latest = render_latest_pointer(packet)
    zero = render_zero_context_rebuild_json(packet)
    dashboard = render_operator_dashboard(packet)
    operator = render_hermes_operator_context(packet)
    assert latest["latest_operation"] == "RHP-017.0"
    assert latest["state"] == "CI_RECONCILED_GREEN"
    assert latest["integration_closed"] is True
    assert zero["observed_ci_status"] == "green"
    assert "CI_RECONCILED_GREEN" in dashboard
    assert operator["latest_operation"] == "RHP-017.0"
    assert "claim_current_operation_ci_without_observation" in operator["hermes_cannot"]
