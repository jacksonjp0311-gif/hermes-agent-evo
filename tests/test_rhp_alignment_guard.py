from pathlib import Path
from rhp.alignment_guard import validate_alignment

def test_alignment_guard_preflight_accepts_current_repo_shape():
    result = validate_alignment(Path.cwd(), require_latest_passed=False)
    assert result.ok is True
    assert result.checks["previous_rhp0121_passed"] is True
    assert result.checks["root_readme_latest_evidence"] is True
    assert result.checks["root_readme_current_status"] is True
    assert result.checks["rhp_readme_rhp0122_present"] is True
    assert result.checks["compact_banner_protocol_env"] is True
    assert result.checks["main_protocol_env_still_present"] is True
    assert result.checks["main_evidence_rhp012_still_present"] is True
    assert result.checks["latest_rhp0122_has_boundary_shape"] is True

def test_alignment_guard_final_requires_green_latest_evidence():
    result = validate_alignment(Path.cwd(), require_latest_passed=True)
    assert result.ok is True
    assert result.checks["latest_rhp0122_passed"] is True
