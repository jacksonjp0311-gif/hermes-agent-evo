from rhp.evidence_graph_index import (
    EXPECTED_ACTIVE_WOUND,
    EXPECTED_LATEST_OPERATION,
    EXPECTED_LATEST_STATE,
    EXPECTED_NEXT_OPERATION,
    EXPECTED_SUBJECT_COMMIT,
    FINAL_EVIDENCE_BY_OPERATION,
    KNOWN_OPERATION_ORDER,
    build_evidence_graph,
    render_evidence_graph_panel,
    report_to_dict,
    validate_evidence_graph,
)


AUTH = {
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


def latest():
    return {
        "latest_operation": EXPECTED_LATEST_OPERATION,
        "state": EXPECTED_LATEST_STATE,
        "subject_commit": EXPECTED_SUBJECT_COMMIT,
        "active_wound_class": EXPECTED_ACTIVE_WOUND,
        "next_operation": EXPECTED_NEXT_OPERATION,
    }


def final_evidence():
    data = {}
    prior = "START"
    for op in KNOWN_OPERATION_ORDER:
        data[op] = {
            "operation": op,
            "subject_commit": EXPECTED_SUBJECT_COMMIT,
            "wound_class": EXPECTED_ACTIVE_WOUND,
            "prior_blocking_state": prior,
            "state_after_alignment": f"{op}_STATE",
            "next_recommended_operation": EXPECTED_NEXT_OPERATION,
            "active_wound_preserved": True,
            "active_subject_closed": False,
            "repair_execution_enabled": False,
            "authority_locks": dict(AUTH),
            "example_module": "rhp/example.py",
            "example_tests": "tests/test_example.py",
        }
        prior = data[op]["state_after_alignment"]
    data[EXPECTED_LATEST_OPERATION]["state_after_alignment"] = EXPECTED_LATEST_STATE
    return data


def test_build_graph_contains_known_operations_and_edges():
    graph = build_evidence_graph(latest_rhp=latest(), final_evidence_by_operation=final_evidence())
    assert graph["schema"] == "RHP-EVIDENCE-GRAPH-INDEX-v0.1"
    assert [node["id"] for node in graph["nodes"]] == list(KNOWN_OPERATION_ORDER)
    assert len(graph["edges"]) >= len(KNOWN_OPERATION_ORDER) * 2


def test_good_graph_validates():
    graph = build_evidence_graph(latest_rhp=latest(), final_evidence_by_operation=final_evidence())
    report = validate_evidence_graph(graph, latest())
    assert report.ok
    assert report.blocking_reasons == ()


def test_latest_mismatch_blocks():
    l = latest()
    graph = build_evidence_graph(latest_rhp=l, final_evidence_by_operation=final_evidence())
    l["state"] = "WRONG"
    report = validate_evidence_graph(graph, l)
    assert not report.ok
    assert "latest_pointer_mismatch" in report.blocking_reasons


def test_subject_mismatch_blocks():
    ev = final_evidence()
    ev["RHP-020.2"]["subject_commit"] = "wrong"
    graph = build_evidence_graph(latest_rhp=latest(), final_evidence_by_operation=ev)
    report = validate_evidence_graph(graph, latest())
    assert not report.ok
    assert "subject_commit_mismatch" in report.blocking_reasons


def test_authority_mismatch_blocks():
    ev = final_evidence()
    ev["RHP-020.4"]["authority_locks"]["self_authorization"] = True
    graph = build_evidence_graph(latest_rhp=latest(), final_evidence_by_operation=ev)
    report = validate_evidence_graph(graph, latest())
    assert not report.ok
    assert "authority_lock_mismatch" in report.blocking_reasons


def test_panel_and_report_dict_render():
    graph = build_evidence_graph(latest_rhp=latest(), final_evidence_by_operation=final_evidence())
    report = validate_evidence_graph(graph, latest())
    panel = render_evidence_graph_panel(report)
    data = report_to_dict(report)
    assert "RHPEVIDENCE-GRAPH [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
    assert data["ok"] is True
    assert data["node_count"] == 5
