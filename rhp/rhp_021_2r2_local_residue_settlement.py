from __future__ import annotations

def settlement_ok(latest_operation: str, state: str, dirty_count: int) -> bool:
    return latest_operation == "RHP-021.2R" and state == "RHP_021_2_POST_SEAL_RESIDUE_CLASSIFIED" and dirty_count == 0