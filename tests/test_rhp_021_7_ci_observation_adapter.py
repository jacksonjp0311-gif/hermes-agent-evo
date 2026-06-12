from rhp.ci_observation_adapter import classify_workflow_runs, classify_status_contexts, merge_observations


def test_workflow_runs_empty_is_unknown():
    obs = classify_workflow_runs("abc", [])
    assert obs.observed_status == "unknown"
    assert not obs.green_eligible
    assert not obs.authority_granted


def test_workflow_runs_success_with_surface_is_green_eligible():
    obs = classify_workflow_runs("abc", [{"status": "completed", "conclusion": "success"}])
    assert obs.observed_status == "success"
    assert obs.workflow_run_count == 1
    assert obs.green_eligible


def test_workflow_runs_failure_precedes_pending_and_success():
    obs = classify_workflow_runs(
        "abc",
        [
            {"status": "completed", "conclusion": "success"},
            {"status": "completed", "conclusion": "failure"},
        ],
    )
    assert obs.observed_status == "failure"
    assert not obs.green_eligible


def test_status_context_classification():
    assert classify_status_contexts("abc", []).observed_status == "unknown"
    assert classify_status_contexts("abc", [{"state": "pending"}]).observed_status == "pending"
    assert classify_status_contexts("abc", [{"state": "success"}]).observed_status == "success"
    assert classify_status_contexts("abc", [{"state": "error"}]).observed_status == "failure"


def test_merge_observations_failure_dominates():
    a = classify_workflow_runs("abc", [{"status": "completed", "conclusion": "success"}])
    b = classify_status_contexts("abc", [{"state": "failure"}])
    merged = merge_observations(a, b)
    assert merged.observed_status == "failure"
    assert merged.workflow_run_count == 1
    assert merged.status_context_count == 1
    assert not merged.green_eligible