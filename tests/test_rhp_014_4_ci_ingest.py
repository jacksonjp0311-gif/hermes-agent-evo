import json
from pathlib import Path
from rhp.ci_ingest import RHP_CI_INGEST_SCHEMA, ingest_text, ingest_github_json, build_gh_command

def test_rhp_014_4_ingest_text():
    packet = ingest_text("FAILED test\nAssertionError", "sample")
    data = packet.as_dict()
    assert data["schema"] == RHP_CI_INGEST_SCHEMA
    assert data["ok"] is True
    assert data["source_mode"] == "text"
    assert data["normalized_text_length"] > 0

def test_rhp_014_4_ingest_github_json(tmp_path: Path):
    path = tmp_path / "run.json"
    path.write_text(json.dumps({"name": "Tests", "conclusion": "failure", "jobs": [{"name": "test", "conclusion": "failure", "steps": [{"name": "pytest", "conclusion": "failure"}]}]}), encoding="utf-8")
    packet = ingest_github_json(path)
    assert packet.ok is True
    assert "job: test" in packet.normalized_text
    assert "step: pytest" in packet.normalized_text

def test_rhp_014_4_build_gh_command():
    cmd = build_gh_command("123", "owner/repo")
    assert cmd[:3] == ["gh", "run", "view"]
    assert "--repo" in cmd
