from rhp.platform_tool_registry import RHP_PLATFORM_TOOL_REGISTRY_SCHEMA, registry, markdown_table

def test_rhp_014_4_platform_tool_registry_contains_fallback_and_gh():
    data = registry()
    names = [item["tool"] for item in data["tools"]]
    assert data["schema"] == RHP_PLATFORM_TOOL_REGISTRY_SCHEMA
    assert "local-paste-fallback" in names
    assert "gh-cli-run-view" in names

def test_rhp_014_4_registry_table():
    table = markdown_table()
    assert "| Tool | Box | Status | Authority | Purpose |" in table
    assert "CI-INGEST-BOX" in table
