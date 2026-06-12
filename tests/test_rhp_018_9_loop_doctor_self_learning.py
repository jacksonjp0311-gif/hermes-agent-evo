from rhp.loop_doctor import (
    render_doctor_panel,
    render_self_learning_panel,
    summarize_doctor_payload,
    validate_self_learning_candidate,
)


def test_doctor_panel_renders_blocked_reasons_and_authority_lock():
    payload = {
        "doctor": {
            "latest_operation": "RHP-018.8",
            "state": "OBSERVED",
            "next_legal_operation": "operator_rerun_or_ingest_replacement_ci_before_repair",
            "can_mutate": False,
            "blocked_reasons": ["remote_ci_not_final", "human_all_one_authorization_required_for_mutation"],
            "evidence_api_ok": True,
            "replay_ok": True,
            "worktree_clean": True,
        }
    }
    summary = summarize_doctor_payload(payload)
    assert summary.can_mutate is False
    text = render_doctor_panel(payload)
    assert "RHPLOOP-DOCTOR [GOLD]" in text
    assert "remote_ci_not_final" in text
    assert "authority: no grant [LOCKED]" in text


def test_self_learning_candidate_requires_evidence_and_behavior_change():
    candidate = {
        "observed_event": "compressed loop hid debug power",
        "evidence_path": "docs/context-layer/ops/RHP-018-8-final-evidence.json",
        "lesson": "visible panels are debugging primitives",
        "future_behavior_change": "future scripts must render RHPREFLECT",
        "authority_boundary": "no authority grant",
    }
    result = validate_self_learning_candidate(candidate)
    assert result["ok"] is True
    assert result["classification"] == "promotable_lesson_candidate"
    text = render_self_learning_panel(candidate)
    assert "RHPLOOP-SELF-LEARNING [GOLD]" in text
    assert "visible panels are debugging primitives" in text


def test_self_learning_candidate_blocks_authority_grants():
    candidate = {
        "observed_event": "bad idea",
        "evidence_path": "docs/context-layer/ops/example.json",
        "lesson": "grant autonomy",
        "future_behavior_change": "agent mutates directly",
        "authority_boundary": "autonomous_authority=true",
    }
    result = validate_self_learning_candidate(candidate)
    assert result["ok"] is False
    assert result["grants_authority"] is True
