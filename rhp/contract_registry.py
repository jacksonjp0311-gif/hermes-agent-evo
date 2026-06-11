from __future__ import annotations

import argparse
import json
from typing import Any

RHP_CONTRACT_REGISTRY_SCHEMA = "RHP-CONTRACT-REGISTRY-v0.1"

STABLE_SYMBOLS: dict[str, list[str]] = {
    "rhp.autoheal_executor_dry_run": [
        "RHP_AUTOHEAL_DRY_RUN_SCHEMA",
        "dry_run_for_packet",
        "build_plan",
        "render_markdown",
    ],
    "rhp.alignment_guard": [
        "AlignmentResult",
        "validate_alignment",
        "find_repo_root",
    ],
    "rhp.ci_pipeline_bridge": [
        "run_bridge",
    ],
    "rhp.current_script_gate": [
        "main",
    ],
}

STABLE_EVIDENCE_KEYS: dict[str, list[str]] = {
    "alignment_guard.checks": [
        "latest_rhp0135_has_boundary_shape",
        "latest_rhp0135_passed",
        "current_pointer_exists",
        "current_evidence_alignment",
        "current_evidence_authority_false",
    ],
    "autoheal_executor_dry_run.result": [
        "schema",
        "ok",
        "classification",
        "allowed_paths",
        "would_mutate",
        "would_commit",
        "would_push",
        "would_execute",
        "dry_run_only",
        "autoheal_execution_enabled",
        "non_claim_lock",
    ],
}

OUTPUT_CONTRACTS: dict[str, str] = {
    "RHPLOAD": "Stable operator/audit box for gates and major phases.",
    "RHPWAIT": "Single-line fill/loading surface only.",
    "RHPDROP": "Closed compact summary surface for repetitive command groups; raw streams remain expandable by path.",
    "RHPDIAG": "Runtime diagnosis box for failures.",
}

AUTHORITY_LOCKS: list[str] = [
    "provider_call_executed", "model_call_executed", "tool_use_executed",
    "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
    "api_write", "dependency_mutation_committed", "external_ingestion",
    "autonomous_authority", "self_authorization",
]


def registry() -> dict[str, Any]:
    return {
        "schema": RHP_CONTRACT_REGISTRY_SCHEMA,
        "stable_symbols": STABLE_SYMBOLS,
        "stable_evidence_keys": STABLE_EVIDENCE_KEYS,
        "output_contracts": OUTPUT_CONTRACTS,
        "authority_locks": AUTHORITY_LOCKS,
        "non_claim_lock": "Registry records stable surfaces only. It grants no runtime, CI, API, model, memory, or self-authorization authority.",
    }


def main(argv=None) -> int:
    argparse.ArgumentParser(description="Print RHP stable contract registry").parse_args(argv)
    print(json.dumps(registry(), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
