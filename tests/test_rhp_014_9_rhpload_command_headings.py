from rhp.rhpload_command_headings import heading_for, registry

def test_command_heading_for_pull_rebase_preauth():
    data = heading_for("pull-rebase-preauth")
    assert "Pre-authorization" in data["heading"]
    assert data["command"] == "git pull --rebase origin main"

def test_command_heading_registry_has_non_claim_lock():
    data = registry()
    assert data["schema"] == "RHPLOAD-COMMAND-HEADINGS-v0.1"
    assert "non_claim_lock" in data
