from rhp.connector_observation_adapter import (
    ADAPTER_SCHEMA,
    connector_observation_contract,
    make_unknown_connector_observation,
    render_connector_observation_panel,
    report_to_dict,
    validate_connector_observation,
)


SUBJECT = "ddb24363e2fac630e7527a2c9eab31e6df50db52"


def test_contract_declares_no_authority():
    contract = connector_observation_contract()
    assert contract["schema"] == ADAPTER_SCHEMA
    assert contract["rules"]["connector_authorizes"] is False
    assert contract["rules"]["unknown_is_not_pass"] is True


def test_unknown_observation_validates_without_authority():
    obs = make_unknown_connector_observation(
        subject_commit=SUBJECT,
        source="github-connector",
        raw_reference="manual-next-observation-required",
    )
    report = validate_connector_observation(obs, expected_subject_commit=SUBJECT)
    assert report.ok
    assert report.blocking_reasons == ()


def test_subject_mismatch_blocks():
    obs = make_unknown_connector_observation(
        subject_commit="wrong",
        source="github-connector",
        raw_reference="manual-next-observation-required",
    )
    report = validate_connector_observation(obs, expected_subject_commit=SUBJECT)
    assert not report.ok
    assert "subject_commit_mismatch" in report.blocking_reasons


def test_authority_grant_blocks():
    obs = make_unknown_connector_observation(
        subject_commit=SUBJECT,
        source="github-connector",
        raw_reference="manual-next-observation-required",
    )
    obs["authority_granted"] = True
    report = validate_connector_observation(obs, expected_subject_commit=SUBJECT)
    assert not report.ok
    assert "connector_authority_grant_detected" in report.blocking_reasons


def test_forbidden_interpretation_blocks():
    obs = make_unknown_connector_observation(
        subject_commit=SUBJECT,
        source="github-connector",
        raw_reference="manual-next-observation-required",
    )
    obs["interpretation"] = "current_operation_green"
    report = validate_connector_observation(obs, expected_subject_commit=SUBJECT)
    assert not report.ok
    assert "forbidden_interpretation_detected" in report.blocking_reasons


def test_panel_and_dict_render():
    obs = make_unknown_connector_observation(
        subject_commit=SUBJECT,
        source="github-connector",
        raw_reference="manual-next-observation-required",
    )
    report = validate_connector_observation(obs, expected_subject_commit=SUBJECT)
    panel = render_connector_observation_panel(report)
    data = report_to_dict(report)
    assert data["ok"] is True
    assert "RHPCONNECTOR-OBS [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
