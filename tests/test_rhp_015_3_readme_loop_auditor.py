from rhp.readme_loop_auditor import audit

def test_rhp_015_3_readme_loop_auditor_finds_operator_contract():
    data = audit(".")
    assert data["ok"] is True
    assert data["missing"] == []
