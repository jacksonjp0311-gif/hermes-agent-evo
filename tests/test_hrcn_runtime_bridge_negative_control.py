import json
from pathlib import Path

import pytest

import hrcn_runtime_bridge as bridge


def _write_fake_repo(tmp_path: Path, evidence: dict) -> Path:
    root = tmp_path / "fake-hermes"
    (root / ".git").mkdir(parents=True)
    (root / "pyproject.toml").write_text("[project]\nname = 'fake-hermes'\n", encoding="utf-8")
    evidence_dir = root / "docs" / "context-layer" / "ops"
    evidence_dir.mkdir(parents=True)
    (evidence_dir / "OPS-020-final-evidence.json").write_text(
        json.dumps(evidence, indent=2) + "\n",
        encoding="utf-8",
    )
    return root


def _valid_evidence() -> dict:
    evidence = {key: False for key in bridge.FORBIDDEN_AUTHORITIES}
    evidence.update({
        "bounded_loop_v0_2_seal_passed": True,
        "new_tag": "hrcn-ops-v0.2.0",
        "next_recommended_operation": "OPS-024 negative-control bridge authority refusal",
    })
    return evidence


def test_negative_control_rejects_cms_write_authority(tmp_path):
    evidence = _valid_evidence()
    evidence["cms_write"] = True
    fake_root = _write_fake_repo(tmp_path, evidence)

    with pytest.raises(RuntimeError, match="cms_write"):
        bridge.get_bridge_status(fake_root)


def test_negative_control_rejects_memory_write_authority(tmp_path):
    evidence = _valid_evidence()
    evidence["memory_write"] = True
    fake_root = _write_fake_repo(tmp_path, evidence)

    with pytest.raises(RuntimeError, match="memory_write"):
        bridge.make_gui_context_packet(fake_root)


def test_negative_control_rejects_api_write_authority(tmp_path):
    evidence = _valid_evidence()
    evidence["api_write"] = True
    fake_root = _write_fake_repo(tmp_path, evidence)

    with pytest.raises(RuntimeError, match="api_write"):
        bridge.format_context_for_prompt(fake_root)


def test_negative_control_rejects_self_authorization(tmp_path):
    evidence = _valid_evidence()
    evidence["self_authorization"] = True
    fake_root = _write_fake_repo(tmp_path, evidence)

    with pytest.raises(RuntimeError, match="self_authorization"):
        bridge.assert_read_only_boundary(fake_root)


def test_negative_control_rejects_autonomous_authority(tmp_path):
    evidence = _valid_evidence()
    evidence["autonomous_authority"] = True
    fake_root = _write_fake_repo(tmp_path, evidence)

    with pytest.raises(RuntimeError, match="autonomous_authority"):
        bridge.assert_read_only_boundary(fake_root)


def test_negative_control_rejects_unsealed_evidence(tmp_path):
    evidence = _valid_evidence()
    evidence["bounded_loop_v0_2_seal_passed"] = False
    fake_root = _write_fake_repo(tmp_path, evidence)

    with pytest.raises(RuntimeError, match="not marked passed"):
        bridge.get_bridge_status(fake_root)


def test_negative_control_accepts_only_fully_read_only_evidence(tmp_path):
    fake_root = _write_fake_repo(tmp_path, _valid_evidence())
    status = bridge.get_bridge_status(fake_root)

    assert status.mode == "read_only"
    assert status.sealed_anchor_tag == "hrcn-ops-v0.2.0"
    assert all(value is False for value in status.authority.values())
