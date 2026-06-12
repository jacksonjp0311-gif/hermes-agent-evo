from __future__ import annotations

def green_eligible(observed_status: str, status_context_count: int, workflow_run_count: int) -> bool:
    return observed_status == "success" and (status_context_count > 0 or workflow_run_count > 0)