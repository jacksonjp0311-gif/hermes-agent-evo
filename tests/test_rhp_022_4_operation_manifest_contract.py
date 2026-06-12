from rhp.operation_manifest_contract import (
    make_manifest,
    required_forbidden_actions,
    required_manifest_fields,
    validate_manifest,
)


def _valid_manifest():
    return make_manifest(
        operation="RHP-X",
        lane="canonization",
        ci_state="unknown",
        story="Install a safe canonization layer while preserving unresolved CI.",
        declared_files=["rhp/example.py"],
        allowed_mutations=["add canonization helper"],
        forbidden_actions=list(required_forbidden_actions()),
        evidence_outputs=["docs/context-layer/ops/RHP-X-final-evidence.json"],
        validation_commands=["python -m pytest tests/test_example.py"],
        non_claim_locks=["does not claim green"],
    )


def test_required_manifest_fields_are_explicit():
    assert "story" in required_manifest_fields()
    assert "declared_files" in required_manifest_fields()
    assert "non_claim_locks" in required_manifest_fields()


def test_valid_manifest_passes_lane_gate():
    result = validate_manifest(_valid_manifest())
    assert result.ok
    assert result.lane_gate_allowed
    assert result.reason == "manifest_valid"


def test_missing_story_fails():
    manifest = _valid_manifest()
    manifest["story"] = ""
    result = validate_manifest(manifest)
    assert not result.ok
    assert result.reason == "story_required"


def test_missing_forbidden_action_fails():
    manifest = _valid_manifest()
    manifest["forbidden_actions"] = ["claim_green"]
    result = validate_manifest(manifest)
    assert not result.ok
    assert result.reason == "missing_required_forbidden_actions"
    assert "close_wound" in result.missing_forbidden_actions


def test_release_lane_under_unknown_ci_fails_lane_gate():
    manifest = _valid_manifest()
    manifest["lane"] = "release"
    result = validate_manifest(manifest)
    assert not result.ok
    assert result.reason == "lane_gate_rejected_manifest"