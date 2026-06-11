from rhp.report_github_summary import render_summary

def test_github_summary_contains_operation_and_next():
    text = render_summary({"operation": "RHP-014.6", "schema": "x", "focused_tests_passed": True, "validation_passed": True, "post_seal_residue_observer_added": True, "machine_reports_are_evidence_only": True, "self_authorization": False, "autonomous_authority": False, "next_recommended_operation": "RHP-014.7"})
    assert "RHPLOAD GitHub Job Summary" in text
    assert "RHP-014.6" in text
    assert "RHP-014.7" in text
