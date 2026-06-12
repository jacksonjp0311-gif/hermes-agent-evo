from __future__ import annotations

EVOLVED_RUNTIME_GEOMETRY = (
    "PREAUTH-FETCH",
    "RHPLOOP-RUNTIME",
    "HUMAN-AUTHORIZATION",
    "RHPREADY",
    "PREAUTH-LINEAGE-ALIGNMENT",
    "OPERATION-START",
)

SUPERSEDED_STAGES = {
    "PREAUTH-PULL": "PREAUTH-FETCH",
}

def evolved_geometry() -> dict:
    return {
        "schema": "RHP-RUNTIME-GEOMETRY-EVOLUTION-CANON-v0.1",
        "evolved_runtime_geometry": list(EVOLVED_RUNTIME_GEOMETRY),
        "superseded_stages": dict(SUPERSEDED_STAGES),
        "authorization_mode": "inline_authorize_parameter",
        "post_authorization_questions": "forbidden",
        "fallback_states": ["unknown", "pending"],
    }