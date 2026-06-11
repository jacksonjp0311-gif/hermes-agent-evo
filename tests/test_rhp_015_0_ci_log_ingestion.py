from rhp.ci_log_ingestion import classify_log

def test_rhp_015_0_ci_log_ingestion_classifies_boot_alignment_wound():
    result = classify_log("boot_preflight_ok is True root_readme_latest_evidence root_readme_current_status OperatorStartupStatus(ok=False")
    assert "boot_preflight_ok_false" in result["failures"]
    assert "root_readme_latest_evidence" in result["failures"]
    assert "operator_startup_degraded" in result["failures"]
