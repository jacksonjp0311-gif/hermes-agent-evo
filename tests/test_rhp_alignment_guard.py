from pathlib import Path

from rhp.alignment_guard import validate_alignment


def test_alignment_guard_accepts_current_repo_after_rhp006():
    result = validate_alignment(Path.cwd())

    assert result.ok is True
    assert result.checks["latest_evidence_exists"] is True
    assert result.checks["latest_rhp006_passed"] is True
    assert result.checks["root_readme_latest_evidence"] is True
    assert result.checks["rhp_readme_latest_boundary"] is True
    assert result.checks["hrcn_bridge_v03_anchor"] is True
    assert result.checks["rhp_bridge_read_only"] is True
    assert result.checks["authority_false"] is True
