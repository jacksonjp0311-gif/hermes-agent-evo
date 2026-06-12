from __future__ import annotations

NO_PROMPT_OPERATOR_RULES = (
    "after_authorization_no_runtime_questions",
    "observe_or_default_to_named_state",
    "unknown_is_named_state_not_failure",
    "pending_is_named_state_not_failure",
    "operator_prompts_allowed_only_for_authorization",
)

def no_prompt_contract() -> dict:
    return {
        "schema": "RHP-NO-PROMPT-OPERATOR-CONTRACT-v0.1",
        "rules": list(NO_PROMPT_OPERATOR_RULES),
        "allowed_operator_input_after_start": [],
        "authorization_mode": "inline_authorize_parameter",
        "fallback": "seal_unknown_or_pending_as_named_evidence",
    }

def is_operator_prompt_allowed(prompt_class: str) -> bool:
    return prompt_class == "authorization"