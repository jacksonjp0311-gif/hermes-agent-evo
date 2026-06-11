from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

RHP_AUTOHEAL_DRY_RUN_SCHEMA = "RHP-AUTOHEAL-EXECUTOR-DRY-RUN-v0.1"
SCHEMA = RHP_AUTOHEAL_DRY_RUN_SCHEMA

AUTH = [
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

KNOWN_CLASSIFICATIONS: dict[str, list[str]] = {
    "stream_output_leak_or_crlf_noise": [
        "docs/context-layer/ops",
        "command-streams",
    ],
    "module_path_execution_bug": [
        "rhp/ci_pipeline_bridge.py",
        "rhp/autoheal_executor_dry_run.py",
    ],
    "current_script_gate_missing_evidence": [
        "docs/context-layer/ops",
        "docs/context-layer/latest-rhp.json",
    ],
    "stale_evidence_key_surface": [
        "rhp/alignment_guard.py",
        "README.md",
        "docs/context-layer/latest-rhp.json",
    ],
    "boot_preflight_ok_false": [
        "rhp/alignment_guard.py",
        "rhp/boot_preflight.py",
    ],
    "operator_startup_degraded": [
        "rhp/operator_startup_status.py",
        "rhp/alignment_guard.py",
    ],
    "autoheal_dry_run_api_compatibility": [
        "rhp/autoheal_executor_dry_run.py",
        "rhp/ci_pipeline_bridge.py",
    ],
}


@dataclass(frozen=True)
class AutohealDryRun:
    ok: bool
    classification: str
    allowed_paths: list[str] = field(default_factory=list)
    stop_reason: str = ""
    actions: list[dict[str, Any]] = field(default_factory=list)
    schema: str = RHP_AUTOHEAL_DRY_RUN_SCHEMA
    would_mutate: bool = False
    would_commit: bool = False
    would_push: bool = False
    would_execute: bool = False
    dry_run_only: bool = True
    autoheal_execution_enabled: bool = False
    non_claim_lock: str = (
        "Autoheal dry-run classifies and proposes only. It does not mutate files, "
        "commit, push, rerun CI, call remote APIs, or grant authority."
    )

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "ok": self.ok,
            "classification": self.classification,
            "allowed_paths": list(self.allowed_paths),
            "stop_reason": self.stop_reason,
            "actions": list(self.actions),
            "would_mutate": self.would_mutate,
            "would_commit": self.would_commit,
            "would_push": self.would_push,
            "would_execute": self.would_execute,
            "dry_run_only": self.dry_run_only,
            "autoheal_execution_enabled": self.autoheal_execution_enabled,
            "non_claim_lock": self.non_claim_lock,
        }


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def _classification_from_packet(packet: dict[str, Any]) -> str:
    value = packet.get("classification")
    if isinstance(value, str) and value:
        return value
    failures = packet.get("failures") or packet.get("failure_classes") or packet.get("issues") or []
    if isinstance(failures, str):
        return failures
    if isinstance(failures, list) and failures:
        return str(failures[0])
    return "unknown"


def dry_run_for_packet(packet: dict[str, Any]) -> AutohealDryRun:
    classification = _classification_from_packet(packet)
    allowed_paths = KNOWN_CLASSIFICATIONS.get(classification)
    if not allowed_paths:
        return AutohealDryRun(
            ok=False,
            classification=classification,
            allowed_paths=[],
            stop_reason=f"unknown classification: {classification}",
            actions=[
                {
                    "step": "collect_more_evidence",
                    "mode": "diagnosis_only",
                    "allowed": True,
                    "executes": False,
                }
            ],
        )
    return AutohealDryRun(
        ok=True,
        classification=classification,
        allowed_paths=allowed_paths,
        stop_reason="",
        actions=[
            {
                "step": "collect_ci_wound",
                "mode": "read_or_paste_only",
                "allowed": True,
                "executes": False,
            },
            {
                "step": "classify_failure",
                "mode": "diagnosis_only",
                "allowed": True,
                "executes": False,
            },
            {
                "step": "propose_patch",
                "mode": "proposal_only",
                "allowed": True,
                "executes": False,
            },
            {
                "step": "execute_patch",
                "mode": "blocked",
                "allowed": False,
                "executes": False,
            },
            {
                "step": "rerun_ci",
                "mode": "blocked",
                "allowed": False,
                "executes": False,
            },
        ],
    )


def build_plan(root: str | Path = ".", ci_status: str = "unknown") -> dict[str, Any]:
    root_path = Path(root)
    pointer = load_json(root_path / "docs" / "context-layer" / "latest-rhp.json")
    evidence = load_json(root_path / str(pointer["latest_evidence"]))
    authority = {key: bool(evidence.get(key, False)) for key in AUTH}
    issues = []
    if ci_status == "red" or evidence.get("ci_red_wound_observed") is True:
        issues.append("remote_ci_red")
    if not bool(evidence.get("validation_passed", False)):
        issues.append("local_validation_not_confirmed")
    if not all(value is False for value in authority.values()):
        issues.append("authority_drift")
    dry = dry_run_for_packet({"classification": "autoheal_dry_run_api_compatibility" if ci_status == "red" else "unknown"})
    return {
        "schema": SCHEMA,
        "operation": pointer.get("latest_operation"),
        "latest_evidence": pointer.get("latest_evidence"),
        "next_operation": pointer.get("next_operation"),
        "ci_status": ci_status,
        "issues": issues,
        "authority_ok": all(value is False for value in authority.values()),
        "autoheal_execution_enabled": False,
        "dry_run_only": True,
        "actions": dry.as_dict()["actions"],
        "recommendation": "Collect remote CI logs or copied failure text next; keep execution disabled until the dry-run plan is reviewed.",
        "non_claim_lock": "Autoheal dry-run proposes and classifies only. It does not mutate files, execute repairs, rerun CI, or grant authority.",
    }


def render_markdown(plan: dict[str, Any]) -> str:
    rows = ["| Step | Mode | Allowed | Executes |", "|---|---|---:|---:|"]
    for action in plan["actions"]:
        rows.append(f"| {action['step']} | `{action['mode']}` | `{action['allowed']}` | `{action['executes']}` |")
    return "\n".join([
        "# RHP Autoheal Executor Dry-Run",
        "",
        f"Schema: `{plan['schema']}`",
        f"Operation: `{plan['operation']}`",
        f"CI status: `{plan['ci_status']}`",
        f"Autoheal execution enabled: `{plan['autoheal_execution_enabled']}`",
        f"Dry-run only: `{plan['dry_run_only']}`",
        "",
        *rows,
        "",
        f"Recommendation: {plan['recommendation']}",
        "",
        f"Non-claim lock: {plan['non_claim_lock']}",
        "",
    ])


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description="Build an RHP autoheal executor dry-run plan")
    p.add_argument("--repo-root", default=".")
    p.add_argument("--ci-status", default="unknown", choices=["green", "red", "unknown"])
    p.add_argument("--json", action="store_true")
    p.add_argument("--out-json", default="")
    p.add_argument("--out-md", default="")
    a = p.parse_args(argv)
    plan = build_plan(a.repo_root, a.ci_status)
    if a.out_json:
        out = Path(a.out_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if a.out_md:
        out = Path(a.out_md)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(plan), encoding="utf-8", newline="\n")
    print(json.dumps(plan, indent=2, ensure_ascii=False) if a.json else render_markdown(plan))
    return 0 if plan["authority_ok"] and plan["dry_run_only"] and not plan["autoheal_execution_enabled"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
