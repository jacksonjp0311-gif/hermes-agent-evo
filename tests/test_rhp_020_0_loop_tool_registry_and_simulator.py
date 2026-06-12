from rhp.loop_tool_registry import (
    forbidden_tools,
    get_tool,
    registry_to_dict,
    render_tool_registry_panel,
    tool_names,
)
from rhp.loop_simulator import simulate_loop_transition, render_simulation_panel


LATEST_BLOCKED = {
    "state": "REPLACEMENT_CI_CONNECTOR_INTAKE_UNRESOLVED",
    "active_wound_class": "readiness_gate_install",
    "next_operation": "operator_rerun_or_ingest_replacement_ci_before_repair",
}


def test_registry_contains_core_tools():
    names = tool_names()
    assert "RHPZERO" in names
    assert "RHPLOOP-GEOMETRY" in names
    assert "RHPCI-CONNECTOR" in names
    assert "RHPSIM" in names
    assert "RHPHEAL" in names


def test_registry_tools_do_not_grant_authority():
    assert forbidden_tools() == ()
    for item in registry_to_dict()["tools"]:
        assert item["grants_authority"] is False
        assert item["repairs_code"] is False
        assert item["closes_wound"] is False


def test_get_tool_normalizes_case():
    assert get_tool("rhpsim").name == "RHPSIM"


def test_tool_registry_panel_renders():
    panel = render_tool_registry_panel()
    assert "RHPTOOL [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel


def test_simulator_allows_loop_tooling_evidence_write_without_repair():
    sim = simulate_loop_transition(
        LATEST_BLOCKED,
        candidate_operation="loop_tooling",
        requested_tool="RHPDROP",
    )
    assert sim.ok
    assert sim.can_mutate
    assert not sim.can_close_wound
    assert not sim.can_repair


def test_simulator_blocks_unapproved_candidate_under_active_wound():
    sim = simulate_loop_transition(
        LATEST_BLOCKED,
        candidate_operation="feature_evolution",
        requested_tool="RHPZERO",
    )
    assert not sim.ok
    assert "active_wound_blocks_candidate_operation" in sim.blocked_reasons


def test_simulator_blocks_unknown_tool():
    sim = simulate_loop_transition(
        LATEST_BLOCKED,
        candidate_operation="loop_tooling",
        requested_tool="NOTATOOL",
    )
    assert not sim.ok
    assert "unknown_tool" in sim.blocked_reasons


def test_simulation_panel_renders():
    sim = simulate_loop_transition(
        LATEST_BLOCKED,
        candidate_operation="loop_tooling",
        requested_tool="RHPSIM",
    )
    panel = render_simulation_panel(sim)
    assert "RHPSIM [GOLD]" in panel
    assert "authority: no grant [LOCKED]" in panel
