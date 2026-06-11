from rhp.error_box import build, classify_message

def test_error_box_classifies_typo():
    assert classify_message("Path.mkdir() got an unexpected keyword argument 'eyist_ok'") == "python_helper_typo"

def test_error_box_builds_feedback():
    b = build("RHP-014.5-v6", "missing_evidence")
    assert b.failure_class == "current_script_gate_missing_evidence"
