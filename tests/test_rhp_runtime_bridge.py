from pathlib import Path

import rhp_runtime_bridge as bridge


def test_rhp_bridge_loads_manifest_report_and_certificate():
    root = Path(__file__).resolve().parent.parent
    context = bridge.load_rhp_context(root)
    assert context["manifest"]["schema"] == "RHP-HERMES-origin-manifest-v0.1"
    assert context["report"]["schema"] == "RHP-HERMES-alignment-report-v0.1"
    assert context["certificate"]["schema"] == "RHP-HERMES-origin-certificate-v0.1"


def test_rhp_bridge_is_read_only_and_grants_no_authority():
    root = Path(__file__).resolve().parent.parent
    assert bridge.assert_read_only_boundary(root) is True
    status = bridge.get_bridge_status(root)
    assert status.mode == "read_only_proposal"
    assert status.compounding_permitted is False
    assert all(value is False for value in status.authority.values())


def test_rhp_prompt_context_contains_non_claim_lock():
    root = Path(__file__).resolve().parent.parent
    text = bridge.format_context_for_prompt(root)
    assert "RHP Runtime Bridge: READ ONLY PROPOSAL ORIENTATION" in text
    assert "Compounding Permitted: False" in text
    assert "RHP before HRCN" in text
    assert "self-authorization" in text
