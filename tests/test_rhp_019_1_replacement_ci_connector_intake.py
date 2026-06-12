from rhp.replacement_ci_connector_intake import (
    SUBJECT_COMMIT,
    classify_connector_ci_intake,
    decision_to_dict,
    render_connector_intake_panel,
)


def test_no_connector_surface_is_unknown_not_pass():
    decision = classify_connector_ci_intake(
        subject_commit=SUBJECT_COMMIT,
        combined_status_count=0,
        workflow_run_count=0,
        connector_observed_status="unknown",
    )
    assert not decision.replacement_ci_established
    assert decision.classification == "connector_replacement_ci_evidence_not_established"
    assert decision.next_operation == "operator_rerun_or_ingest_replacement_ci_before_repair"


def test_green_requires_connector_surface():
    decision = classify_connector_ci_intake(
        subject_commit=SUBJECT_COMMIT,
        combined_status_count=0,
        workflow_run_count=0,
        connector_observed_status="green",
    )
    assert not decision.replacement_ci_established


def test_green_with_subject_connector_surface_allows_closure_next_only():
    decision = classify_connector_ci_intake(
        subject_commit=SUBJECT_COMMIT,
        combined_status_count=1,
        workflow_run_count=0,
        connector_observed_status="green",
    )
    assert decision.replacement_ci_established
    assert decision.wound_closure_allowed_next
    assert not decision.repair_allowed_next
    assert decision.next_operation == "close_active_subject_wound_after_subject_scoped_green_ci"


def test_red_with_connector_surface_requires_logs_before_repair():
    decision = classify_connector_ci_intake(
        subject_commit=SUBJECT_COMMIT,
        combined_status_count=0,
        workflow_run_count=1,
        connector_observed_status="red",
    )
    assert decision.replacement_ci_established
    assert decision.failed_log_ingestion_required
    assert not decision.repair_allowed_next
    assert decision.next_operation == "ingest_failed_replacement_ci_logs_before_repair"


def test_wrong_subject_never_establishes():
    decision = classify_connector_ci_intake(
        subject_commit="wrong",
        combined_status_count=1,
        workflow_run_count=1,
        connector_observed_status="green",
    )
    assert not decision.subject_scoped
    assert not decision.replacement_ci_established


def test_panel_and_dict():
    decision = classify_connector_ci_intake(
        subject_commit=SUBJECT_COMMIT,
        combined_status_count=0,
        workflow_run_count=0,
        connector_observed_status="unknown",
    )
    data = decision_to_dict(decision)
    panel = render_connector_intake_panel(decision)
    assert data["classification"] == "connector_replacement_ci_evidence_not_established"
    assert "RHPCI-CONNECTOR [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
