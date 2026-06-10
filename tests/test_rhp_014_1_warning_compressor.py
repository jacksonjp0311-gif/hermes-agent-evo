from rhp.warning_compressor import RHP_WARNING_COMPRESSOR_SCHEMA, compress

def test_rhp_014_1_warning_compressor_collapses_crlf():
    text = "\n".join([
        "warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it",
        "warning: in the working copy of 'AGENTS.md', LF will be replaced by CRLF the next time Git touches it",
        "normal output",
    ])
    summary, rendered = compress(text)
    assert summary.schema == RHP_WARNING_COMPRESSOR_SCHEMA
    assert summary.crlf_warning_count == 2
    assert "CRLF warnings compressed: 2" in rendered
    assert "normal output" in rendered
