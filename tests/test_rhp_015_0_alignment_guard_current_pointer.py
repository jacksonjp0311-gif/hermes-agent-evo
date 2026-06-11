from pathlib import Path
from rhp.alignment_guard import validate_alignment

def test_rhp_015_0_alignment_guard_preserves_legacy_keys_and_current_pointer():
    preflight = validate_alignment(Path.cwd(), require_latest_passed=False)
    final = validate_alignment(Path.cwd(), require_latest_passed=True)
    assert preflight.ok is True
    assert final.ok is True
    assert preflight.checks["latest_rhp0135_has_boundary_shape"] is True
    assert final.checks["latest_rhp0135_passed"] is True
    assert preflight.checks["current_pointer_exists"] is True
    assert preflight.checks["current_evidence_alignment"] is True
    assert preflight.checks["current_evidence_authority_false"] is True
