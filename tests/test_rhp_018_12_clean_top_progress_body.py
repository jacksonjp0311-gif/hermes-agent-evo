from rhp.progress_console import (
    PROGRESS_STAGE_PERCENT,
    animation_frames,
    frame_for,
    global_progress_contract,
    progress_bar,
    progress_contract,
    render_progress_frame,
    render_progress_sequence,
    render_settled_stage,
    required_progress_stages,
)


def test_progress_bar_kept_only_for_compatibility():
    assert progress_bar(0) == "[--------------------]"
    assert progress_bar(100) == "[####################]"


def test_each_required_stage_has_percent():
    stages = required_progress_stages()
    assert "ENTRYPOINT-GATE" in stages
    assert "RHPLOOP-SELF-LEARNING" in stages
    assert "HUMAN-UI-SUMMARY" in stages
    assert PROGRESS_STAGE_PERCENT["ENTRYPOINT-GATE"] == 5
    assert PROGRESS_STAGE_PERCENT["HUMAN-UI-SUMMARY"] == 100


def test_legacy_progress_frame_still_exists_for_evidence_compatibility():
    frame = frame_for("RHPREADY", status="diagnostic", detail="readiness evidence", tick=0, tone="gold")
    text = render_progress_frame(frame, operation="RHP-018.12")
    assert "RHPLOAD [035%]" in text
    assert "spin=" in text
    assert "loop=RHPREADY" in text


def test_settled_stage_has_no_inline_bar_or_spinner():
    text = render_settled_stage(
        "RHPLOOP-SELF-LEARNING",
        operation="RHP-018.12",
        status="runtime-checkpoint",
        detail="lesson checkpoint before final summary",
        tone="gold",
    )
    assert "RHPLOAD [060%]" in text
    assert "loop=RHPLOOP-SELF-LEARNING" in text
    assert "spin=" not in text
    assert "[#" not in text
    assert "lesson checkpoint before final summary" in text


def test_render_progress_sequence_contains_self_learning_before_summary_without_bars():
    text = render_progress_sequence("RHP-018.12")
    assert "loop=RHPLOOP-SELF-LEARNING" in text
    assert "loop=HUMAN-UI-SUMMARY" in text
    assert text.index("loop=RHPLOOP-SELF-LEARNING") < text.index("loop=HUMAN-UI-SUMMARY")
    assert "[#" not in text
    assert "spin=" not in text


def test_animation_frames_remain_non_runtime_compatibility_surface():
    frames = animation_frames(20, 25, stage="RHPLOOP-RUNTIME", status="preauth", detail="moving progress", operation="RHP-018.12")
    assert len(frames) >= 2
    assert "spin=" in frames[0]


def test_progress_contract_bans_body_bars_and_body_spinners():
    contract = progress_contract()
    assert contract["requires_global_top_progress"] is True
    assert contract["requires_concise_settled_sections"] is True
    assert contract["body_inline_bars_allowed"] is False
    assert contract["body_spinner_allowed"] is False
    assert contract["body_frame_spam_allowed"] is False


def test_global_progress_contract_prefers_single_top_surface():
    contract = global_progress_contract()
    assert contract["preferred_runtime_surface"] == "PowerShell Write-Progress"
    assert contract["requires_concise_settled_sections"] is True
    assert contract["body_inline_bars_allowed"] is False
    assert "no inline body bars" in contract["console_rule"]
