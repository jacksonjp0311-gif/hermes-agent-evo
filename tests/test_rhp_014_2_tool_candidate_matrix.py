from rhp.tool_candidate_matrix import RHP_TOOL_CANDIDATE_MATRIX_SCHEMA, matrix, markdown_table

def test_rhp_014_2_tool_candidate_matrix_contains_ci_and_otel():
    data = matrix()
    names = [item["name"] for item in data["candidates"]]
    assert data["schema"] == RHP_TOOL_CANDIDATE_MATRIX_SCHEMA
    assert "GitHub Actions workflow commands" in names
    assert "OpenTelemetry-style signals" in names

def test_rhp_014_2_tool_candidate_markdown_table():
    table = markdown_table()
    assert "| Candidate | Loop box | Purpose | Integration | Authority |" in table
    assert "CI-WATCH-BOX" in table
