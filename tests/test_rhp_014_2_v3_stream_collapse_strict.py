from rhp.stream_collapse import collapse

def test_rhp_014_2_v3_stream_collapse_keeps_details_suppressed():
    text = "\n".join([
        "warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it",
        "M  README.md",
        "A  docs/context-layer/ops/file.txt",
        "[main abc123] commit message",
        " create mode 100644 file.txt",
        "normal diagnostic",
    ])
    result, rendered = collapse(text, 0)
    assert result.crlf_warning_count == 1
    assert result.git_status_count >= 2
    assert "raw: evidence artifact" in rendered
