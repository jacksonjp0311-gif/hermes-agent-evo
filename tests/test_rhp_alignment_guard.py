from pathlib import Path
from rhp.alignment_guard import validate_alignment

def test_alignment_guard_preflight_accepts_current_repo_shape():
    result = validate_alignment(Path.cwd(), require_latest_passed=False)
    assert result.ok is True
    assert result.checks["previous_rhp0133_passed"] is True
    assert result.checks["root_readme_latest_evidence"] is True
    assert result.checks["root_readme_current_status"] is True
    assert result.checks["rhp_readme_rhp0134_present"] is True
    assert result.checks["runtimebootstate_schema_present"] is True
    assert result.checks["runtimebootstate_evidence_0134"] is True
    assert result.checks["boot_preflight_latest_evidence_present"] is True
    assert result.checks["operator_status_evidence_0134"] is True
    assert result.checks["cli_uses_runtime_boot_state"] is True
    assert result.checks["banner_evidence_0134"] is True
    assert result.checks["latest_rhp0134_has_boundary_shape"] is True

def test_alignment_guard_final_requires_green_latest_evidence():
    result = validate_alignment(Path.cwd(), require_latest_passed=True)
    assert result.ok is True
    assert result.checks["latest_rhp0134_passed"] is True
