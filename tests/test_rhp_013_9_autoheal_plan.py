
from rhp.autoheal_plan import RHP_AUTOHEAL_PLAN_SCHEMA, plan_for_classification

def test_rhp_013_9_plan_dirty_residue():
    plan = plan_for_classification("dirty_worktree_and_module_path_execution_bug", "RHP-013.9")
    assert plan.schema == RHP_AUTOHEAL_PLAN_SCHEMA
    assert plan.ok is True
    assert plan.loop == "AUTOHEAL-PLAN"
    assert plan.mutation_allowed_now is False
    assert plan.commit_allowed_now is False
    assert plan.attempt_budget == 1

def test_rhp_013_9_plan_module_execution_bug():
    plan = plan_for_classification("module_path_execution_bug", "RHP-013.9")
    assert plan.ok is True
    assert plan.repair_strategy == "package_module_execution"

def test_rhp_013_9_plan_unknown_requires_diagnosis():
    plan = plan_for_classification("unclassified_wound", "RHP-013.9")
    assert plan.ok is False
    assert plan.loop == "DIAGNOSIS"
