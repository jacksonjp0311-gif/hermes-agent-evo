from pathlib import Path
from rhp.alignment_guard import validate_alignment

def test_alignment_guard_preflight_accepts_current_repo_shape():
    result = validate_alignment(Path.cwd(), require_latest_passed=False)
    assert result.ok is True
    assert result.checks["root_readme_latest_evidence"] is True
    assert result.checks["root_readme_no_codex_header"] is True
    assert result.checks["root_readme_rhp010_passed"] is True
    assert result.checks["root_readme_next_rhp011"] is True
    assert result.checks["root_readme_no_mojibake_in_managed_blocks"] is True
    assert result.checks["native_hook_present"] is True
    assert result.checks["startup_packet_exists"] is True
    assert result.checks["authority_false"] is True

def test_alignment_guard_final_requires_green_latest_evidence():
    result = validate_alignment(Path.cwd(), require_latest_passed=True)
    assert result.ok is True
    assert result.checks["latest_rhp010_passed"] is True