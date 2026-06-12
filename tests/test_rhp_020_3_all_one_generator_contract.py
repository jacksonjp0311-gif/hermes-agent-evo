from rhp.all_one_generator_contract import (
    FORBIDDEN_CAPABILITIES,
    REQUIRED_ALL_ONE_RULES,
    REQUIRED_CANONICAL_STAGES,
    generator_contract_to_dict,
    render_all_one_generator_contract_panel,
    validate_all_one_generator_contract,
)


def good_trace():
    return {
        "stage_order": list(REQUIRED_CANONICAL_STAGES),
        "stage_count": 19,
        "exact_script_bound": True,
        "installed_module": "rhp/runtime_script_trace_map.py",
        "evidence_location": "docs/context-layer/ops/RHP-020-1-exact-runtime-script-trace-map/",
        "stages": [
            {
                "stage": stage,
                "grants_authority": False,
                "closes_wound": False,
                "repairs_code": False,
                "claims_current_operation_ci_green": False,
            }
            for stage in REQUIRED_CANONICAL_STAGES
        ],
    }


def test_good_contract_passes():
    report = validate_all_one_generator_contract(trace_map=good_trace())
    assert report.ok
    assert report.blocking_reasons == ()


def test_stage_order_mismatch_blocks():
    trace = good_trace()
    trace["stage_order"] = list(reversed(trace["stage_order"]))
    report = validate_all_one_generator_contract(trace_map=trace)
    assert not report.ok
    assert "canonical_stage_order_mismatch" in report.blocking_reasons


def test_missing_generation_rule_blocks():
    rules = tuple(rule for rule in REQUIRED_ALL_ONE_RULES if rule != "secret_shape_scan")
    report = validate_all_one_generator_contract(trace_map=good_trace(), declared_rules=rules)
    assert not report.ok
    assert "required_generation_rule_missing" in report.blocking_reasons


def test_missing_forbidden_capability_blocks():
    forbidden = tuple(item for item in FORBIDDEN_CAPABILITIES if item != "self_authorize")
    report = validate_all_one_generator_contract(trace_map=good_trace(), forbidden_capabilities=forbidden)
    assert not report.ok
    assert "forbidden_capability_missing" in report.blocking_reasons


def test_trace_contract_mismatch_blocks():
    trace = good_trace()
    trace["exact_script_bound"] = False
    report = validate_all_one_generator_contract(trace_map=trace)
    assert not report.ok
    assert "trace_contract_mismatch" in report.blocking_reasons


def test_stage_authority_lock_mismatch_blocks():
    trace = good_trace()
    trace["stages"][0]["grants_authority"] = True
    report = validate_all_one_generator_contract(trace_map=trace)
    assert not report.ok
    assert "stage_authority_lock_mismatch" in report.blocking_reasons


def test_panel_and_contract_dict_render():
    report = validate_all_one_generator_contract(trace_map=good_trace())
    panel = render_all_one_generator_contract_panel(report)
    data = generator_contract_to_dict(report)
    assert "RHPGEN-CONTRACT [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
    assert data["report"]["ok"] is True
    assert len(data["required_canonical_stages"]) == 19
