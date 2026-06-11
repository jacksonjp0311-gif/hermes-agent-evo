from rhp.report_junit import build_junit

def test_junit_report_has_testsuite_and_zero_failures():
    xml = build_junit({"operation": "RHP-014.6", "focused_tests_passed": True, "validation_passed": True, "self_authorization": False, "autonomous_authority": False, "operator_script_name": "x.ps1", "post_seal_residue_observer_added": True, "machine_reports_are_evidence_only": True, "generated_source_escape_repair": True})
    assert "<testsuite" in xml
    assert "authority_locks_false" in xml
    assert 'failures="0"' in xml
