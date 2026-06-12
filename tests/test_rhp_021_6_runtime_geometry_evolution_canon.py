from rhp.loop_geometry import FULL_RUNTIME_GEOMETRY, LINEAGE_RUNTIME_GEOMETRY_ALIASES, canonicalize_runtime_stage
from rhp.runtime_geometry_evolution_canon import evolved_geometry


def test_preauth_fetch_replaces_preauth_pull():
    assert "PREAUTH-FETCH" in FULL_RUNTIME_GEOMETRY
    assert "PREAUTH-PULL" not in FULL_RUNTIME_GEOMETRY
    assert LINEAGE_RUNTIME_GEOMETRY_ALIASES["PREAUTH-PULL"] == "PREAUTH-FETCH"
    assert canonicalize_runtime_stage("PREAUTH-PULL") == "PREAUTH-FETCH"


def test_lineage_alignment_is_explicit_after_authorization():
    auth_i = FULL_RUNTIME_GEOMETRY.index("HUMAN-AUTHORIZATION")
    ready_i = FULL_RUNTIME_GEOMETRY.index("RHPREADY")
    lineage_i = FULL_RUNTIME_GEOMETRY.index("PREAUTH-LINEAGE-ALIGNMENT")
    op_i = FULL_RUNTIME_GEOMETRY.index("OPERATION-START")
    assert auth_i < ready_i < lineage_i < op_i


def test_evolved_geometry_contract_names_no_prompt_fallback():
    data = evolved_geometry()
    assert data["authorization_mode"] == "inline_authorize_parameter"
    assert data["post_authorization_questions"] == "forbidden"
    assert "unknown" in data["fallback_states"]
    assert "pending" in data["fallback_states"]