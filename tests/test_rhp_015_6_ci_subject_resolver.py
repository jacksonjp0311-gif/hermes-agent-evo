from rhp.ci_subject_resolver import resolve


def test_rhp_015_6_ci_subject_resolver_scopes_previous_green_not_current():
    data = resolve(
        previous_commit="prev",
        previous_ci_status="green",
        current_head="head",
        current_head_ci_status="pending",
        source="operator-provided",
    )
    assert data["previous_green_applies_to_current_head"] is False
    assert data["current_head_green"] is False
    current = [c for c in data["claims"] if c["claim"] == "current_head_remote_ci_status"][0]
    assert current["subject_id"] == "head"
    assert current["status"] == "pending"
