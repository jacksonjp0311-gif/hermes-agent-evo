from rhp.rhpload_replay import replay


def test_rhp_015_6_rhpload_replay_latest_has_required_artifacts():
    data = replay(".")
    assert data["ok"] is True
    assert data["replay_completeness"] == 1.0
    assert data["required"]["final_evidence"] is True
