# Read-only Rehydration Protocol runtime bridge for Hermes.
#
# This module exposes the Hermes-local /rhp origin-alignment substrate to
# runtime prompt surfaces without granting write/apply/tool/runtime authority.

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping


FORBIDDEN_AUTHORITIES = {
    "provider_call_executed": False,
    "model_call_executed": False,
    "tool_use_executed": False,
    "runtime_source_mutation": False,
    "cms_runtime_execution": False,
    "cms_write": False,
    "memory_write": False,
    "memory_promotion": False,
    "api_write": False,
    "dependency_mutation_committed": False,
    "env_file_committed": False,
    "rollback_executed": False,
    "self_authorization": False,
    "ongoing_provider_authority": False,
    "autonomous_authority": False,
    "codex_ingestion": False,
}


@dataclass(frozen=True)
class RHPBridgeStatus:
    enabled: bool
    mode: str
    repo_root: str
    rhp_root: str
    origin_hash: str
    alignment_status: str
    latest_manifest_path: str
    latest_alignment_report_path: str
    latest_origin_certificate_path: str
    context_gate: str
    compounding_permitted: bool
    authority: Mapping[str, bool]
    non_claim_lock: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "enabled": self.enabled,
            "mode": self.mode,
            "repo_root": self.repo_root,
            "rhp_root": self.rhp_root,
            "origin_hash": self.origin_hash,
            "alignment_status": self.alignment_status,
            "latest_manifest_path": self.latest_manifest_path,
            "latest_alignment_report_path": self.latest_alignment_report_path,
            "latest_origin_certificate_path": self.latest_origin_certificate_path,
            "context_gate": self.context_gate,
            "compounding_permitted": self.compounding_permitted,
            "authority": dict(self.authority),
            "non_claim_lock": self.non_claim_lock,
        }


def find_repo_root(start: str | Path | None = None) -> Path:
    current = Path(start or Path.cwd()).resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / "pyproject.toml").is_file() and (candidate / ".git").exists():
            return candidate
    raise FileNotFoundError("Could not locate Hermes repository root")


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return data


def load_rhp_context(repo_root: str | Path | None = None) -> dict[str, Any]:
    root = find_repo_root(repo_root)
    rhp_root = root / "rhp"
    manifest_path = rhp_root / "origin_manifest.json"
    report_path = rhp_root / "latest_alignment_report.json"
    certificate_path = rhp_root / "latest_origin_certificate.json"

    for path in (manifest_path, report_path, certificate_path):
        if not path.is_file():
            raise FileNotFoundError(str(path))

    manifest = _load_json(manifest_path)
    report = _load_json(report_path)
    certificate = _load_json(certificate_path)

    if manifest.get("context_default_enabled") is not False:
        raise RuntimeError("RHP context default must remain disabled")

    if certificate.get("compounding_permission") is not False:
        raise RuntimeError("RHP proposal-mode certificate must not permit compounding")

    return {
        "repo_root": str(root),
        "rhp_root": str(rhp_root),
        "manifest_path": str(manifest_path.relative_to(root)),
        "report_path": str(report_path.relative_to(root)),
        "certificate_path": str(certificate_path.relative_to(root)),
        "manifest": manifest,
        "report": report,
        "certificate": certificate,
    }


def get_bridge_status(repo_root: str | Path | None = None) -> RHPBridgeStatus:
    context = load_rhp_context(repo_root)
    manifest = context["manifest"]
    report = context["report"]
    certificate = context["certificate"]

    return RHPBridgeStatus(
        enabled=True,
        mode="read_only_proposal",
        repo_root=context["repo_root"],
        rhp_root=context["rhp_root"],
        origin_hash=str(manifest.get("origin_hash", "")),
        alignment_status=str(report.get("alignment_status", "unknown")),
        latest_manifest_path=context["manifest_path"],
        latest_alignment_report_path=context["report_path"],
        latest_origin_certificate_path=context["certificate_path"],
        context_gate="HERMES_RHP_CONTEXT",
        compounding_permitted=bool(certificate.get("compounding_permission", False)),
        authority=FORBIDDEN_AUTHORITIES,
        non_claim_lock=(
            "RHP runtime bridge is read-only proposal orientation only. "
            "It does not authorize tools, provider/model calls, runtime mutation, "
            "CMS execution, CMS write, memory write, memory promotion, API write, "
            "dependency mutation, Codex ingestion, autonomy, or self-authorization."
        ),
    )


def make_runtime_context_packet(repo_root: str | Path | None = None) -> dict[str, Any]:
    status = get_bridge_status(repo_root)
    context = load_rhp_context(repo_root)
    return {
        "packet_schema": "RHP-HERMES-RUNTIME-CONTEXT-PACKET-v0.1",
        "bridge_status": status.as_dict(),
        "origin_manifest": context["manifest"],
        "alignment_report": context["report"],
        "origin_certificate": context["certificate"],
        "runtime_order": [
            "RHP origin-alignment context",
            "HRCN authority-boundary context",
            "Hermes proposal/runtime loop",
        ],
        "allowed_runtime_use": [
            "display RHP status",
            "include RHP origin summary in session context",
            "orient proposals to declared origin surfaces",
        ],
        "forbidden_runtime_use": [
            "grant tool authority",
            "grant provider/model authority",
            "mutate runtime source",
            "execute CMS runtime",
            "write CMS",
            "write memory",
            "promote memory",
            "write APIs",
            "change dependencies",
            "ingest Codex",
            "operate autonomously",
            "self-authorize",
        ],
    }


def format_context_for_prompt(repo_root: str | Path | None = None) -> str:
    packet = make_runtime_context_packet(repo_root)
    status = packet["bridge_status"]
    report = packet["alignment_report"]
    forbidden = ", ".join(packet["forbidden_runtime_use"])
    drift_count = len(report.get("drift_findings", []))
    return (
        "RHP Runtime Bridge: READ ONLY PROPOSAL ORIENTATION\n"
        f"Origin Hash: {status['origin_hash']}\n"
        f"Alignment: {status['alignment_status']}\n"
        f"Manifest: {status['latest_manifest_path']}\n"
        f"Report: {status['latest_alignment_report_path']}\n"
        f"Certificate: {status['latest_origin_certificate_path']}\n"
        f"Compounding Permitted: {status['compounding_permitted']}\n"
        f"Drift Findings: {drift_count}\n"
        "Runtime Order: RHP before HRCN before Hermes action\n"
        f"Forbidden: {forbidden}\n"
        f"Lock: {status['non_claim_lock']}"
    )


def assert_read_only_boundary(repo_root: str | Path | None = None) -> bool:
    status = get_bridge_status(repo_root)
    if status.mode != "read_only_proposal":
        raise RuntimeError("RHP bridge mode is not read_only_proposal")
    if status.compounding_permitted is not False:
        raise RuntimeError("RHP bridge must not permit compounding in RHP-001")
    for key, value in status.authority.items():
        if value is not False:
            raise RuntimeError(f"RHP bridge authority is not false: {key}")
    return True
