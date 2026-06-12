from __future__ import annotations

REPAIRED_WOUND_CLASSES = (
    "zero_context_next_operation_contract_drift",
    "loop_geometry_legacy_api_drift",
    "zero_context_bom_json_loader_drift",
    "evidence_api_bom_pointer_loader_drift",
)

def repaired_wounds() -> tuple[str, ...]:
    return REPAIRED_WOUND_CLASSES