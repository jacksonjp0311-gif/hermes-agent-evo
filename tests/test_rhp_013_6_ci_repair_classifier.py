from rhp.ci_repair_classifier import CI_REPAIR_CLASSIFIER_SCHEMA, classify_failure_text

def test_rhp_013_6_classifier_detects_stale_rhp_evidence():
    result = classify_failure_text("AssertionError: expected evidence=RHP-012 but got evidence=RHP-013.5")
    assert result.schema == CI_REPAIR_CLASSIFIER_SCHEMA
    assert result.classification == "stale_test_or_guard_surface"
    assert result.recommended_loop == "CI-REPAIR"

def test_rhp_013_6_classifier_detects_keyerror_stale_guard():
    result = classify_failure_text("KeyError: 'latest_rhp0122_passed'")
    assert result.classification == "stale_test_or_guard_surface"

def test_rhp_013_6_classifier_detects_import_surface():
    result = classify_failure_text("ModuleNotFoundError: No module named rhp.foo")
    assert result.classification == "import_or_packaging_surface"

def test_rhp_013_6_classifier_unknown_assertion_goes_to_diagnosis():
    result = classify_failure_text("AssertionError: assert 1 == 2")
    assert result.classification == "assertion_failure_unknown"
    assert result.recommended_loop == "DIAGNOSIS"
