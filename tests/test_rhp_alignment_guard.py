from pathlib import Path
from rhp.alignment_guard import validate_alignment

def test_alignment_guard_preflight_accepts_current_repo_shape():
    result = validate_alignment(Path.cwd(), require_latest_passed=False)
    assert result.ok is True
    assert result.checks["latest_evidence_exists"] is True
    assert result.checks["root_readme_latest_evidence"] is True
    assert result.checks["root_readme_rhp009_passed"] is True
    assert result.checks["root_readme_next_rhp010"] is True
    assert result.checks["rhp_readme_boot_preflight"] is True
    assert result.checks["agent_init_boot_preflight_hook"] is True
    assert result.checks["pyproject_rhp_bridge_packaged_or_implicit"] is True
    assert result.checks["authority_false"] is True

def test_alignment_guard_final_requires_green_latest_evidence():
    result = validate_alignment(Path.cwd(), require_latest_passed=True)
    assert result.ok is True
    assert result.checks["latest_rhp009_passed"] is True