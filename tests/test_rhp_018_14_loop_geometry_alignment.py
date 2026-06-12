from pathlib import Path

from rhp.loop_geometry import (
    FULL_RUNTIME_GEOMETRY,
    VISIBLE_BODY_GEOMETRY,
    extract_loop_geometry_from_text,
    render_geometry_panel,
    validate_full_runtime_geometry,
    validate_readme_geometry,
    validate_visible_body_geometry,
)


def test_full_runtime_geometry_contains_all_required_loops():
    assert FULL_RUNTIME_GEOMETRY == (
        "ENTRYPOINT-GATE",
        "ROOT-ANCHOR",
        "RESIDUE-MANAGER",
        "PREAUTH-PULL",
        "RHPLOOP-RUNTIME",
        "HUMAN-AUTHORIZATION",
        "RHPREADY",
        "OPERATION-START",
        "RHPLOOP-DOCTOR",
        "RHPLOOP-SELF-LEARNING",
        "VALIDATION",
        "SECRET-SCAN",
        "COMMIT-SEAL",
        "PUSH-SEAL",
        "RHPDROP",
        "RHPREFLECT",
        "POST-SEAL-RESIDUE",
        "RETURN-ROOT",
        "HUMAN-UI-SUMMARY",
    )


def test_visible_body_geometry_has_doctor_self_learning_reflect_summary():
    assert VISIBLE_BODY_GEOMETRY.index("RHPLOOP-DOCTOR") < VISIBLE_BODY_GEOMETRY.index("RHPLOOP-SELF-LEARNING")
    assert VISIBLE_BODY_GEOMETRY.index("RHPLOOP-SELF-LEARNING") < VISIBLE_BODY_GEOMETRY.index("RHPREFLECT")
    assert VISIBLE_BODY_GEOMETRY.index("RHPREFLECT") < VISIBLE_BODY_GEOMETRY.index("HUMAN-UI-SUMMARY")


def test_extract_geometry_from_runtime_text():
    text = """
RHPLOAD [005%] loop=ENTRYPOINT-GATE operation=RHP-X | status=ok tone=green
RHPREADY [DIAGNOSTIC] class=x decision=pending
RHPLOOP-DOCTOR [GOLD] status=aligned
RHPLOOP-SELF-LEARNING [GOLD] status=runtime-checkpoint
RHPDROP [closed] status=ok tone=gold
RHPREFLECT [GOLD] status=aligned
RHPLOAD [100%] loop=HUMAN-UI-SUMMARY operation=RHP-X | status=ok tone=gold
"""
    observed = extract_loop_geometry_from_text(text)
    assert observed == (
        "ENTRYPOINT-GATE",
        "RHPREADY",
        "RHPLOOP-DOCTOR",
        "RHPLOOP-SELF-LEARNING",
        "RHPDROP",
        "RHPREFLECT",
        "HUMAN-UI-SUMMARY",
    )


def test_full_geometry_report_passes_when_exact():
    report = validate_full_runtime_geometry(FULL_RUNTIME_GEOMETRY)
    assert report.ok
    assert not report.missing
    assert not report.unexpected


def test_visible_geometry_report_blocks_missing_self_learning():
    observed = (
        "RHPREADY",
        "RHPLOOP-DOCTOR",
        "RHPDROP",
        "RHPREFLECT",
        "POST-SEAL-RESIDUE",
        "RETURN-ROOT",
        "HUMAN-UI-SUMMARY",
    )
    report = validate_visible_body_geometry(observed)
    assert not report.ok
    assert report.missing == ("RHPLOOP-SELF-LEARNING",)


def test_synthetic_canonical_run_block_matches_full_geometry():
    synthetic_readme = """
<!-- RHP_CANONICAL_RUNTIME_RUN_BLOCK_START -->
```text
RHPLOAD [005%] loop=ENTRYPOINT-GATE operation=<OPERATION> | status=ok tone=green
RHPLOAD [010%] loop=ROOT-ANCHOR operation=<OPERATION> | status=ok tone=green
RHPLOAD [015%] loop=RESIDUE-MANAGER operation=<OPERATION> | status=ok tone=green
RHPLOAD [020%] loop=PREAUTH-PULL operation=<OPERATION> | status=ok tone=green
RHPLOAD [025%] loop=RHPLOOP-RUNTIME operation=<OPERATION> | status=preauth tone=gold
RHPLOAD [030%] loop=HUMAN-AUTHORIZATION operation=<OPERATION> | status=ok tone=green
RHPREADY [DIAGNOSTIC] class=<class> decision=<allowed|blocked|pending>
RHPLOAD [040%] loop=OPERATION-START operation=<OPERATION> | status=running tone=green
RHPLOOP-DOCTOR [GOLD] status=<diagnostic|preserved|aligned>
RHPLOOP-SELF-LEARNING [GOLD] status=runtime-checkpoint
RHPLOAD [070%] loop=VALIDATION operation=<OPERATION> | status=ok tone=green
RHPLOAD [078%] loop=SECRET-SCAN operation=<OPERATION> | status=ok tone=green
RHPLOAD [084%] loop=COMMIT-SEAL operation=<OPERATION> | status=ok tone=green
RHPLOAD [090%] loop=PUSH-SEAL operation=<OPERATION> | status=ok tone=green
RHPDROP [closed] status=ok tone=gold
RHPREFLECT [GOLD] status=aligned
RHPLOAD [098%] loop=POST-SEAL-RESIDUE operation=<OPERATION> | status=ok tone=green
RHPLOAD [099%] loop=RETURN-ROOT operation=<OPERATION> | status=ok tone=green
RHPLOAD [100%] loop=HUMAN-UI-SUMMARY operation=<OPERATION> | status=ok tone=gold
```
<!-- RHP_CANONICAL_RUNTIME_RUN_BLOCK_END -->
"""
    report = validate_readme_geometry(synthetic_readme)
    assert report.ok, report


def test_geometry_panel_renders_status_and_authority_lock():
    report = validate_full_runtime_geometry(FULL_RUNTIME_GEOMETRY)
    panel = render_geometry_panel(report, operation="RHP-018.14")
    assert "RHPLOOP-GEOMETRY [GOLD]" in panel
    assert "status=aligned" in panel
    assert "authority: no grant [LOCKED]" in panel
