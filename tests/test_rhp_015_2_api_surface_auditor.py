from rhp.api_surface_auditor import audit_contract
from rhp.contract_registry import STABLE_SYMBOLS, STABLE_EVIDENCE_KEYS, registry


def test_rhp_015_2_contract_registry_lists_stable_surfaces():
    data = registry()
    assert data["schema"] == "RHP-CONTRACT-REGISTRY-v0.1"
    assert "rhp.autoheal_executor_dry_run" in STABLE_SYMBOLS
    assert "RHP_AUTOHEAL_DRY_RUN_SCHEMA" in STABLE_SYMBOLS["rhp.autoheal_executor_dry_run"]
    assert "latest_rhp0135_passed" in STABLE_EVIDENCE_KEYS["alignment_guard.checks"]


def test_rhp_015_2_api_surface_audit_is_green_for_registry():
    result = audit_contract(".", include_discovered=False)
    assert result["ok"] is True
    assert result["missing"] == []
    assert result["summary"]["registry_symbols"] >= 1
