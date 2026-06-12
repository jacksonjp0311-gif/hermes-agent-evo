from rhp.rhp_021_2_post_seal_residue import classify_residue, parse_git_status_lines


def test_parse_git_status_lines_extracts_paths():
    paths = parse_git_status_lines([" M README.md", "?? docs/context-layer/ops/RHP-021-2-current-operation-ci-wound-packet/foo.txt"])
    assert paths == ("README.md", "docs/context-layer/ops/RHP-021-2-current-operation-ci-wound-packet/foo.txt")


def test_bounded_residue_passes():
    result = classify_residue([
        " M README.md",
        "?? docs/context-layer/ops/RHP-021-2-current-operation-ci-wound-packet/raw.txt",
        " M rhp/current_operation_ci_wound_packet.py",
    ])
    assert result.ok
    assert result.unbounded_count == 0
    assert result.classification == "bounded_rhp_021_2_residue"


def test_unbounded_residue_blocks():
    result = classify_residue([" M pyproject.toml"])
    assert not result.ok
    assert result.unbounded_paths == ("pyproject.toml",)
    assert result.next_action == "stop_and_classify_unbounded_paths"
