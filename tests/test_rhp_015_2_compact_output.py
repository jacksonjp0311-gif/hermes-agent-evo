from rhp.compact_output import render_closed, summarize


def test_rhp_015_2_compact_output_closed_summary():
    summary = summarize(
        [{"stage": "a", "exit": 0, "raw": "a.txt"}, {"stage": "b", "exit": 0, "raw": "b.txt"}],
        operation="RHP-015.2",
        group="operation-commands",
    )
    text = render_closed(summary)
    assert summary["failed"] == 0
    assert "RHPDROP [closed]" in text
    assert "commands: 2" in text
