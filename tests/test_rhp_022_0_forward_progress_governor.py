from rhp.forward_progress_governor import advancement_policy, decide_forward_progress


def test_unknown_ci_allows_orthogonal_canonization():
    decision = decide_forward_progress("canonization", "unknown")
    assert decision.allowed
    assert decision.reason == "orthogonal_advancement_allowed_while_ci_unresolved"
    assert decision.next_state == "advance_with_open_wound_preserved"


def test_unknown_ci_blocks_closure_and_release():
    assert not decide_forward_progress("wound_closure", "unknown").allowed
    assert not decide_forward_progress("release", "pending").allowed
    assert not decide_forward_progress("green_claim", "failure").allowed


def test_success_ci_can_route_to_human_authorized_closure_proposal():
    decision = decide_forward_progress("wound_closure", "success")
    assert decision.allowed
    assert decision.next_state == "human_authorized_closure_or_release_proposal"


def test_unregistered_lane_blocks_with_diag():
    decision = decide_forward_progress("mystery_lane", "unknown")
    assert not decision.allowed
    assert decision.next_state == "stop_with_rhpdiag"


def test_policy_names_core_rule():
    policy = advancement_policy()
    assert "canonization" in policy["orthogonal_advancement_lanes"]
    assert "release" in policy["blocked_by_unresolved_ci"]
    assert "unknown" in policy["known_ci_states"]
    assert "does not block orthogonal system advancement" in policy["core_rule"]