from rhp.no_prompt_operator_contract import no_prompt_contract, is_operator_prompt_allowed

def test_no_prompt_contract_blocks_runtime_questions():
    contract = no_prompt_contract()
    assert "after_authorization_no_runtime_questions" in contract["rules"]
    assert contract["allowed_operator_input_after_start"] == []
    assert contract["fallback"] == "seal_unknown_or_pending_as_named_evidence"

def test_only_authorization_prompt_allowed():
    assert is_operator_prompt_allowed("authorization")
    assert not is_operator_prompt_allowed("ci_status")
    assert not is_operator_prompt_allowed("runtime_fact")