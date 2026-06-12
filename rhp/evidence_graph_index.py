from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Iterable

GRAPH_SCHEMA = "RHP-EVIDENCE-GRAPH-INDEX-v0.1"
KNOWN_OPERATION_ORDER: tuple[str, ...] = (
    "RHP-020.0",
    "RHP-020.1",
    "RHP-020.2",
    "RHP-020.3",
    "RHP-020.4",
)

EXPECTED_LATEST_OPERATION = "RHP-020.4"
EXPECTED_LATEST_STATE = "CANONICAL_ALL_ONE_TEMPLATE_EMITTER_ALIGNED_SUBJECT_UNRESOLVED"
EXPECTED_ACTIVE_WOUND = "readiness_gate_install"
EXPECTED_SUBJECT_COMMIT = "ddb24363e2fac630e7527a2c9eab31e6df50db52"
EXPECTED_NEXT_OPERATION = "operator_rerun_or_ingest_replacement_ci_before_repair"

FINAL_EVIDENCE_BY_OPERATION: dict[str, str] = {
    "RHP-020.0": "docs/context-layer/ops/RHP-020-0-final-evidence.json",
    "RHP-020.1": "docs/context-layer/ops/RHP-020-1-final-evidence.json",
    "RHP-020.2": "docs/context-layer/ops/RHP-020-2-final-evidence.json",
    "RHP-020.3": "docs/context-layer/ops/RHP-020-3-final-evidence.json",
    "RHP-020.4": "docs/context-layer/ops/RHP-020-4-final-evidence.json",
}


@dataclass(frozen=True)
class EvidenceGraphReport:
    ok: bool
    latest_ok: bool
    operation_order_ok: bool
    active_wound_ok: bool
    subject_ok: bool
    authority_ok: bool
    graph_complete: bool
    node_count: int
    edge_count: int
    blocking_reasons: tuple[str, ...]


def _locks_false(evidence: Mapping[str, Any]) -> bool:
    locks = evidence.get("authority_locks", {})
    if not isinstance(locks, Mapping):
        return False
    required = (
        "provider_call_executed",
        "model_call_executed",
        "tool_use_executed",
        "cms_runtime_execution",
        "cms_write",
        "memory_write",
        "memory_promotion",
        "api_write",
        "dependency_mutation_committed",
        "external_ingestion",
        "autonomous_authority",
        "self_authorization",
    )
    return all(locks.get(key) is False for key in required)


def build_evidence_graph(
    *,
    latest_rhp: Mapping[str, Any],
    final_evidence_by_operation: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, str]] = []

    for operation in KNOWN_OPERATION_ORDER:
        evidence = final_evidence_by_operation.get(operation, {})
        evidence_path = FINAL_EVIDENCE_BY_OPERATION[operation]
        state = evidence.get("state_after_alignment")
        prior_state = evidence.get("prior_blocking_state")
        subject = evidence.get("subject_commit")
        wound = evidence.get("wound_class")
        next_op = evidence.get("next_recommended_operation")

        modules = []
        tests = []
        for key, value in evidence.items():
            if key.endswith("_module") and isinstance(value, str):
                modules.append(value)
            if key.endswith("_tests") and isinstance(value, str):
                tests.append(value)

        nodes.append(
            {
                "id": operation,
                "type": "operation",
                "evidence": evidence_path,
                "state_after_alignment": state,
                "prior_blocking_state": prior_state,
                "subject_commit": subject,
                "wound_class": wound,
                "next_recommended_operation": next_op,
                "modules": sorted(modules),
                "tests": sorted(tests),
                "active_wound_preserved": evidence.get("active_wound_preserved"),
                "active_subject_closed": evidence.get("active_subject_closed"),
                "repair_execution_enabled": evidence.get("repair_execution_enabled"),
                "authority_locks_false": _locks_false(evidence),
            }
        )
        edges.append({"from": operation, "to": evidence_path, "kind": "operation_has_final_evidence"})
        if modules:
            for module in modules:
                edges.append({"from": operation, "to": module, "kind": "operation_installs_module"})
        if tests:
            for test in tests:
                edges.append({"from": operation, "to": test, "kind": "operation_installs_tests"})

    for left, right in zip(KNOWN_OPERATION_ORDER, KNOWN_OPERATION_ORDER[1:]):
        edges.append({"from": left, "to": right, "kind": "operation_sequence"})

    return {
        "schema": GRAPH_SCHEMA,
        "latest_operation": latest_rhp.get("latest_operation"),
        "latest_state": latest_rhp.get("state"),
        "subject_commit": latest_rhp.get("subject_commit"),
        "active_wound_class": latest_rhp.get("active_wound_class"),
        "next_operation": latest_rhp.get("next_operation"),
        "nodes": nodes,
        "edges": edges,
        "non_claim_lock": "Evidence graph indexes sealed proof surfaces only; it grants no authority.",
    }


