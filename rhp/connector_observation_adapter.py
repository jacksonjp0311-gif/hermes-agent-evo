from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

ADAPTER_SCHEMA = "RHP-CONNECTOR-OBSERVATION-ADAPTER-CONTRACT-v0.1"

REQUIRED_OBSERVATION_FIELDS: tuple[str, ...] = (
    "subject_commit",
    "source",
    "observed_status",
    "observed_at_utc",
    "observer",
    "raw_reference",
    "interpretation",
    "authority_granted",
)

ALLOWED_STATUSES: tuple[str, ...] = (
    "success",
    "failure",
    "cancelled",
    "pending",
    "unknown",
)

FORBIDDEN_INTERPRETATIONS: tuple[str, ...] = (
    "current_operation_green",
    "wound_closed_without_subject_match",
    "repair_authorized_by_connector",
    "mutation_authorized_by_connector",
    "model_authorized_by_connector",
    "memory_promotion_authorized_by_connector",
)


@dataclass(frozen=True)
class ConnectorObservationAdapterReport:
    ok: bool
    schema_ok: bool
    subject_ok: bool
    status_ok: bool
    field_contract_ok: bool
    authority_ok: bool
    interpretation_ok: bool
    blocking_reasons: tuple[str, ...]


def connector_observation_contract() -> dict[str, Any]:
    return {
        "schema": ADAPTER_SCHEMA,
        "required_observation_fields": list(REQUIRED_OBSERVATION_FIELDS),
        "allowed_statuses": list(ALLOWED_STATUSES),
        "forbidden_interpretations": list(FORBIDDEN_INTERPRETATIONS),
        "rules": {
            "connector_observes": True,
            "connector_authorizes": False,
            "observation_is_not_mutation": True,
            "unknown_is_not_pass": True,
            "pending_is_named_state": True,
            "subject_commit_required": True,
            "raw_reference_required": True,
        },
        "non_claim_lock": "Connector observations are evidence inputs only; they grant no authority.",
    }


def validate_connector_observation(
    observation: Mapping[str, Any],
    *,
    expected_subject_commit: str,
) -> ConnectorObservationAdapterReport:
    reasons: list[str] = []

    schema_ok = observation.get("schema") == ADAPTER_SCHEMA
    if not schema_ok:
        reasons.append("schema_mismatch")

    subject_ok = observation.get("subject_commit") == expected_subject_commit
    if not subject_ok:
        reasons.append("subject_commit_mismatch")

    status_ok = observation.get("observed_status") in ALLOWED_STATUSES
    if not status_ok:
        reasons.append("observed_status_invalid")

    field_contract_ok = all(field in observation for field in REQUIRED_OBSERVATION_FIELDS)
    if not field_contract_ok:
        reasons.append("required_field_missing")

    authority_ok = observation.get("authority_granted") is False
    if not authority_ok:
        reasons.append("connector_authority_grant_detected")

    interpretation = str(observation.get("interpretation", ""))
    interpretation_ok = not any(forbidden in interpretation for forbidden in FORBIDDEN_INTERPRETATIONS)
    if not interpretation_ok:
        reasons.append("forbidden_interpretation_detected")

    return ConnectorObservationAdapterReport(
        ok=not reasons,
        schema_ok=schema_ok,
        subject_ok=subject_ok,
        status_ok=status_ok,
        field_contract_ok=field_contract_ok,
        authority_ok=authority_ok,
        interpretation_ok=interpretation_ok,
        blocking_reasons=tuple(reasons),
    )


def make_unknown_connector_observation(
    *,
    subject_commit: str,
    source: str,
    raw_reference: str,
    observer: str = "operator",
) -> dict[str, Any]:
    return {
        "schema": ADAPTER_SCHEMA,
        "subject_commit": subject_commit,
        "source": source,
        "observed_status": "unknown",
        "observed_at_utc": "unknown_until_observed",
        "observer": observer,
        "raw_reference": raw_reference,
        "interpretation": "No pass/fail claim. Observation unresolved.",
        "authority_granted": False,
    }


def report_to_dict(report: ConnectorObservationAdapterReport) -> dict[str, Any]:
    return {
        "ok": report.ok,
        "schema_ok": report.schema_ok,
        "subject_ok": report.subject_ok,
        "status_ok": report.status_ok,
        "field_contract_ok": report.field_contract_ok,
        "authority_ok": report.authority_ok,
        "interpretation_ok": report.interpretation_ok,
        "blocking_reasons": list(report.blocking_reasons),
    }


def render_connector_observation_panel(report: ConnectorObservationAdapterReport) -> str:
    status = "accepted" if report.ok else "blocked"
    reasons = ",".join(report.blocking_reasons) if report.blocking_reasons else "none"
    lines = [
        f"RHPCONNECTOR-OBS [GOLD] status={status}",
        "`- connector observation adapter contract",
        f"   +- schema-ok: {str(report.schema_ok).lower()}",
        f"   +- subject-ok: {str(report.subject_ok).lower()}",
        f"   +- status-ok: {str(report.status_ok).lower()}",
        f"   +- field-contract-ok: {str(report.field_contract_ok).lower()}",
        f"   +- authority-ok: {str(report.authority_ok).lower()}",
        f"   +- interpretation-ok: {str(report.interpretation_ok).lower()}",
        f"   +- blocking-reasons: {reasons}",
        "   `- authority: no grant [LOCKED]",
    ]
    return "\n".join(lines)
