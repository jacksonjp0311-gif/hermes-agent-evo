from rhp.evidence_api_compatibility_gate import gate


def test_rhp_015_6_evidence_api_gate_current_pointer_is_compatible():
    data = gate(".")
    assert data["ok"] is True
    assert data["missing_pointer_required"] == []
    assert data["missing_evidence_required"] == []
    assert data["authority_not_false"] == []
