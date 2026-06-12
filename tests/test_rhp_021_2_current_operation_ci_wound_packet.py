from rhp.current_operation_ci_wound_packet import (
    CURRENT_OPERATION_COMMIT,
    INHERITED_SUBJECT_COMMIT,
    classify_current_operation_ci_wounds,
    render_current_operation_ci_wound_panel,
    validate_current_operation_ci_wound_packet,
)


def packet():
    return {
        "current_operation_commit": CURRENT_OPERATION_COMMIT,
        "inherited_subject_commit": INHERITED_SUBJECT_COMMIT,
        "current_operation_ci_status": "failure",
        "wound_classes": [
            "zero_context_next_operation_contract_drift",
            "loop_geometry_legacy_api_drift",
        ],
        "repair_execution_enabled": False,
        "repair_executed": False,
    }


def test_classifies_contract_drift_and_legacy_api_drift():
    wounds = classify_current_operation_ci_wounds([
        "expected operator_rerun_or_ingest_replacement_ci_before_repair got operator_rerun_ci_or_provide_replacement_green_subject_observation",
        "ImportError: cannot import name 'geometry' from rhp.loop_geometry / from rhp.loop_geometry import geometry",
    ])
    assert "zero_context_next_operation_contract_drift" in wounds
    assert "loop_geometry_legacy_api_drift" in wounds


def test_valid_packet_passes():
    report = validate_current_operation_ci_wound_packet(packet())
    assert report.ok
    assert report.blocking_reasons == ()


def test_current_operation_commit_mismatch_blocks():
    p = packet()
    p["current_operation_commit"] = "wrong"
    report = validate_current_operation_ci_wound_packet(p)
    assert not report.ok
    assert "current_operation_commit_mismatch" in report.blocking_reasons


def test_subject_mismatch_blocks():
    p = packet()
    p["inherited_subject_commit"] = "wrong"
    report = validate_current_operation_ci_wound_packet(p)
    assert not report.ok
    assert "inherited_subject_commit_mismatch" in report.blocking_reasons


def test_repair_execution_blocks():
    p = packet()
    p["repair_executed"] = True
    report = validate_current_operation_ci_wound_packet(p)
    assert not report.ok
    assert "repair_execution_detected" in report.blocking_reasons


def test_panel_render():
    report = validate_current_operation_ci_wound_packet(packet())
    panel = render_current_operation_ci_wound_panel(report, packet()["wound_classes"])
    assert "RHPCI-WOUND [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
