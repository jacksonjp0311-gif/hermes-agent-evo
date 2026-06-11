import json

from rhp.evidence_api_compatibility_gate import AUTHORITY_FIELDS, gate


def test_rhp_017_1_gate_accepts_nested_authority_locks_alias(tmp_path):
    root = tmp_path
    ctx = root / "docs" / "context-layer"
    ops = ctx / "ops"
    ops.mkdir(parents=True)
    pointer = {
        "schema": "RHP-LATEST-POINTER-v2.1",
        "latest_operation": "RHP-017.0",
        "latest_evidence": "docs/context-layer/ops/final.json",
        "next_operation": "continue_bounded_evolution_after_named_subject_green",
        "authority_ok": True,
    }
    evidence = {
        "schema": "RHP-CI-OBSERVATION-LOOP-EVIDENCE-v0.1",
        "operation": "RHP-017.0",
        "operator_script_name": "RHP_017_0_V3_CI_OBSERVATION_LOOP_KERNEL_SINGLE_ALL_ONE.ps1",
        "validation_passed": True,
        "focused_tests_passed": True,
        "non_claim_lock": "Nested authority lock fixture grants no authority.",
        "authority_locks": {field: False for field in AUTHORITY_FIELDS},
    }
    (ctx / "latest-rhp.json").write_text(json.dumps(pointer), encoding="utf-8")
    (ops / "final.json").write_text(json.dumps(evidence), encoding="utf-8")

    data = gate(root)
    assert data["ok"] is True
    assert data["missing_authority_fields"] == []
    assert data["authority_not_false"] == []
    assert data["authority_source"] == "nested_authority_locks"
    assert data["classification"]["alias"]["authority_locks"] == AUTHORITY_FIELDS


def test_rhp_017_1_gate_still_accepts_top_level_authority_fields(tmp_path):
    root = tmp_path
    ctx = root / "docs" / "context-layer"
    ops = ctx / "ops"
    ops.mkdir(parents=True)
    pointer = {
        "schema": "RHP-LATEST-POINTER-v2.1",
        "latest_operation": "RHP-legacy",
        "latest_evidence": "docs/context-layer/ops/final.json",
        "next_operation": "continue",
        "authority_ok": True,
    }
    evidence = {
        "schema": "RHP-LEGACY-EVIDENCE",
        "operation": "RHP-legacy",
        "operator_script_name": "legacy.ps1",
        "validation_passed": True,
        "focused_tests_passed": True,
        "non_claim_lock": "Top-level authority fixture grants no authority.",
        **{field: False for field in AUTHORITY_FIELDS},
    }
    (ctx / "latest-rhp.json").write_text(json.dumps(pointer), encoding="utf-8")
    (ops / "final.json").write_text(json.dumps(evidence), encoding="utf-8")

    data = gate(root)
    assert data["ok"] is True
    assert data["missing_authority_fields"] == []
    assert data["authority_not_false"] == []
    assert data["authority_source"] == "top_level_fields"
