
import json
from pathlib import Path
from rhp.current_script_gate import RHP_CURRENT_SCRIPT_GATE_SCHEMA, validate_current_script

def test_rhp_014_0_current_script_gate_passes(tmp_path: Path):
    evidence = tmp_path / "evidence.json"
    evidence.write_text(json.dumps({"operation": "RHP-014.0", "operator_script_name": "run.ps1"}), encoding="utf-8")
    gate = validate_current_script("RHP-014.0", "run.ps1", "run.ps1", evidence)
    assert gate.schema == RHP_CURRENT_SCRIPT_GATE_SCHEMA
    assert gate.ok is True
    assert gate.glyph == "[OK]"

def test_rhp_014_0_current_script_gate_blocks_mismatch(tmp_path: Path):
    evidence = tmp_path / "evidence.json"
    evidence.write_text(json.dumps({"operation": "RHP-014.0", "operator_script_name": "other.ps1"}), encoding="utf-8")
    gate = validate_current_script("RHP-014.0", "run.ps1", "run.ps1", evidence)
    assert gate.ok is False
    assert "evidence_script_mismatch" in gate.failures
