from rhp.machine_report_registry import registry

def test_machine_report_registry_lists_outputs():
    data = registry()
    names = [r["name"] for r in data["reports"]]
    assert "github-summary" in names
    assert "junit" in names
    assert "sarif" in names
    assert "post-seal-residue" in names
