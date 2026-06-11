from pathlib import Path
from rhp.command_runner import RHP_COMMAND_RUNNER_SCHEMA, run_captured

def test_rhp_014_2_v3_command_runner_captures_raw(tmp_path: Path):
    raw = tmp_path / "cmd.txt"
    result = run_captured(["python", "-c", "print('hello')"], cwd=".", raw_path=raw)
    data = result.as_dict()
    assert data["schema"] == RHP_COMMAND_RUNNER_SCHEMA
    assert data["ok"] is True
    assert raw.exists()
    assert "hello" in raw.read_text(encoding="utf-8")
