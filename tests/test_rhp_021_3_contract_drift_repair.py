from rhp.rhp_021_3_contract_drift_repair import repaired_wounds

def test_repaired_wounds_declared():
    assert "zero_context_next_operation_contract_drift" in repaired_wounds()
    assert "loop_geometry_legacy_api_drift" in repaired_wounds()
    assert "zero_context_bom_json_loader_drift" in repaired_wounds()
    assert "evidence_api_bom_pointer_loader_drift" in repaired_wounds()