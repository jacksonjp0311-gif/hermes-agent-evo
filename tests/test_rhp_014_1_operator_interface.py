from rhp.operator_interface import BoxLine, RHP_OPERATOR_INTERFACE_SCHEMA, render_box

def test_rhp_014_1_operator_box_renders_ok():
    box = BoxLine(89, "WARNING-COMPRESSOR", "RHP-014.1", "warning compressor box", "ok", "compressed", True)
    data = box.as_dict()
    text = render_box(box)
    assert data["schema"] == RHP_OPERATOR_INTERFACE_SCHEMA
    assert data["glyph"] == "[OK]"
    assert "verified: true [OK]" in text
