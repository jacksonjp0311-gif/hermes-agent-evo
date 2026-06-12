from rhp.runtime_trace_drift_guard import (
    EXPECTED_OPERATION,
    EXPECTED_STAGE_COUNT,
    EXPECTED_STATE,
    EXPECTED_SUBJECT_COMMIT,
    EXPECTED_TRACE_EVIDENCE,
    EXPECTED_TRACE_MODULE,
    report_to_dict,
    render_runtime_trace_drift_guard_panel,
    validate_runtime_trace_drift,
)


def fresh_auth():
    return {
        "provider_call_executed": False,
        "model_call_executed": False,
        "tool_use_executed": False,
        "cms_runtime_execution": False,
        "cms_write": False,
        "memory_write": False,
        "memory_promotion": False,
        "api_write": False,
        "dependency_mutation_committed": False,
        "external_ingestion": False,
        "autonomous_authority": False,
        "self_authorization": False,
    }


def good_inputs():
    latest = {
        "latest_operation": EXPECTED_OPERATION,
        "state": EXPECTED_STATE,
        "active_wound_class": "readiness_gate_install",
        "subject_commit": EXPECTED_SUBJECT_COMMIT,
        "observed_ci_status": "unknown",
        "integration_closed": False,
        "next_operation": "operator_rerun_or_ingest_replacement_ci_before_repair",
        "authority_ok": True,
    }
    final = {
        "operation": EXPECTED_OPERATION,
        "state_after_alignment": EXPECTED_STATE,
        "runtime_script_trace_map_module": EXPECTED_TRACE_MODULE,
        "runtime_script_trace_map_evidence": EXPECTED_TRACE_EVIDENCE,
        "active_wound_preserved": True,
        "active_subject_closed": False,
        "repair_execution_enabled": False,
        "current_operation_remote_ci_status": "unknown_until_next_observation",
        "authority_locks": fresh_auth(),
    }
    order = [f"STAGE-{i}" for i in range(EXPECTED_STAGE_COUNT)]
    trace = {
        "operation": EXPECTED_OPERATION,
        "installed_module": EXPECTED_TRACE_MODULE,
        "stage_count": EXPECTED_STAGE_COUNT,
        "exact_script_bound": True,
        "stage_order": order,
        "stages": [{"stage": name} for name in order],
    }
    module = {
        "operation": EXPECTED_OPERATION,
        "installed_module": EXPECTED_TRACE_MODULE,
        "stage_count": EXPECTED_STAGE_COUNT,
        "exact_script_bound": True,
        "stage_order": order,
    }
    readme = "<!-- RHP_EXACT_RUNTIME_SCRIPT_TRACE_MAP_START --> RHPSCRIPT-TRACE [GOLD] rhp/runtime_script_trace_map.py docs/context-layer/ops/RHP-020-1-exact-runtime-script-trace-map/runtime-script-trace-map.json <!-- RHP_EXACT_RUNTIME_SCRIPT_TRACE_MAP_END -->"
    agents = "<!-- HERMES_AGENT_EXACT_RUNTIME_SCRIPT_TRACE_MAP_START --> exact stage-to-script trace script-trace preservation grants no authority <!-- HERMES_AGENT_EXACT_RUNTIME_SCRIPT_TRACE_MAP_END -->"
    return latest, final, trace, module, readme, agents


def test_good_inputs_pass():
    latest, final, trace, module, readme, agents = good_inputs()
    report = validate_runtime_trace_drift(
        latest_rhp=latest,
        final_evidence=final,
        trace_evidence=trace,
        module_trace=module,
        readme_text=readme,
        agents_text=agents,
    )
    assert report.ok
    assert report.blocking_reasons == ()


def test_latest_mismatch_blocks():
    latest, final, trace, module, readme, agents = good_inputs()
    latest["state"] = "WRONG"
    report = validate_runtime_trace_drift(
        latest_rhp=latest,
        final_evidence=final,
        trace_evidence=trace,
        module_trace=module,
        readme_text=readme,
        agents_text=agents,
    )
    assert not report.ok
    assert "latest_rhp_mismatch" in report.blocking_reasons


def test_trace_stage_count_mismatch_blocks():
    latest, final, trace, module, readme, agents = good_inputs()
    trace["stage_count"] = 18
    report = validate_runtime_trace_drift(
        latest_rhp=latest,
        final_evidence=final,
        trace_evidence=trace,
        module_trace=module,
        readme_text=readme,
        agents_text=agents,
    )
    assert not report.ok
    assert "trace_evidence_mismatch" in report.blocking_reasons
    assert "stage_count_mismatch" in report.blocking_reasons


def test_readme_or_agents_missing_blocks():
    latest, final, trace, module, readme, agents = good_inputs()
    report = validate_runtime_trace_drift(
        latest_rhp=latest,
        final_evidence=final,
        trace_evidence=trace,
        module_trace=module,
        readme_text="missing",
        agents_text=agents,
    )
    assert not report.ok
    assert "readme_trace_block_mismatch" in report.blocking_reasons

    report = validate_runtime_trace_drift(
        latest_rhp=latest,
        final_evidence=final,
        trace_evidence=trace,
        module_trace=module,
        readme_text=readme,
        agents_text="missing",
    )
    assert not report.ok
    assert "agents_trace_rule_mismatch" in report.blocking_reasons


def test_authority_mismatch_blocks():
    latest, final, trace, module, readme, agents = good_inputs()
    final["authority_locks"]["self_authorization"] = True
    report = validate_runtime_trace_drift(
        latest_rhp=latest,
        final_evidence=final,
        trace_evidence=trace,
        module_trace=module,
        readme_text=readme,
        agents_text=agents,
    )
    assert not report.ok
    assert "authority_lock_mismatch" in report.blocking_reasons


def test_panel_and_dict():
    latest, final, trace, module, readme, agents = good_inputs()
    report = validate_runtime_trace_drift(
        latest_rhp=latest,
        final_evidence=final,
        trace_evidence=trace,
        module_trace=module,
        readme_text=readme,
        agents_text=agents,
    )
    data = report_to_dict(report)
    panel = render_runtime_trace_drift_guard_panel(report)
    assert data["ok"] is True
    assert "RHPTRACE-GUARD [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
