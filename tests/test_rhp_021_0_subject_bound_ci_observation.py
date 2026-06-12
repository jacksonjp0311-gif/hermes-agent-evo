from rhp.subject_bound_ci_observation import (
    EXPECTED_SUBJECT_COMMIT,
    classify_subject_bound_ci_observation,
    make_subject_bound_ci_observation_evidence,
    render_subject_bound_ci_ingest_panel,
    validate_subject_bound_ci_ingest,
)


def obs(status="unknown", subject=EXPECTED_SUBJECT_COMMIT, authority=False):
    return {
        "schema": "RHP-CONNECTOR-OBSERVATION-ADAPTER-CONTRACT-v0.1",
        "subject_commit": subject,
        "source": "github-connector",
        "observed_status": status,
        "observed_at_utc": "2026-06-12T00:00:00+00:00",
        "observer": "RHP-021.0",
        "raw_reference": "github-connector-status-and-workflow-run-lookup",
        "interpretation": "No pass/fail claim. Observation unresolved.",
        "authority_granted": authority,
    }


def test_unknown_with_no_runs_is_unresolved_unknown():
    result = classify_subject_bound_ci_observation(
        connector_observation=obs("unknown"),
        status_context_count=0,
        workflow_run_count=0,
    )
    assert result == "unresolved_unknown"


def test_success_requires_evidence_surface():
    result = classify_subject_bound_ci_observation(
        connector_observation=obs("success"),
        status_context_count=0,
        workflow_run_count=0,
    )
    assert result == "unresolved_unknown"

    result = classify_subject_bound_ci_observation(
        connector_observation=obs("success"),
        status_context_count=1,
        workflow_run_count=0,
    )
    assert result == "resolved_green"


def test_subject_mismatch_blocks():
    report = validate_subject_bound_ci_ingest(
        connector_observation=obs(subject="wrong"),
        status_context_count=0,
        workflow_run_count=0,
    )
    assert not report.ok
    assert "subject_commit_mismatch" in report.blocking_reasons


def test_connector_authority_grant_blocks():
    report = validate_subject_bound_ci_ingest(
        connector_observation=obs(authority=True),
        status_context_count=0,
        workflow_run_count=0,
    )
    assert not report.ok
    assert "connector_authority_grant_detected" in report.blocking_reasons


def test_wound_closure_request_blocks():
    report = validate_subject_bound_ci_ingest(
        connector_observation=obs(),
        status_context_count=0,
        workflow_run_count=0,
        requested_wound_closure=True,
    )
    assert not report.ok
    assert "wound_closure_requested_during_observation_ingest" in report.blocking_reasons


def test_evidence_and_panel_render():
    report = validate_subject_bound_ci_ingest(
        connector_observation=obs(),
        status_context_count=0,
        workflow_run_count=0,
    )
    evidence = make_subject_bound_ci_observation_evidence(
        connector_observation=obs(),
        status_context_count=0,
        workflow_run_count=0,
        report=report,
    )
    panel = render_subject_bound_ci_ingest_panel(report)
    assert report.ok
    assert evidence["result_state"] == "unresolved_unknown"
    assert evidence["can_close_wound"] is False
    assert "RHPCI-INGEST [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
