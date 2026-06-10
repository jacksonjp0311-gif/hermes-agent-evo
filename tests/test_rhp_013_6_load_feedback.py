from rhp.load_feedback import RHPLOAD_FEEDBACK_SCHEMA, build_standard_tree, render_feedback_tree

def test_rhp_013_6_feedback_tree_renders_expandable_process():
    tree = build_standard_tree("CI-REPAIR", "RHP-013.6", 35)
    text = render_feedback_tree(tree)
    assert tree.schema == RHPLOAD_FEEDBACK_SCHEMA
    assert "RHPLOAD [035%]" in text
    assert "loop=CI-REPAIR" in text
    assert "Inspect target surfaces" in text
    assert "Validate" in text
    assert "feedback:" in text

def test_rhp_013_6_feedback_tree_json_has_children():
    tree = build_standard_tree("REHYDRATION", "RHP-013.6", 10)
    data = tree.as_dict()
    assert data["root"]["children"]
    assert data["root"]["children"][0]["label"] == "Rehydrate"
