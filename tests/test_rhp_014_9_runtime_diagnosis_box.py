from rhp.runtime_diagnosis_box import classify, diagnosis, render_box

def test_runtime_diagnosis_classifies_powershell_invocation_collision():
    assert classify("The expression after '&' in a pipeline element produced an object") == "powershell_command_invocation_collision"

def test_runtime_diagnosis_renders_expandable_box():
    data = diagnosis("pull-rebase-preauth", "remote_ci_red", "raw.txt")
    text = render_box(data)
    assert "RHPDIAG" in text
    assert "expand" in text
