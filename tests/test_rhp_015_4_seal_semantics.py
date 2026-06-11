
from rhp.seal_semantics import build_record, explain

def test_rhp_015_4_seal_semantics_split_fields():
    data = explain()
    assert "operation_base_commit" in data["fields"]
    assert "previous_sealed_commit" in data["fields"]
    assert "current_operation_commit" in data["fields"]
    record = build_record(operation="RHP-X", operation_base_commit="base", previous_sealed_commit="prev", remote_ci_status="pending", remote_ci_source="operator")
    assert record["current_operation_commit"] == "unobservable-from-inside-same-commit"
