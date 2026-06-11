from rhp.autoheal_executor_dry_run import RHP_AUTOHEAL_DRY_RUN_SCHEMA, dry_run_for_packet

def test_rhp_014_3_dry_run_never_mutates():
    dry = dry_run_for_packet({"classification": "stream_output_leak_or_crlf_noise"})
    data = dry.as_dict()
    assert data["schema"] == RHP_AUTOHEAL_DRY_RUN_SCHEMA
    assert data["ok"] is True
    assert data["would_mutate"] is False
    assert data["would_commit"] is False
    assert data["allowed_paths"]

def test_rhp_014_3_unknown_returns_diagnosis():
    dry = dry_run_for_packet({"classification": "unknown"})
    assert dry.ok is False
    assert dry.stop_reason
