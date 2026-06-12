from rhp.lane_declaration_gate import make_declaration, required_fields, validate_lane_declaration


def test_required_fields_are_declared():
    assert required_fields() == (
        "operation",
        "lane",
        "ci_state",
        "mutation_requested",
        "closure_requested",
    )


def test_orthogonal_lane_allows_mutation_under_unknown_ci():
    declaration = make_declaration("RHP-X", "canonization", "unknown", mutation_requested=True)
    result = validate_lane_declaration(declaration)
    assert result.allowed
    assert result.mutation_allowed
    assert not result.closure_allowed
    assert result.lane_kind == "orthogonal"


def test_blocked_lane_rejected_under_unknown_ci():
    declaration = make_declaration("RHP-X", "release", "unknown", mutation_requested=True)
    result = validate_lane_declaration(declaration)
    assert not result.allowed
    assert result.reason in {
        "ci_unresolved_blocks_this_lane",
        "mutation_requested_but_lane_does_not_allow_mutation",
    }


def test_missing_fields_rejected():
    result = validate_lane_declaration({"operation": "RHP-X"})
    assert not result.allowed
    assert "lane" in result.missing_fields


def test_closure_request_rejected_inside_gate_even_on_orthogonal_lane():
    declaration = make_declaration(
        "RHP-X",
        "observability",
        "unknown",
        mutation_requested=True,
        closure_requested=True,
    )
    result = validate_lane_declaration(declaration)
    assert not result.allowed
    assert result.reason == "closure_requested_inside_lane_gate"