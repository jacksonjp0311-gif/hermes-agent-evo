
from rhp.loop_registry import RHP_LOOP_REGISTRY_SCHEMA, registry_as_dict, validate_loop

def test_rhp_013_8_loop_registry_contains_autoheal_plan():
    data = registry_as_dict()
    assert data["schema"] == RHP_LOOP_REGISTRY_SCHEMA
    assert "AUTOHEAL-PLAN" in data["loops"]
    assert data["loops"]["AUTOHEAL-PLAN"]["mutation_allowed"] is False

def test_rhp_013_8_registry_blocks_mutation_in_watch_loop():
    ok, failures = validate_loop("CI-WATCH", mutation_requested=True)
    assert ok is False
    assert "mutation_not_allowed" in failures

def test_rhp_013_8_registry_allows_bounded_autoheal_execute_attempt_one():
    ok, failures = validate_loop("AUTOHEAL-EXECUTE", mutation_requested=True, commit_requested=True, attempt=1)
    assert ok is True
    assert failures == []

def test_rhp_013_8_registry_blocks_attempt_over_budget():
    ok, failures = validate_loop("AUTOHEAL-EXECUTE", mutation_requested=True, commit_requested=True, attempt=2)
    assert ok is False
    assert "attempt_budget_exceeded" in failures
