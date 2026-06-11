from rhp.ci_wound_harvester import harvest


def test_rhp_015_2_ci_wound_harvester_classifies_import_wound():
    text = "ERROR collecting tests/test_rhp_014_3_autoheal_executor_dry_run.py ImportError cannot import name 'dry_run_for_packet'"
    result = harvest(text)
    assert result["primary_classification"] == "autoheal_dry_run_api_compatibility"
    assert "dry_run_for_packet" in result["missing_symbols"]
    assert "tests/test_rhp_014_3_autoheal_executor_dry_run.py" in result["failed_tests"]
