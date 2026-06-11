from rhp.wound_taxonomy import WOUND_CLASSES, classify_text, registry


def test_rhp_015_8_wound_taxonomy_has_stable_classes():
    data = registry()
    assert data["schema"] == "RHP-WOUND-TAXONOMY-v0.1"
    assert "evidence_api_break" in WOUND_CLASSES
    assert "remote_ci_red" in WOUND_CLASSES
    assert "doctor_bootstrap_dirty_self_observation" in WOUND_CLASSES


def test_rhp_015_8_wound_taxonomy_classifies_doctor_bootstrap_dirty():
    data = classify_text("doctor failed on dirty bootstrap during authorized construction")
    assert data["class"] == "doctor_bootstrap_dirty_self_observation"
