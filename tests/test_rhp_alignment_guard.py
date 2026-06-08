from pathlib import Path

from rhp.alignment_guard import validate_alignment


def test_alignment_guard_preflight_accepts_current_repo_shape():
    result = validate_alignment(Path.cwd(), require_latest_passed=False)

    assert result.ok is True
    assert result.mode == "preflight"
    assert result.checks["latest_evidence_exists"] is True
    assert result.checks["root_readme_latest_evidence"] is True
    assert result.checks["rhp_readme_latest_boundary"] is True
    assert result.checks["hrcn_bridge_v03_anchor"] is True
    assert result.checks["rhp_bridge_read_only"] is True
    assert result.checks["authority_false"] is True


def test_alignment_guard_final_requires_green_latest_evidence():
    result = validate_alignment(Path.cwd(), require_latest_passed=True)

    assert result.ok is True
    assert result.mode == "final"
    assert result.checks["latest_rhp006_passed"] is True
