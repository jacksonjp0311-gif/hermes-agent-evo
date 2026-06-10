from rhp.ci_watch import CI_WATCH_SCHEMA, classify_runs, watch_commit

def test_rhp_013_5_classify_green_run():
    runs = [{"status": "completed", "conclusion": "success", "name": "Tests"}]
    jobs = [{"name": "test (1)", "status": "completed", "conclusion": "success"}]
    classification, ok, degraded, reason, failures = classify_runs(runs, jobs)
    assert classification == "green"
    assert ok is True
    assert degraded is False
    assert reason == ""
    assert failures == []

def test_rhp_013_5_classify_failed_job_actionable():
    runs = [{"status": "completed", "conclusion": "failure", "name": "Tests"}]
    jobs = [{"name": "test (3)", "status": "completed", "conclusion": "failure"}]
    classification, ok, degraded, reason, failures = classify_runs(runs, jobs)
    assert classification == "red-actionable"
    assert ok is False
    assert degraded is True
    assert "failed" in reason
    assert failures and "test (3)" in failures[0]

def test_rhp_013_5_classify_no_runs_unknown():
    classification, ok, degraded, reason, failures = classify_runs([], [])
    assert classification == "unknown"
    assert ok is False
    assert degraded is True
    assert "no workflow runs" in reason
    assert failures == []

def test_rhp_013_5_watch_commit_error_degrades(monkeypatch):
    import rhp.ci_watch as ci_watch
    def boom(*args, **kwargs):
        raise ValueError("synthetic")
    monkeypatch.setattr(ci_watch, "_get_json", boom)
    packet = watch_commit("owner", "repo", "abc123")
    assert packet.schema == CI_WATCH_SCHEMA
    assert packet.classification == "unknown"
    assert packet.degraded is True
    assert "github_api_error" in packet.degraded_reason
