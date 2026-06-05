
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from typing import Any, Dict, List

VERSION = "v0.3b5"
SCHEMA = "CMS-SA-v0.3b5-memory-promotion-report"

NON_CLAIM_LOCK = (
    "Memory promotion is repository-bound and does not prove code correctness, "
    "truth, AGI, consciousness, production readiness, security, external "
    "validation, or real-world correctness."
)

VALID_MEMORY_DECISIONS = {
    "promote_memory",
    "downgrade_memory",
    "observe_only",
    "block_memory",
}


@dataclass(frozen=True)
class MemoryCandidate:
    candidate_id: str
    source: str
    evidence_utility: float
    negative_control_passed: bool
    runtime_decision_state: str
    downgrade_path: str
    falsification_condition: str
    lesson: str
    non_claim_lock: str = NON_CLAIM_LOCK


def evaluate_memory_candidate(candidate: MemoryCandidate) -> str:
    if candidate.runtime_decision_state == "block":
        return "block_memory"
    if candidate.negative_control_passed is not True:
        return "block_memory"
    if not candidate.downgrade_path or not candidate.falsification_condition:
        return "block_memory"
    if candidate.evidence_utility >= 0.80:
        return "promote_memory"
    if candidate.evidence_utility >= 0.50:
        return "downgrade_memory"
    return "observe_only"


def _default_candidates() -> List[MemoryCandidate]:
    return [
        MemoryCandidate(
            candidate_id="CMS-MEM-001-runtime-decision-kernel",
            source="v0.3b3 runtime decision + replay ledger",
            evidence_utility=0.86,
            negative_control_passed=True,
            runtime_decision_state="promote",
            downgrade_path="downgrade_to_decision_surface_observation_if_replay_hash_missing",
            falsification_condition="Fails if decision lacks validator aggregation, decision hash, or replay surface.",
            lesson="Validator signals should aggregate into one replayable decision object before promotion.",
        ),
        MemoryCandidate(
            candidate_id="CMS-MEM-002-negative-control-refusal",
            source="v0.3b4 negative control and downgrade harness",
            evidence_utility=0.91,
            negative_control_passed=True,
            runtime_decision_state="promote",
            downgrade_path="downgrade_to_control_observation_if_false_promote_rejection_missing",
            falsification_condition="Fails if false promote, downgrade, or observe-only controls are absent or fail.",
            lesson="A system is not promoted by happy-path validation alone; it must reject false success.",
        ),
        MemoryCandidate(
            candidate_id="CMS-MEM-003-paste-safe-execution",
            source="CMS-L-026 and CMS-L-027 failure ledger entries",
            evidence_utility=0.72,
            negative_control_passed=True,
            runtime_decision_state="promote",
            downgrade_path="downgrade_to_operator_process_warning_if_file_run_boundary_not_preserved",
            falsification_condition="Fails if future patch flow combines preflight failure and write phase in one interactive paste.",
            lesson="Evolution patches require file-run scripts or short isolated paste-safe cells.",
        ),
        MemoryCandidate(
            candidate_id="CMS-MEM-004-incomplete-external-correlation",
            source="external theory architecture correlation candidate",
            evidence_utility=0.43,
            negative_control_passed=True,
            runtime_decision_state="observe_only",
            downgrade_path="hold_as_observe_only_until_repository_bound_evidence_exists",
            falsification_condition="Fails if an external conceptual correlation is promoted without repo-bound artifacts and validators.",
            lesson="Cross-project resonance is useful only as a candidate until evidence surfaces exist.",
        ),
    ]


def build_memory_promotion_report() -> Dict[str, Any]:
    candidates: List[Dict[str, Any]] = []
    for candidate in _default_candidates():
        decision = evaluate_memory_candidate(candidate)
        item = asdict(candidate)
        item["memory_decision"] = decision
        item["promoted"] = decision == "promote_memory"
        item["downgraded"] = decision == "downgrade_memory"
        item["observe_only"] = decision == "observe_only"
        item["blocked"] = decision == "block_memory"
        candidates.append(item)

    promoted_count = sum(1 for item in candidates if item["promoted"])
    downgraded_count = sum(1 for item in candidates if item["downgraded"])
    observe_only_count = sum(1 for item in candidates if item["observe_only"])
    blocked_count = sum(1 for item in candidates if item["blocked"])

    passed = (
        promoted_count >= 1
        and downgraded_count >= 1
        and observe_only_count >= 1
        and all(item.get("downgrade_path") for item in candidates)
        and all(item.get("falsification_condition") for item in candidates)
        and all("does not prove" in item.get("non_claim_lock", "") for item in candidates)
    )

    body: Dict[str, Any] = {
        "schema": SCHEMA,
        "version": VERSION,
        "passed": passed,
        "candidate_count": len(candidates),
        "promoted_count": promoted_count,
        "downgraded_count": downgraded_count,
        "observe_only_count": observe_only_count,
        "blocked_count": blocked_count,
        "candidates": candidates,
        "core_rule": "Memory is not storage; memory is controlled influence on future repository action.",
        "promotion_rule": "Promote only reusable invariants that survive evidence utility, negative controls, downgrade paths, falsification conditions, and non-claim locks.",
        "next_boundary": "v0.4.0 may begin after memory promotion reports pass and remain downgrade-safe.",
        "non_claim_lock": NON_CLAIM_LOCK,
    }
    stable = json.dumps(body, sort_keys=True, separators=(",", ":"))
    body["promotion_hash"] = sha256(stable.encode("utf-8")).hexdigest()
    return body
