
from rhp.remote_ci_result_ingestion import ingest

def test_rhp_015_4_remote_ci_ingestion_unknown_does_not_close():
    data = ingest("unknown", commit="abc", source="operator-provided")
    assert data["green"] is False
    assert data["closed"] is False
    assert data["pending"] is True

def test_rhp_015_4_remote_ci_ingestion_green_closes_status_only():
    data = ingest("green", commit="abc", source="operator-provided")
    assert data["green"] is True
    assert data["closed"] is True
    assert "does not call GitHub" in data["non_claim_lock"]
