from rhp.runtime_script_trace_map import (
    CANONICAL_RUNTIME_STAGE_ORDER,
    RUNTIME_SCRIPT_TRACE_MAP,
    get_stage,
    render_runtime_script_trace_panel,
    script_trace_map_to_dict,
    stage_names,
    validate_exact_script_bindings,
    validate_stage_order,
)


def test_all_19_canonical_stages_are_present():
    assert len(CANONICAL_RUNTIME_STAGE_ORDER) == 19
    assert len(RUNTIME_SCRIPT_TRACE_MAP) == 19
    assert stage_names() == CANONICAL_RUNTIME_STAGE_ORDER
    assert validate_stage_order(stage_names())


def test_each_stage_has_required_exact_trace_fields():
    for stage in RUNTIME_SCRIPT_TRACE_MAP:
        assert stage["executing_script"]
        assert "python_script" in stage
        assert "repo_modules" in stage
        assert stage["launch_location"] or stage["working_directory_before"] or stage["working_directory_after"]
        assert stage["purpose"]
        assert "writes_repo" in stage
        assert "next_stage" in stage


def test_required_stage_specific_bindings():
    assert get_stage("ENTRYPOINT-GATE")["executing_script"] == "$env:USERPROFILE\\Downloads\\RHP_020_1_V3_EXACT_RUNTIME_SCRIPT_TRACE_MAP_SINGLE_ALL_ONE.ps1"
    assert get_stage("ROOT-ANCHOR")["working_directory_after"] == "C:/Users/jacks/OneDrive/Desktop/hermes-agent-evo"
    assert "git rev-parse --show-toplevel" in get_stage("ROOT-ANCHOR")["commands"]
    assert "rhp/evolution_readiness_gate.py" in get_stage("RHPREADY")["repo_modules"]
    assert get_stage("OPERATION-START")["python_script"] == "$env:TEMP\\RHP-020-1-python-streams\\rhp_020_1_exact_runtime_script_trace_map.py"
    assert "rhp/runtime_script_trace_map.py" in get_stage("OPERATION-START")["repo_modules"]
    assert "rhp/rhpload_doctor.py" in get_stage("RHPLOOP-DOCTOR")["repo_modules"]
    assert "rhp/doctor_cli.py" in get_stage("RHPLOOP-DOCTOR")["repo_modules"]
    assert "rhp/loop_doctor.py" in get_stage("RHPLOOP-DOCTOR")["repo_modules"]
    assert "rhp/runtime_script_trace_map.py" in get_stage("RHPLOOP-SELF-LEARNING")["repo_modules"]
    assert any("py_compile" in c for c in get_stage("VALIDATION")["commands"])
    assert any("pytest -o addopts=" in c for c in get_stage("VALIDATION")["commands"])
    assert any("evidence_api_compatibility_gate" in c for c in get_stage("VALIDATION")["commands"])
    assert "git diff --cached -U0" in get_stage("SECRET-SCAN")["commands"]
    assert any(c.startswith("git add ") for c in get_stage("COMMIT-SEAL")["commands"])
    assert any(c.startswith("git commit ") for c in get_stage("COMMIT-SEAL")["commands"])
    assert "git pull --rebase origin main" in get_stage("PUSH-SEAL")["commands"]
    assert "git push origin main" in get_stage("PUSH-SEAL")["commands"]
    assert "rhp/runtime_loop.py" in get_stage("RHPDROP")["repo_modules"]
    assert "docs/context-layer/ops/RHP-020-1-final-evidence.json" in get_stage("RHPREFLECT")["repo_evidence"]
    assert "git status --short" in get_stage("POST-SEAL-RESIDUE")["commands"]
    assert get_stage("RETURN-ROOT")["working_directory_after"] == "C:/Users/jacks/OneDrive/Desktop/hermes-agent-evo"
    assert get_stage("HUMAN-UI-SUMMARY")["writes_repo"] is False


def test_no_stage_grants_authority_closes_wound_repairs_or_claims_green():
    assert validate_exact_script_bindings()
    for stage in RUNTIME_SCRIPT_TRACE_MAP:
        assert stage["grants_authority"] is False
        assert stage["closes_wound"] is False
        assert stage["repairs_code"] is False
        assert stage["claims_current_operation_ci_green"] is False


def test_panel_and_dict():
    data = script_trace_map_to_dict()
    panel = render_runtime_script_trace_panel()
    assert data["stage_count"] == 19
    assert data["exact_script_bound"] is True
    assert "RHPSCRIPT-TRACE [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
