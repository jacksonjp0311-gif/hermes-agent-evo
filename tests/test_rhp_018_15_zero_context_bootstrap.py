from pathlib import Path
import json

from rhp.zero_context_bootstrap import (
    REQUIRED_AUTHORITY_FALSE_KEYS,
    ZERO_CONTEXT_SOURCE_ORDER,
    authority_false_map,
    authority_ok,
    render_zero_context_panel,
    report_to_dict,
    validate_zero_context_bootstrap,
)


def _latest_next_operation():
    return json.loads(Path("docs/context-layer/latest-rhp.json").read_text(encoding="utf-8-sig"))["next_operation"]

def _authority_locks():
    return {key: False for key in REQUIRED_AUTHORITY_FALSE_KEYS}


def test_source_order_starts_with_readme_and_loads_latest_evidence():
    assert ZERO_CONTEXT_SOURCE_ORDER[0] == "README.md"
    assert ZERO_CONTEXT_SOURCE_ORDER[1] == "AGENTS.md"
    assert "docs/context-layer/latest-rhp.json" in ZERO_CONTEXT_SOURCE_ORDER
    assert "<latest_evidence_from_latest_rhp>" in ZERO_CONTEXT_SOURCE_ORDER


def test_authority_ok_requires_all_locks_false():
    locks = {"authority_locks": _authority_locks()}
    assert authority_ok(locks)
    bad = {"authority_locks": {**_authority_locks(), "self_authorization": True}}
    assert not authority_ok(bad)


def test_authority_false_map_supports_legacy_top_level_keys():
    data = _authority_locks()
    assert all(authority_false_map(data).values())


def test_latest_pointer_authority_ok_is_valid_pointer_surface():
    data = {"schema": "RHP-LATEST-POINTER-v2.1", "authority_ok": True}
    assert all(authority_false_map(data).values())




def test_validate_current_repository_zero_context_bootstrap():
    report = validate_zero_context_bootstrap(Path("."))
    assert report.readme_loaded
    assert report.agents_loaded
    assert report.latest_rhp_loaded
    assert report.latest_evidence_loaded
    assert report.zero_context_rebuild_loaded
    assert report.operator_context_loaded
    assert report.loop_geometry_loaded
    assert report.geometry_ok
    assert report.authority_ok
    assert report.next_operation == _latest_next_operation()


def test_render_zero_context_panel_contains_locks_and_next():
    report = validate_zero_context_bootstrap(Path("."))
    panel = render_zero_context_panel(report)
    assert "RHPZERO [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
    assert f"next: {_latest_next_operation()}" in panel


def test_report_to_dict_is_json_serializable():
    report = validate_zero_context_bootstrap(Path("."))
    json.dumps(report_to_dict(report))
