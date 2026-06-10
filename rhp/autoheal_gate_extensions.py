
# RHP-014.0 autoheal plan extensions.
from __future__ import annotations
from rhp.autoheal_plan import plan_for_classification

KNOWN_RHP_014_PLAN_CLASSES = [
    "dirty_worktree_and_module_path_execution_bug",
    "module_path_execution_bug",
    "tooling_escape_bug",
    "current_script_identity_mismatch",
    "push_gate_sequence_mismatch",
]

def classify_gate_failure(text: str) -> str:
    lower = (text or "").lower()
    if "actual_script_mismatch" in lower or "evidence_script_mismatch" in lower or "current script" in lower:
        return "current_script_identity_mismatch"
    if "push" in lower and ("sequence" in lower or "gate" in lower or "miss" in lower):
        return "push_gate_sequence_mismatch"
    if "modulenotfounderror" in lower:
        return "module_path_execution_bug"
    if "dirty" in lower and "worktree" in lower:
        return "dirty_worktree_and_module_path_execution_bug"
    return "unknown"

def build_known_plan(classification: str, operation: str = "RHP"):
    return plan_for_classification(classification, operation)
