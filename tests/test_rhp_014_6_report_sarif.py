from rhp.report_sarif import build_sarif

def test_sarif_report_shape():
    data = build_sarif({"operation": "RHP-014.6", "validation_passed": True, "self_authorization": False, "autonomous_authority": False, "operator_script_name": "x.ps1"})
    assert data["version"] == "2.1.0"
    assert data["runs"][0]["tool"]["driver"]["name"] == "RHPLOAD Machine Report"
    assert data["runs"][0]["results"] == []
