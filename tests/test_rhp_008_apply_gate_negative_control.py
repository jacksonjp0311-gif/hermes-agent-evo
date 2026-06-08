from pathlib import Path

from rhp.apply_gate_negative_control import (
    ATTEMPTED_ESCALATIONS,
    refuse_attempt,
    run_apply_gate_negative_control,
)

def test_rhp_008_apply_gate_negative_control_refuses_all_escalations():
    proof = run_apply_gate_negative_control(Path.cwd())
    data = proof.as_dict()

    assert proof.ok is True
    assert proof.proposal_loop_ok is True
    assert proof.human_apply_gate_present is False
    assert proof.attempted_escalations_count == len(ATTEMPTED_ESCALATIONS)
    assert proof.refused_escalations_count == len(ATTEMPTED_ESCALATIONS)
    assert proof.all_escalations_refused is True

    for key in [
        "provider_call_executed",
        "model_call_executed",
        "tool_use_executed",
        "cms_runtime_execution",
        "cms_write",
        "memory_write",
        "memory_promotion",
        "api_write",
        "dependency_mutation_committed",
        "codex_ingestion",
        "self_authorization",
        "autonomous_authority",
    ]:
        assert data[key] is False

def test_rhp_008_refusal_does_not_become_apply_even_if_gate_boolean_is_true():
    refusal = refuse_attempt("tool_use", human_apply_gate_present=True)
    assert refusal.allowed is False
    assert refusal.authority_value is False
    assert "negative-control proof" in refusal.reason