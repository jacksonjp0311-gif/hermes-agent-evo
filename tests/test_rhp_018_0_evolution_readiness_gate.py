import json

from rhp.evolution_readiness_gate import allowed_classes_for_pointer, evaluate, render_rhpready_box


def _pointer(status="green", active="no_active_wound", integrated=True):
    return {
        "schema": "RHP-LATEST-POINTER-v2.1",
        "latest_operation": "RHP-test",
        "latest_evidence": "docs/context-layer/ops/test-final-evidence.json",
        "observed_ci_status": status,
        "active_wound_class": active,
        "integration_closed": integrated,
        "state": "CI_RECONCILED_GREEN" if integrated else "REMOTE_PENDING",
        "next_operation": "continue",
        "authority_ok": True,
    }


def test_ready_integrated_allows_feature_and_governance():
    state, allowed, next_op, reason = allowed_classes_for_pointer(_pointer())
    assert state == "READY_INTEGRATED"
    assert "feature_evolution" in allowed
    assert "governance_kernel_update" in allowed
    assert next_op == "continue_bounded_evolution_after_named_subject_green"
    assert "green" in reason


def test_pending_allows_observe_and_diagnostic_only():
    state, allowed, next_op, _ = allowed_classes_for_pointer(_pointer(status="pending", active="remote_ci_pending", integrated=False))
    assert state == "REMOTE_NOT_FINAL"
    assert allowed == {"observe", "diagnostic"}
    assert next_op == "wait_or_ingest_final_ci_status_before_green_claim"


def test_red_or_active_wound_blocks_feature_and_allows_repair():
    state, allowed, next_op, _ = allowed_classes_for_pointer(_pointer(status="red", active="evidence_api_break", integrated=False))
    assert state == "WOUND_OPEN"
    assert "feature_evolution" not in allowed
    assert "known_wound_repair" in allowed
    assert next_op == "create_wound_packet_or_repair_known_wound"


def test_dirty_state_only_allows_residue_cleanup():
    state, allowed, next_op, _ = allowed_classes_for_pointer(_pointer(), worktree_clean=False)
    assert state == "DIRTY_BLOCK"
    assert allowed == {"residue_cleanup"}
    assert next_op == "bounded_residue_cleanup_required"


def test_evaluate_reads_fixture_repo_and_renders_rhpready(tmp_path):
    root = tmp_path
    ctx = root / "docs" / "context-layer"
    ctx.mkdir(parents=True)
    (root / ".git").mkdir()
    (ctx / "latest-rhp.json").write_text(json.dumps(_pointer()), encoding="utf-8")

    data = evaluate(root, candidate_operation_class="governance_kernel_update", current_head_ci_status="unknown", allow_dirty=True)
    assert data["allowed"] is True
    assert data["box"] == "RHPREADY"
    assert data["authority_locks"]["self_authorization"] is False
    box = render_rhpready_box(data)
    assert "RHPREADY [ALLOW]" in box
    assert "governance_kernel_update" in box


def test_evaluate_blocks_feature_when_pending(tmp_path):
    root = tmp_path
    ctx = root / "docs" / "context-layer"
    ctx.mkdir(parents=True)
    (root / ".git").mkdir()
    (ctx / "latest-rhp.json").write_text(json.dumps(_pointer(status="pending", active="remote_ci_pending", integrated=False)), encoding="utf-8")

    data = evaluate(root, candidate_operation_class="feature_evolution", current_head_ci_status="unknown", allow_dirty=True)
    assert data["allowed"] is False
    assert data["decision"] == "blocked"
    assert "candidate_operation_class_not_allowed_by_readiness_state" in data["blocked_reasons"]
