from rhp.dev_loop_chart import RHP_DEV_LOOP_CHART_SCHEMA, chart, markdown_table

def test_rhp_014_1_dev_loop_chart_contains_required_boxes():
    data = chart()
    names = [item["box"] for item in data["tools"]]
    assert data["schema"] == RHP_DEV_LOOP_CHART_SCHEMA
    assert "AUTOHEAL-PREFLIGHT" in names
    assert "CURRENT-SCRIPT-GATE" in names
    assert "WARNING-COMPRESSOR" in names
    assert "GITHUB-PUSH-BOX" in names
    assert "RETURN-ROOT" in data["sequence"]

def test_rhp_014_1_markdown_table_renders():
    table = markdown_table()
    assert "| Box | Tool | Purpose |" in table
    assert "warning_compressor.py" in table
