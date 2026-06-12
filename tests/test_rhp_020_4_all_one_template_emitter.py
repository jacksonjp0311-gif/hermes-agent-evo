from rhp.all_one_template_emitter import (
    CANONICAL_STAGE_ORDER,
    FORBIDDEN_TEMPLATE_ACTIONS,
    REQUIRED_TEMPLATE_SECTIONS,
    canonical_all_one_template_skeleton,
    emitter_contract_to_dict,
    render_template_emitter_panel,
    template_metadata,
    validate_template_emitter,
)


def good_generator_contract():
    return {
        "schema": "RHP-ALL-ONE-GENERATOR-CONTRACT-v0.1",
        "report": {
            "ok": True,
            "stage_contract_ok": True,
            "rule_contract_ok": True,
            "forbidden_contract_ok": True,
            "trace_contract_ok": True,
            "authority_contract_ok": True,
            "blocking_reasons": [],
        },
    }


def test_template_metadata_preserves_19_stage_order():
    metadata = template_metadata()
    assert metadata["stage_count"] == 19
    assert tuple(metadata["stage_order"]) == CANONICAL_STAGE_ORDER
    assert metadata["grants_authority"] is False
    assert metadata["closes_wound"] is False
    assert metadata["repairs_code"] is False
    assert metadata["claims_current_operation_ci_green"] is False


def test_template_has_required_sections_and_forbidden_actions():
    metadata = template_metadata()
    for section in REQUIRED_TEMPLATE_SECTIONS:
        assert section in metadata["required_sections"]
    for action in FORBIDDEN_TEMPLATE_ACTIONS:
        assert action in metadata["forbidden_actions"]


def test_good_generator_contract_allows_template_emission():
    report = validate_template_emitter(good_generator_contract())
    assert report.ok
    assert report.blocking_reasons == ()


def test_bad_generator_contract_blocks_template_emission():
    bad = good_generator_contract()
    bad["report"]["trace_contract_ok"] = False
    report = validate_template_emitter(bad)
    assert not report.ok
    assert "generator_contract_not_ok" in report.blocking_reasons


def test_skeleton_contains_required_loop_stage_labels():
    skeleton = canonical_all_one_template_skeleton()
    assert "STAGE 01 ENTRYPOINT-GATE" in skeleton
    assert "STAGE 19 HUMAN-UI-SUMMARY" in skeleton
    assert "PREAUTH-PULL" in skeleton
    assert "SECRET-SCAN" in skeleton
    assert "POST-SEAL-RESIDUE" in skeleton
    assert "NON-CLAIM LOCK" in skeleton


def test_panel_and_contract_dict_render():
    report = validate_template_emitter(good_generator_contract())
    panel = render_template_emitter_panel(report)
    data = emitter_contract_to_dict(report)
    assert "RHPTEMPLATE-EMIT [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
    assert data["report"]["ok"] is True
    assert data["metadata"]["stage_count"] == 19
    assert "RHP Canonical All-One Template Skeleton" in data["skeleton_preview"]
