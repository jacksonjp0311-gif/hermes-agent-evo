from rhp.replacement_ci_observer import (
    SUBJECT_COMMIT,
    classify_replacement_ci_observation,
    normalize_status,
    observation_to_dict,
    render_replacement_ci_panel,
)


def test_normalize_status():
    assert normalize_status("GREEN") == "green"
    assert normalize_status("red") == "red"
    assert normalize_status("nonsense") == "unknown"


def test_subject_scoped_green_only_allows_wound_closure_next_not_now():
    obs = classify_replacement_ci_observation(
        subject_commit=SUBJECT_COMMIT,
        observed_status="green",
        source="operator-provided replacement CI",
        source_scope="subject_commit",
        evidence_note="green check on subject commit",
    )
    assert obs.replacement_ci_established is True
    assert obs.wound_closure_allowed_next is True
    assert obs.repair_allowed_next is False
    assert obs.next_operation == "close_active_subject_wound_after_subject_scoped_green_ci"


def test_green_not_subject_scoped_does_not_establish_replacement_ci():
    obs = classify_replacement_ci_observation(
        subject_commit=SUBJECT_COMMIT,
        observed_status="green",
        source="green screenshot from another commit",
        source_scope="current_operation",
        evidence_note="wrong scope",
    )
    assert obs.replacement_ci_established is False
    assert obs.wound_closure_allowed_next is False
    assert obs.next_operation == "operator_rerun_or_ingest_replacement_ci_before_repair"


def test_subject_scoped_red_requires_failed_logs_before_repair():
    obs = classify_replacement_ci_observation(
        subject_commit=SUBJECT_COMMIT,
        observed_status="red",
        source="operator-provided replacement CI",
        source_scope="subject_commit",
        evidence_note="red replacement CI",
    )
    assert obs.replacement_ci_established is True
    assert obs.wound_closure_allowed_next is False
    assert obs.repair_allowed_next is False
    assert obs.next_operation == "ingest_failed_replacement_ci_logs_before_repair"


def test_subject_scoped_pending_waits_for_final():
    obs = classify_replacement_ci_observation(
        subject_commit=SUBJECT_COMMIT,
        observed_status="pending",
        source="operator-provided replacement CI",
        source_scope="subject_commit",
        evidence_note="pending replacement CI",
    )
    assert obs.replacement_ci_established is True
    assert obs.next_operation == "wait_or_ingest_final_replacement_ci_result"


def test_panel_and_dict_render():
    obs = classify_replacement_ci_observation(
        subject_commit=SUBJECT_COMMIT,
        observed_status="unknown",
        source="connector returned no workflow runs",
        source_scope="unknown",
        evidence_note="no status surface",
    )
    data = observation_to_dict(obs)
    panel = render_replacement_ci_panel(obs)
    assert data["classification"] == "replacement_ci_not_established"
    assert "RHPCI [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
