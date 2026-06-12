from rhp.lineage_coherence_auditor import audit_lineage


def test_matching_pointer_and_evidence_is_ok():
    pointer = {
        "latest_operation": "RHP-X",
        "latest_evidence": "docs/x.json",
        "subject_commit": "abc",
        "state": "STATE",
        "observed_ci_status": "unknown",
        "operation_base_commit": "base",
        "current_operation_commit": "repair",
    }
    evidence = {
        "operation": "RHP-X",
        "subject_commit": "abc",
        "state_after_alignment": "STATE",
        "observed_ci_status": "unknown",
        "operation_base_commit": "base",
        "repair_commit": "repair",
    }
    result = audit_lineage(pointer, evidence, head_commit="repair")
    assert result["ok"]
    assert result["error_count"] == 0


def test_base_commit_divergence_is_warning_not_error():
    pointer = {
        "latest_operation": "RHP-X",
        "latest_evidence": "docs/x.json",
        "subject_commit": "abc",
        "state": "STATE",
        "observed_ci_status": "unknown",
        "operation_base_commit": "old-base",
    }
    evidence = {
        "operation": "RHP-X",
        "subject_commit": "abc",
        "state_after_alignment": "STATE",
        "observed_ci_status": "unknown",
        "operation_base_commit": "new-base",
    }
    result = audit_lineage(pointer, evidence)
    assert result["ok"]
    assert result["warning_count"] == 1
    assert result["findings"][0]["code"] == "operation_base_commit_divergence"


def test_operation_mismatch_is_error():
    result = audit_lineage(
        {"latest_operation": "RHP-A", "latest_evidence": "docs/a.json"},
        {"operation": "RHP-B"},
    )
    assert not result["ok"]
    assert result["error_count"] >= 1