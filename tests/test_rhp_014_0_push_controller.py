
from rhp.push_controller import RHP_PUSH_CONTROLLER_SCHEMA, PushBox, render_stage, stage

def test_rhp_014_0_push_stage_ok_renders_green_box():
    item = stage("push", "ok", "remote main updated")
    text = render_stage("RHP-014.0", item, 98)
    assert "GITHUB PUSH" in text
    assert "[OK]" in text
    assert "verified: true" in text

def test_rhp_014_0_push_box_schema():
    item = stage("commit", "ok", "commit object created")
    box = PushBox(RHP_PUSH_CONTROLLER_SCHEMA, True, "RHP-014.0", [item])
    assert box.as_dict()["schema"] == RHP_PUSH_CONTROLLER_SCHEMA
