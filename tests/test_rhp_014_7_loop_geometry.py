from rhp.loop_geometry import geometry


def test_loop_geometry_axes_and_boundary():
    data = geometry()
    assert data["schema"] == "RHP-LOOP-GEOMETRY-v0.1"
    assert "evidence" in data["axes"]
    assert data["boundary"] == "human authorization"
    assert "bounded tools" in data["adaptation_rule"]
