
from rhp.autoheal_preflight import RHP_AUTOHEAL_PREFLIGHT_SCHEMA, classify_dirty, render_preflight_box

def test_rhp_013_9_preflight_clean_state_verified():
    result = classify_dirty([], "RHP-013.9")
    assert result.schema == RHP_AUTOHEAL_PREFLIGHT_SCHEMA
    assert result.ok is True
    assert result.status == "clean"
    assert result.verified is True
    assert result.glyph == "[OK]"

def test_rhp_013_9_preflight_bounded_residue_warns_and_allows():
    result = classify_dirty(["README.md", "docs/context-layer/ops/RHP-013-9-x/file.txt"], "RHP-013.9")
    text = render_preflight_box(result)
    assert result.ok is True
    assert result.status == "bounded_residue_detected"
    assert result.action == "clean_bounded_residue_then_continue"
    assert "autoheal preflight box" in text

def test_rhp_013_9_preflight_blocks_unknown_work():
    result = classify_dirty(["src/user_work.py"], "RHP-013.9")
    assert result.ok is False
    assert result.status == "blocked_dirty_worktree"
    assert result.blocked_paths == ["src/user_work.py"]
