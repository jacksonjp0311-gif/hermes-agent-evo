
from pathlib import Path
from rhp.load_console import RHPLOAD_LIVE_SCHEMA, LoadEvent, append_event, read_transcript, render_event, summarize_transcript

def test_rhp_013_7_render_event_expanded():
    event = LoadEvent(42, "validate transcript", "running", "EVIDENCE", "RHP-013.7", "jsonl")
    text = render_event(event)
    assert "RHPLOAD [042%]" in text
    assert "live feedback" in text
    assert "transcript: jsonl" in text

def test_rhp_013_7_transcript_round_trip(tmp_path: Path):
    path = tmp_path / "rhpload.jsonl"
    append_event(path, LoadEvent(10, "rehydrate", "ok", "REHYDRATION", "RHP-013.7"))
    append_event(path, LoadEvent(100, "complete", "ok", "CI-WATCH", "RHP-013.7"))
    rows = read_transcript(path)
    summary = summarize_transcript(path)
    assert rows[0]["schema"] == RHPLOAD_LIVE_SCHEMA
    assert summary["event_count"] == 2
    assert summary["last_percent"] == 100
    assert summary["ok"] is True
