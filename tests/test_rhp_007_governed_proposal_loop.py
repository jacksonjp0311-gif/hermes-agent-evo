from pathlib import Path
from rhp.proposal_loop_proof import run_governed_proposal_loop_proof

def test_rhp_007_governed_proposal_loop_proof():
    proof = run_governed_proposal_loop_proof(Path.cwd())
    data = proof.as_dict()
    assert proof.ok is True
    assert proof.rhp_packet_schema == "RHP-HERMES-RUNTIME-CONTEXT-PACKET-v0.1"
    assert proof.hrcn_packet_schema == "HRCN-GUI-RUNTIME-CONTEXT-PACKET-v0.3"
    assert proof.proposal_context_contains_rhp is True
    assert proof.proposal_context_contains_hrcn is True
    assert proof.rhp_before_hrcn is True
    assert proof.forbidden_authority_all_false is True
    for key in [
        "provider_call_executed", "model_call_executed", "tool_use_executed",
        "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
        "api_write", "dependency_mutation_committed", "codex_ingestion",
        "self_authorization", "autonomous_authority",
    ]:
        assert data[key] is False