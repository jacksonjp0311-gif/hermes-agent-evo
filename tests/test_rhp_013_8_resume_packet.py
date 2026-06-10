
from pathlib import Path
from rhp.resume_packet import RHP_RESUME_PACKET_SCHEMA, build_resume_packet, find_latest_evidence

def test_rhp_013_8_find_latest_evidence():
    latest = find_latest_evidence(Path.cwd())
    assert latest.name.endswith("-final-evidence.json")
    assert "RHP-" in latest.name

def test_rhp_013_8_resume_packet_builds_from_repo():
    packet = build_resume_packet(Path.cwd())
    data = packet.as_dict()
    assert data["schema"] == RHP_RESUME_PACKET_SCHEMA
    assert data["latest_evidence"]
    assert data["latest_operation"].startswith("RHP-")
    assert data["recommended_loop"] in {"EVOLUTION", "CI-WATCH", "DIAGNOSIS", "AUTOHEAL-PLAN"}
    assert data["authority"]["self_authorization"] is False
