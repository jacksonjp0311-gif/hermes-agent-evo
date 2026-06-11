from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

RHP_EVIDENCE_API_COMPATIBILITY_GATE_SCHEMA = "RHP-EVIDENCE-API-COMPATIBILITY-GATE-v0.2"

AUTHORITY_FIELDS = [
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
]
AUTHORITY_CONTAINER_FIELD = "authority_locks"

PUBLIC_REQUIRED_LATEST_POINTER = [
    "schema",
    "latest_operation",
    "latest_evidence",
    "next_operation",
    "authority_ok",
]

PUBLIC_REQUIRED_FINAL_EVIDENCE = [
    "schema",
    "operation",
    "operator_script_name",
    "validation_passed",
    "focused_tests_passed",
    "non_claim_lock",
]

PUBLIC_OPTIONAL_FINAL_EVIDENCE = [
    "operation_base_commit",
    "observed_previous_sealed_commit",
    "current_operation_commit",
    "current_operation_commit_observed_by",
    "remote_ci_status",
    "integration_closed",
    "wait_state",
    "authority_locks",
]

DEPRECATED_FIELDS = ["latest_commit_or_base"]


def _check_required(data: dict[str, Any], required: list[str]) -> list[str]:
    return [field for field in required if field not in data]


def _authority_locks(data: dict[str, Any]) -> dict[str, Any]:
    locks = data.get(AUTHORITY_CONTAINER_FIELD)
    return locks if isinstance(locks, dict) else {}


def _has_authority_field(data: dict[str, Any], field: str) -> bool:
    return field in data or field in _authority_locks(data)


def _authority_value(data: dict[str, Any], field: str) -> Any:
    if field in data:
        return data.get(field)
    return _authority_locks(data).get(field)


def _missing_authority_fields(data: dict[str, Any]) -> list[str]:
    return [field for field in AUTHORITY_FIELDS if not _has_authority_field(data, field)]


def _authority_not_false(data: dict[str, Any]) -> list[str]:
    return [field for field in AUTHORITY_FIELDS if _authority_value(data, field) is not False]


def gate(repo_root: str | Path = ".", latest_pointer: str = "docs/context-layer/latest-rhp.json") -> dict[str, Any]:
    root = Path(repo_root)
    pointer_path = root / latest_pointer
    pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
    evidence_path = root / pointer["latest_evidence"]
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))

    missing_pointer = _check_required(pointer, PUBLIC_REQUIRED_LATEST_POINTER)
    missing_evidence = _check_required(evidence, PUBLIC_REQUIRED_FINAL_EVIDENCE)
    missing_authority = _missing_authority_fields(evidence)
    authority_not_false = _authority_not_false(evidence)
    deprecated_present = [field for field in DEPRECATED_FIELDS if field in pointer or field in evidence]
    authority_source = (
        "nested_authority_locks"
        if isinstance(evidence.get(AUTHORITY_CONTAINER_FIELD), dict)
        else "top_level_fields"
    )

    public_fields = sorted(set(PUBLIC_REQUIRED_FINAL_EVIDENCE + PUBLIC_OPTIONAL_FINAL_EVIDENCE + AUTHORITY_FIELDS))
    result = {
        "schema": RHP_EVIDENCE_API_COMPATIBILITY_GATE_SCHEMA,
        "ok": not missing_pointer and not missing_evidence and not missing_authority and not authority_not_false,
        "latest_pointer": latest_pointer,
        "latest_operation": pointer.get("latest_operation"),
        "latest_evidence": pointer.get("latest_evidence"),
        "missing_pointer_required": missing_pointer,
        "missing_evidence_required": missing_evidence,
        "missing_authority_fields": missing_authority,
        "authority_not_false": authority_not_false,
        "authority_source": authority_source,
        "deprecated_present": deprecated_present,
        "public_required_latest_pointer": PUBLIC_REQUIRED_LATEST_POINTER,
        "public_required_final_evidence": PUBLIC_REQUIRED_FINAL_EVIDENCE,
        "public_optional_final_evidence": PUBLIC_OPTIONAL_FINAL_EVIDENCE,
        "public_authority_fields": AUTHORITY_FIELDS,
        "public_fields": public_fields,
        "classification": {
            "required": PUBLIC_REQUIRED_LATEST_POINTER + PUBLIC_REQUIRED_FINAL_EVIDENCE,
            "optional": PUBLIC_OPTIONAL_FINAL_EVIDENCE,
            "deprecated": DEPRECATED_FIELDS,
            "private": ["helper implementation details", "temp stream paths unless referenced by sealed summaries"],
            "alias": {"authority_locks": AUTHORITY_FIELDS},
        },
        "non_claim_lock": "Evidence API gate validates local evidence shape only. It does not call remote APIs, rerun CI, execute repairs, or grant authority.",
    }
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate RHP evidence API compatibility")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--latest-pointer", default="docs/context-layer/latest-rhp.json")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = gate(args.repo_root, args.latest_pointer)
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
