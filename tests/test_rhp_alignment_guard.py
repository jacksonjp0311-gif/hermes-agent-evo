from pathlib import Path
from rhp.alignment_guard import validate_alignment

def test_alignment_guard_preflight_accepts_current_repo_shape():
    result = validate_alignment(Path.cwd(), require_latest_passed=False)
    assert result.ok is True
    assert result.checks["root_readme_latest_evidence"] is True
    assert result.checks["root_readme_rhp011_passed"] is True
    assert result.checks["root_readme_next_rhp012"] is True
    assert result.checks["operator_status_exists"] is True
    assert result.checks["operator_status_hooked"] is True
    assert result.checks["ascii_safe_hook"] is True
    assert result.checks["authority_false"] is True

def test_alignment_guard_final_requires_green_latest_evidence():
    result = validate_alignment(Path.cwd(), require_latest_passed=True)
    assert result.ok is True
    assert result.checks["latest_rhp011_passed"] is True