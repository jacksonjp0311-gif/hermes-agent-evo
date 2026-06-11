from rhp.human_ui_summary import render_summary

def test_rhp_014_3_human_ui_summary_renders_dashboard():
    text = render_summary(
        {"operation": "RHP-014.3", "next_recommended_operation": "RHP-014.4", "schema": "x", "self_authorization": False, "autonomous_authority": False},
        {"classification": "assertion_failure", "confidence": 0.8},
        {"would_mutate": False, "would_commit": False},
    )
    assert "operator dashboard" in text
    assert "wound: assertion_failure" in text
    assert "would_mutate=False" in text
