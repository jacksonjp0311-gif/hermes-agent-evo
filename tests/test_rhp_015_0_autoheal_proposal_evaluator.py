from rhp.autoheal_proposal_evaluator import evaluate

def test_rhp_015_0_autoheal_proposal_evaluator_does_not_execute():
    result = evaluate({"failures": ["root_readme_latest_evidence", "boot_preflight_ok_false"]})
    assert result["dry_run_only"] is True
    assert result["autoheal_execution_enabled"] is False
    assert all(action["executes"] is False for action in result["actions"])
