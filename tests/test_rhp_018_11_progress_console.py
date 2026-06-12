from rhp.progress_console import (
    global_progress_contract,
    animation_frames,
    PROGRESS_STAGE_PERCENT,
    frame_for,
    progress_bar,
    progress_contract,
    render_progress_frame,
    render_progress_sequence,
    required_progress_stages,
)


def test_progress_bar_has_expected_width_and_percent_bounds():
    assert progress_bar(0) == "[--------------------]"
    assert progress_bar(100) == "[####################]"
    assert progress_bar(150) == "[####################]"


def test_each_required_stage_has_percent_and_spinner():
    stages = required_progress_stages()
    assert "ENTRYPOINT-GATE" in stages
    assert "RHPLOOP-SELF-LEARNING" in stages
    assert "HUMAN-UI-SUMMARY" in stages
    assert PROGRESS_STAGE_PERCENT["ENTRYPOINT-GATE"] == 5
    assert PROGRESS_STAGE_PERCENT["HUMAN-UI-SUMMARY"] == 100
    frame = frame_for("RHPLOOP-SELF-LEARNING", detail="lesson checkpoint", tick=1)
    assert frame.percent == 60
    assert frame.spinner in {"|", "/", "-", "\\"}


def test_render_progress_frame_includes_percent_spinner_bar_and_stage():
    frame = frame_for("RHPREADY", status="diagnostic", detail="readiness evidence", tick=0, tone="gold")
    text = render_progress_frame(frame, operation="RHP-018.11")
    assert "RHPLOAD [035%]" in text
    assert "spin=" in text
    assert "loop=RHPREADY" in text
    assert "[#######-------------]" in text


def test_render_progress_sequence_contains_self_learning_before_summary():
    text = render_progress_sequence("RHP-018.11")
    assert "loop=RHPLOOP-SELF-LEARNING" in text
    assert "loop=HUMAN-UI-SUMMARY" in text
    assert text.index("loop=RHPLOOP-SELF-LEARNING") < text.index("loop=HUMAN-UI-SUMMARY")


def test_progress_contract_requires_all_visibility_surfaces():
    contract = progress_contract()
    assert contract["requires_percent"] is True
    assert contract["requires_spinner"] is True
    assert contract["requires_load_bar"] is True
    assert contract["requires_stage_label"] is True


def test_animation_frames_move_from_start_to_end():
    frames = animation_frames(
        20,
        25,
        stage="RHPLOOP-RUNTIME",
        status="preauth",
        detail="moving progress",
        operation="RHP-018.11",
    )
    assert len(frames) >= 2
    assert "RHPLOAD [020%]" in frames[0]
    assert "RHPLOAD [025%]" in frames[-1]
    assert "spin=" in frames[0]
    assert "spin=" in frames[-1]
    assert frames[0] != frames[-1]


def test_progress_contract_requires_motion():
    contract = progress_contract()
    assert contract["requires_motion"] is True
    assert contract["requires_animated_transition"] is True


def test_global_progress_contract_prefers_single_top_surface():
    contract = global_progress_contract()
    assert contract["preferred_runtime_surface"] == "PowerShell Write-Progress"
    assert contract["requires_concise_settled_sections"] is True
    assert "do not spam" in contract["console_rule"]
