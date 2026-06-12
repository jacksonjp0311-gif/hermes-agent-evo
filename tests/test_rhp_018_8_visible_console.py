from rhp.visible_console import (
    ConsoleField,
    ConsolePanel,
    minimum_panel_fields,
    render_panel,
    render_reflection_panel,
    required_uncompressed_stages,
)


def test_render_panel_includes_tree_fields_and_footer():
    panel = ConsolePanel(
        tag="RHPREADY [DIAGNOSTIC]",
        title="readiness diagnostic evidence",
        status="allowed",
        tone="gold",
        fields=[
            ConsoleField("exit", "0"),
            ConsoleField("state", "WOUND_OPEN"),
            ConsoleField("allowed", "true"),
        ],
        footer="authority: no grant [LOCKED]",
    )
    text = render_panel(panel)
    assert "RHPREADY [DIAGNOSTIC]" in text
    assert "`- readiness diagnostic evidence" in text
    assert "+- state: WOUND_OPEN" in text
    assert "authority: no grant [LOCKED]" in text


def test_reflection_panel_names_state_wound_and_learning():
    text = render_reflection_panel(
        operation="RHP-018.8",
        state="UNCOMPRESSED_OPERATOR_CONSOLE_CANON_ALIGNED_SUBJECT_UNRESOLVED",
        active_wound="readiness_gate_install",
        subject_commit="ddb24363",
        repair_basis=False,
        next_operation="operator_rerun_or_ingest_replacement_ci_before_repair",
        learned=[
            "RHP is an observability loop",
            "gold panels carry reflection and diagnostic context",
        ],
    )
    assert "RHPREFLECT [GOLD]" in text
    assert "repair-basis: false" in text
    assert "operator_rerun_or_ingest_replacement_ci_before_repair" in text
    assert "RHP is an observability loop" in text


def test_required_stage_contract_contains_debug_and_summary_surfaces():
    stages = required_uncompressed_stages()
    assert "RHPDIAG" in stages
    assert "RHPDROP" in stages
    assert "RHPREADY" in stages
    assert "HUMAN-UI-SUMMARY" in stages
    assert "RHPREFLECT" in stages


def test_minimum_panel_fields_include_next_and_authority():
    fields = minimum_panel_fields()
    assert "decision" in fields
    assert "authority" in fields
    assert "next" in fields
