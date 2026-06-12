from rhp.runtime_loop import (
    RUNTIME_LOOP_ORDER,
    classify_command_records,
    render_command_summary_panel,
    render_runtime_loop_order_panel,
    render_self_learning_runtime_panel,
)


def test_runtime_loop_places_self_learning_before_summary():
    assert "RHPLOOP-DOCTOR" in RUNTIME_LOOP_ORDER
    assert "RHPLOOP-SELF-LEARNING" in RUNTIME_LOOP_ORDER
    assert "RHPREFLECT" in RUNTIME_LOOP_ORDER
    assert "HUMAN-UI-SUMMARY" in RUNTIME_LOOP_ORDER
    assert RUNTIME_LOOP_ORDER.index("RHPLOOP-DOCTOR") < RUNTIME_LOOP_ORDER.index("RHPLOOP-SELF-LEARNING")
    assert RUNTIME_LOOP_ORDER.index("RHPLOOP-SELF-LEARNING") < RUNTIME_LOOP_ORDER.index("RHPREFLECT")
    assert RUNTIME_LOOP_ORDER.index("RHPREFLECT") < RUNTIME_LOOP_ORDER.index("HUMAN-UI-SUMMARY")


def test_diagnostic_nonzero_is_not_hard_failure():
    records = [
        {"stage": "operation-base-commit", "exit": 0},
        {"stage": "doctor-cli-readonly", "exit": 1},
        {"stage": "focused-tests", "exit": 0},
    ]
    summary = classify_command_records(records)
    assert summary.total == 3
    assert summary.ok == 2
    assert summary.diagnostic_nonzero == 1
    assert summary.hard_failed == 0
    panel = render_command_summary_panel(records)
    assert "diagnostic-nonzero: 1" in panel
    assert "hard-failed: 0" in panel
    assert "status=ok" in panel


def test_runtime_loop_order_panel_renders_gold_runtime_contract():
    text = render_runtime_loop_order_panel()
    assert "RHPLOOP-RUNTIME [GOLD]" in text
    assert "RHPLOOP-SELF-LEARNING" in text
    assert "doctor and self-learning run before reflection and human summary" in text


def test_self_learning_runtime_panel_is_before_final_summary_contract():
    text = render_self_learning_runtime_panel(
        observed_event="RHP-018.9 compressed self-learning into final summary",
        evidence_path="docs/context-layer/ops/RHP-018-9-final-evidence.json",
        lesson="self-learning must be runtime panel before final summary",
        future_behavior_change="render RHPLOOP-SELF-LEARNING before RHPREFLECT and HUMAN-UI-SUMMARY",
    )
    assert "RHPLOOP-SELF-LEARNING [GOLD]" in text
    assert "runtime lesson checkpoint before final summary" in text
    assert "promotion: evidence-gated / human-authorized [LOCKED]" in text
