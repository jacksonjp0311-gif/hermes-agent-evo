from rhp.operator_quickstart import OUTPUT_GRAMMAR, READ_ORDER, build_quickstart

def test_rhp_015_3_quickstart_exposes_read_order_and_output_grammar():
    data = build_quickstart(".")
    assert "docs/context-layer/latest-rhp.json" in READ_ORDER
    assert OUTPUT_GRAMMAR["RHPDROP"].startswith("closed compact")
    assert data["authority_ok"] is True
    assert data["run_pattern"][0].startswith("cd")
