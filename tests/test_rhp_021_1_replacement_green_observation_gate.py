from rhp.replacement_green_observation_gate import (
    EXPECTED_SUBJECT_COMMIT,
    make_unresolved_gate_baseline,
    render_replacement_green_gate_panel,
    validate_replacement_green_observation,
)


def observation(status="success", status_context_count=1, workflow_run_count=0, authority=False, subject=EXPECTED_SUBJECT_COMMIT):
    return {
        "subject_commit": subject,
        "source": "github-connector",
        "observed_status": status,
        "status_context_count": status_context_count,
        "workflow_run_count": workflow_run_count,
        "authority_granted": authority,
    }


def test_valid_future_green_observation_is_eligible_but_does_not_close():
    report = validate_replacement_green_observation(observation())
    assert report.ok
    assert report.eligible_for_future_closure is True
    assert report.no_closure_inside_gate_ok is True


def test_success_without_evidence_surface_blocks():
    report = validate_replacement_green_observation(observation(status_context_count=0, workflow_run_count=0))
    assert not report.ok
    assert "no_status_context_or_workflow_run_surface" in report.blocking_reasons
    assert report.eligible_for_future_closure is False


def test_unknown_status_blocks():
    report = validate_replacement_green_observation(observation(status="unknown"))
    assert not report.ok
    assert "observed_status_not_success" in report.blocking_reasons


def test_subject_mismatch_blocks():
    report = validate_replacement_green_observation(observation(subject="wrong"))
    assert not report.ok
    assert "subject_commit_mismatch" in report.blocking_reasons


def test_authority_grant_blocks():
    report = validate_replacement_green_observation(observation(authority=True))
    assert not report.ok
    assert "authority_grant_detected" in report.blocking_reasons


def test_closure_attempt_inside_gate_blocks():
    report = validate_replacement_green_observation(observation(), close_now=True)
    assert not report.ok
    assert "closure_attempted_inside_green_observation_gate" in report.blocking_reasons


def test_baseline_and_panel_render():
    baseline = make_unresolved_gate_baseline()
    report = validate_replacement_green_observation(observation(status="unknown", status_context_count=0))
    panel = render_replacement_green_gate_panel(report)
    assert baseline["close_wound_inside_gate"] is False
    assert baseline["authority_granted"] is False
    assert "RHPGREEN-GATE [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
