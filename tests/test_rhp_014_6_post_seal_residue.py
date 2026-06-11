from rhp.post_seal_residue import classify_paths

def test_post_seal_residue_accepts_known_014_5_stream():
    report = classify_paths(["docs/context-layer/ops/RHP-014-5-v6-residue-manager-error-box-zero-context/command-streams/push.txt"])
    assert report.ok is True
    assert report.classification == "bounded_post_seal_command_residue"

def test_post_seal_residue_blocks_unknown_path():
    report = classify_paths(["README.md"])
    assert report.ok is False
    assert report.blocked == ["README.md"]
