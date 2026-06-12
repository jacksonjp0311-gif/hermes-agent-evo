from rhp.rhp_021_4_post_repair_ci_observation import green_eligible

def test_green_eligible_requires_success_and_surface():
    assert green_eligible("success", 1, 0)
    assert green_eligible("success", 0, 1)
    assert not green_eligible("success", 0, 0)
    assert not green_eligible("failure", 1, 1)