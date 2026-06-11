from rhp.stream_collapse import RHP_STREAM_COLLAPSE_SCHEMA, collapse

def test_rhp_014_2_stream_collapse_suppresses_crlf_and_git_status():
    text = "\n".join([
        "warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it",
        "M  README.md",
        "A  docs/context-layer/ops/file.txt",
        "[main abc123] commit message",
        "normal line",
    ])
    result, rendered = collapse(text, 0)
    assert result.schema == RHP_STREAM_COLLAPSE_SCHEMA
    assert result.crlf_warning_count == 1
    assert result.git_status_count == 2
    assert result.git_summary_count == 1
    assert "normal line" in rendered
    assert "raw: evidence artifact" in rendered
