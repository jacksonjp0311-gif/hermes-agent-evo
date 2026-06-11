from rhp.ci_artifact_extractor import RHP_CI_WOUND_PACKET_SCHEMA, classify_ci_text

def test_rhp_014_3_extracts_module_path_bug():
    packet = classify_ci_text("ModuleNotFoundError: No module named 'rhp'")
    data = packet.as_dict()
    assert data["schema"] == RHP_CI_WOUND_PACKET_SCHEMA
    assert data["classification"] == "module_path_execution_bug"
    assert data["suggested_loop"] == "AUTOHEAL-PLAN"

def test_rhp_014_3_extracts_current_script_gate_bug():
    packet = classify_ci_text("actual_script_mismatch evidence_script_mismatch")
    assert packet.classification == "current_script_identity_mismatch"
