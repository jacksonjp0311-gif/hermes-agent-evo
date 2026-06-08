from pathlib import Path

import hrcn_runtime_bridge as hrcn


def test_hrcn_bridge_anchors_to_ops_027_after_v0_3_seal():
    root = Path(__file__).resolve().parent.parent
    context = hrcn.load_hrcn_context(root)
    assert context["latest_evidence_path"] == "docs/context-layer/ops/OPS-027-final-evidence.json"
    assert context["evidence"]["v0_3_seal_passed"] is True
    assert context["evidence"]["tag_name"] == "hrcn-ops-v0.3.0"


def test_hrcn_bridge_status_reports_v0_3_state():
    root = Path(__file__).resolve().parent.parent
    status = hrcn.get_bridge_status(root)
    assert status.mode == "read_only"
    assert status.sealed_anchor_tag == "hrcn-ops-v0.3.0"
    assert status.current_state == "HRCN OPS v0.3.0 read-only runtime/proposal bridge sealed"
    assert status.latest_evidence_path == "docs/context-layer/ops/OPS-027-final-evidence.json"
    assert all(value is False for value in status.authority.values())


def test_hrcn_bridge_prompt_mentions_ops_027_anchor():
    root = Path(__file__).resolve().parent.parent
    text = hrcn.format_context_for_prompt(root)
    assert "HRCN Runtime Bridge: READ ONLY" in text
    assert "hrcn-ops-v0.3.0" in text
    assert "OPS-027-final-evidence.json" in text
    assert "read-only runtime/proposal bridge sealed" in text
