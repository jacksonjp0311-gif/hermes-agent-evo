from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from rhp.loop_tool_registry import get_tool


ACTIVE_WOUND_STATES: tuple[str, ...] = (
    "REPLACEMENT_CI_CONNECTOR_INTAKE_UNRESOLVED",
    "REPLACEMENT_CI_OBSERVATION_UNRESOLVED",
    "ZERO_CONTEXT_AI_BOOTSTRAP_CONTRACT_ALIGNED_SUBJECT_UNRESOLVED",
    "LOOP_GEOMETRY_ALIGNMENT_GUARD_ALIGNED_SUBJECT_UNRESOLVED",
)

CI_BLOCKING_NEXT = "operator_rerun_or_ingest_replacement_ci_before_repair"


@dataclass(frozen=True)
class LoopSimulation:
    ok: bool
    candidate_operation: str
    requested_tool: str
    current_state: str
    active_wound: str
    next_operation: str
    can_mutate: bool
    can_close_wound: bool
    can_repair: bool
    blocked_reasons: tuple[str, ...]
    simulated_stages: tuple[str, ...]


def simulate_loop_transition(
    latest_rhp: Mapping[str, Any],
    *,
    candidate_operation: str,
    requested_tool: str,
) -> LoopSimulation:
    current_state = str(latest_rhp.get("state", ""))
    active_wound = str(latest_rhp.get("active_wound_class", ""))
    next_operation = str(latest_rhp.get("next_operation", ""))

    blocked: list[str] = []
    try:
        tool = get_tool(requested_tool)
    except KeyError:
        tool = None
        blocked.append("unknown_tool")

    wound_active = bool(active_wound and active_wound != "none")
    ci_blocked = next_operation == CI_BLOCKING_NEXT or current_state in ACTIVE_WOUND_STATES

    can_close_wound = False
    can_repair = False
    can_mutate = False

    if tool is None:
        pass
    else:
        if tool.grants_authority:
            blocked.append("tool_grants_authority")
        if tool.closes_wound:
            blocked.append("tool_closes_wound")
        if tool.repairs_code:
            blocked.append("tool_repairs_code")
        if tool.authority_tier == "authorized_mutation":
            blocked.append("authorized_mutation_not_allowed_in_simulator")
        if wound_active and ci_blocked and candidate_operation not in {
            "loop_tooling",
            "diagnostic",
            "evidence_only",
            "connector_ci_observation",
            "zero_context_bootstrap",
        }:
            blocked.append("active_wound_blocks_candidate_operation")
        if tool.writes_repo and candidate_operation not in {"loop_tooling", "evidence_only"}:
            blocked.append("tool_writes_repo_outside_allowed_candidate_class")
        can_mutate = bool(tool.writes_repo and not blocked and candidate_operation in {"loop_tooling", "evidence_only"})

    ok = not blocked
    stages = (
        "ENTRYPOINT-GATE",
        "ROOT-ANCHOR",
        "RESIDUE-MANAGER",
        "PREAUTH-PULL",
        "RHPLOOP-RUNTIME",
        "HUMAN-AUTHORIZATION",
        "RHPREADY",
        "OPERATION-START",
        "RHPTOOL",
        "RHPSIM",
        "VALIDATION",
        "SECRET-SCAN",
        "COMMIT-SEAL" if can_mutate else "NO-COMMIT",
        "PUSH-SEAL" if can_mutate else "NO-PUSH",
        "RHPDROP",
        "RHPREFLECT",
        "POST-SEAL-RESIDUE",
        "RETURN-ROOT",
        "HUMAN-UI-SUMMARY",
    )
    return LoopSimulation(
        ok=ok,
        candidate_operation=candidate_operation,
        requested_tool=requested_tool,
        current_state=current_state,
        active_wound=active_wound,
        next_operation=next_operation,
        can_mutate=can_mutate,
        can_close_wound=can_close_wound,
        can_repair=can_repair,
        blocked_reasons=tuple(blocked),
        simulated_stages=stages,
    )


def simulation_to_dict(sim: LoopSimulation) -> dict[str, Any]:
    return {
        "ok": sim.ok,
        "candidate_operation": sim.candidate_operation,
        "requested_tool": sim.requested_tool,
        "current_state": sim.current_state,
        "active_wound": sim.active_wound,
        "next_operation": sim.next_operation,
        "can_mutate": sim.can_mutate,
        "can_close_wound": sim.can_close_wound,
        "can_repair": sim.can_repair,
        "blocked_reasons": list(sim.blocked_reasons),
        "simulated_stages": list(sim.simulated_stages),
    }


def render_simulation_panel(sim: LoopSimulation) -> str:
    status = "allowed" if sim.ok else "blocked"
    lines = [
        f"RHPSIM [GOLD] status={status}",
        "`- loop transition simulation",
        f"   +- candidate-operation: {sim.candidate_operation}",
        f"   +- requested-tool: {sim.requested_tool}",
        f"   +- current-state: {sim.current_state}",
        f"   +- active-wound: {sim.active_wound or 'none'}",
        f"   +- can-mutate: {str(sim.can_mutate).lower()}",
        f"   +- can-close-wound: {str(sim.can_close_wound).lower()}",
        f"   +- can-repair: {str(sim.can_repair).lower()}",
        f"   +- blocked-reasons: {','.join(sim.blocked_reasons) if sim.blocked_reasons else 'none'}",
        f"   +- simulated-stage-count: {len(sim.simulated_stages)}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
