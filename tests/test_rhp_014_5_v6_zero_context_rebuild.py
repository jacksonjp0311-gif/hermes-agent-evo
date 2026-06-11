import json
from pathlib import Path
from rhp.zero_context_rebuild import build_packet

def test_zero_context_v6_includes_residue_and_error_boxes(tmp_path: Path):
    ops = tmp_path / "docs" / "context-layer" / "ops"
    ops.mkdir(parents=True)
    (ops / "RHP-014-5-v6-final-evidence.json").write_text(json.dumps({"operation":"RHP-014.5-v6","next_recommended_operation":"RHP-014.6","base_commit":"abc","self_authorization":False,"autonomous_authority":False}), encoding="utf-8")
    p = build_packet(tmp_path)
    assert "RESIDUE-MANAGER" in p.active_sequence
    assert "ERROR-BOX" in p.active_sequence
