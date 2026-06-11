from rhp.residue_manager import classify_paths

def test_residue_manager_allows_old_rhp0145_tests():
    r = classify_paths(["tests/test_rhp_014_5_zero_context_rebuild.py"])
    assert r.ok is True
    assert r.classification == "bounded_failed_run_residue"

def test_residue_manager_blocks_unknown_source():
    r = classify_paths(["hermes_cli/main.py"])
    assert r.ok is False
    assert r.blocked == ["hermes_cli/main.py"]
