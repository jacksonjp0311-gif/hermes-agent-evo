from rhp.rhp_021_2r2_local_residue_settlement import settlement_ok

def test_settlement_ok():
    assert settlement_ok("RHP-021.2R", "RHP_021_2_POST_SEAL_RESIDUE_CLASSIFIED", 0)

def test_settlement_blocks_dirty():
    assert not settlement_ok("RHP-021.2R", "RHP_021_2_POST_SEAL_RESIDUE_CLASSIFIED", 1)