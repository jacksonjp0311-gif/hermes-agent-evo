from rhp.advancement_lane_registry import decide_lane, lane_kind, registry


def test_known_orthogonal_lanes_are_allowed_under_unknown_ci():
    for lane in ["documentation", "canonization", "adapter", "tooling", "observability", "test_contract", "operator_experience"]:
        decision = decide_lane(lane, "unknown")
        assert decision.allowed
        assert decision.mutation_allowed
        assert not decision.closure_allowed
        assert decision.lane_kind == "orthogonal"


def test_blocked_lanes_are_blocked_under_unknown_ci():
    for lane in ["green_claim", "wound_closure", "release", "promotion", "dependency_mutation", "destructive_repair"]:
        decision = decide_lane(lane, "unknown")
        assert not decision.allowed
        assert not decision.mutation_allowed
        assert not decision.closure_allowed
        assert decision.reason == "ci_unresolved_blocks_this_lane"


def test_unknown_lane_blocks():
    decision = decide_lane("mystery", "unknown")
    assert not decision.allowed
    assert decision.lane_kind == "unknown"
    assert decision.reason == "lane_not_registered"


def test_lane_kind_lookup_and_registry_rule():
    assert lane_kind("adapter") == "orthogonal"
    assert lane_kind("release") == "blocked_when_ci_unresolved"
    assert registry()["rule"] == "Every operation must declare its lane before mutation."