from rhp.render_hygiene_auditor import audit


def test_rhp_015_5_render_hygiene_surfaces_have_real_lines():
    data = audit(".")
    assert data["ok"] is True
    assert data["errors"] == []


def test_rhp_015_5_render_hygiene_allows_documented_literal_newline_mentions():
    data = audit(".")
    docs = [check for check in data["checks"] if check["surface"] == "documentation"]
    assert docs
    assert all(check["unexpected_literal_backslash_n_count"] == 0 for check in docs)