def validate_evidence_graph(graph: Mapping[str, Any], latest_rhp: Mapping[str, Any]) -> EvidenceGraphReport:
    reasons: list[str] = []

    latest_ok = (
        graph.get("latest_operation") == EXPECTED_LATEST_OPERATION
        and graph.get("latest_state") == EXPECTED_LATEST_STATE
        and latest_rhp.get("latest_operation") == EXPECTED_LATEST_OPERATION
        and latest_rhp.get("state") == EXPECTED_LATEST_STATE
        and latest_rhp.get("next_operation") == EXPECTED_NEXT_OPERATION
    )
    if not latest_ok:
        reasons.append("latest_pointer_mismatch")

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    operation_ids = tuple(node.get("id") for node in nodes if node.get("type") == "operation")
    operation_order_ok = operation_ids == KNOWN_OPERATION_ORDER
    if not operation_order_ok:
        reasons.append("operation_order_mismatch")

    active_wound_ok = (
        graph.get("active_wound_class") == EXPECTED_ACTIVE_WOUND
        and latest_rhp.get("active_wound_class") == EXPECTED_ACTIVE_WOUND
        and all(node.get("wound_class") == EXPECTED_ACTIVE_WOUND for node in nodes)
    )
    if not active_wound_ok:
        reasons.append("active_wound_mismatch")

    subject_ok = (
        graph.get("subject_commit") == EXPECTED_SUBJECT_COMMIT
        and latest_rhp.get("subject_commit") == EXPECTED_SUBJECT_COMMIT
        and all(node.get("subject_commit") == EXPECTED_SUBJECT_COMMIT for node in nodes)
    )
    if not subject_ok:
        reasons.append("subject_commit_mismatch")

    authority_ok = all(node.get("authority_locks_false") is True for node in nodes)
    if not authority_ok:
        reasons.append("authority_lock_mismatch")

    graph_complete = (
        len(nodes) == len(KNOWN_OPERATION_ORDER)
        and len(edges) >= len(KNOWN_OPERATION_ORDER) * 2
        and all(node.get("evidence") == FINAL_EVIDENCE_BY_OPERATION.get(node.get("id")) for node in nodes)
    )
    if not graph_complete:
        reasons.append("graph_incomplete")

    return EvidenceGraphReport(
        ok=not reasons,
        latest_ok=latest_ok,
        operation_order_ok=operation_order_ok,
        active_wound_ok=active_wound_ok,
        subject_ok=subject_ok,
        authority_ok=authority_ok,
        graph_complete=graph_complete,
        node_count=len(nodes),
        edge_count=len(edges),
        blocking_reasons=tuple(reasons),
    )


def report_to_dict(report: EvidenceGraphReport) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "latest_ok": report.latest_ok,
        "operation_order_ok": report.operation_order_ok,
        "active_wound_ok": report.active_wound_ok,
        "subject_ok": report.subject_ok,
        "authority_ok": report.authority_ok,
        "graph_complete": report.graph_complete,
        "node_count": report.node_count,
        "edge_count": report.edge_count,
        "blocking_reasons": list(report.blocking_reasons),
    }


def render_evidence_graph_panel(report: EvidenceGraphReport) -> str:
    status = "indexed" if report.ok else "blocked"
    reasons = ",".join(report.blocking_reasons) if report.blocking_reasons else "none"
    lines = [
        f"RHPEVIDENCE-GRAPH [GOLD] status={status}",
        "`- evidence graph index",
        f"   +- latest-ok: {str(report.latest_ok).lower()}",
        f"   +- operation-order-ok: {str(report.operation_order_ok).lower()}",
        f"   +- active-wound-ok: {str(report.active_wound_ok).lower()}",
        f"   +- subject-ok: {str(report.subject_ok).lower()}",
        f"   +- authority-ok: {str(report.authority_ok).lower()}",
        f"   +- graph-complete: {str(report.graph_complete).lower()}",
        f"   +- node-count: {report.node_count}",
        f"   +- edge-count: {report.edge_count}",
        f"   +- blocking-reasons: {reasons}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
