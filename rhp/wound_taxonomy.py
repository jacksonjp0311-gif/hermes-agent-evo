from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

RHP_WOUND_TAXONOMY_SCHEMA = "RHP-WOUND-TAXONOMY-v0.1"

WOUND_CLASSES: dict[str, dict[str, Any]] = {
    "no_active_wound": {
        "severity": "none",
        "description": "No active wound is asserted; scaffold/protocol evolution only.",
        "default_next": "continue_bounded_evolution",
    },
    "evidence_api_break": {
        "severity": "high",
        "description": "A public evidence/check key disappeared, changed meaning, or lacks alias/deprecation.",
        "default_next": "restore_key_or_add_alias_then_gate",
    },
    "post_seal_residue_leak": {
        "severity": "high",
        "description": "A repo artifact was written after seal/push instead of volatile external storage.",
        "default_next": "classify_residue_and_add_seal_boundary_gate",
    },
    "remote_ci_red": {
        "severity": "high",
        "description": "Remote CI reported a failing terminal state for a commit subject.",
        "default_next": "create_wound_packet_before_repair",
    },
    "remote_ci_pending": {
        "severity": "medium",
        "description": "Remote CI is pending/unknown for current head; do not claim green closure.",
        "default_next": "wait_or_ingest_final_ci_status",
    },
    "stale_readme_surface": {
        "severity": "medium",
        "description": "README/operator docs no longer describe latest state or required next action.",
        "default_next": "repair_documented_state_and_add_alignment_check",
    },
    "alignment_guard_contract_drift": {
        "severity": "high",
        "description": "Alignment guard expects stale legacy evidence contract.",
        "default_next": "restore_backward_compatibility_or_migrate_with_alias",
    },
    "workflow_slice_failure": {
        "severity": "high",
        "description": "One CI slice failed while local proof may still pass.",
        "default_next": "harvest_remote_logs_and_create_slice_wound_packet",
    },
    "compact_summary_boundary_leak": {
        "severity": "medium",
        "description": "Compact summary was written to repo after commit instead of sealed-before-commit or volatile external.",
        "default_next": "enforce_compact_summary_seal_check",
    },
    "render_hygiene_drift": {
        "severity": "medium",
        "description": "Generated text surface contains literal escaped newline drift or broken physical formatting.",
        "default_next": "normalize_generated_text_surface_and_audit",
    },
    "render_hygiene_auditor_overmatch": {
        "severity": "low",
        "description": "Render hygiene gate treats documentation examples as generated-surface drift.",
        "default_next": "make_auditor_context_aware",
    },
    "doctor_bootstrap_dirty_self_observation": {
        "severity": "medium",
        "description": "Doctor blocks its own authorized construction because bounded operation dirt is visible.",
        "default_next": "add_bootstrap_dirty_read_only_mode",
    },
    "ci_claim_subject_ambiguity": {
        "severity": "high",
        "description": "CI claim lacks an explicit commit/run subject.",
        "default_next": "add_claim_subject_and_source",
    },
    "evidence_replay_incomplete": {
        "severity": "high",
        "description": "Operation cannot be reconstructed from pointer, evidence, summaries, and dashboard.",
        "default_next": "repair_replay_artifact_graph",
    },
    "browser_supervisor_websockets_dependency_api_drift": {
        "severity": "high",
        "description": "Remote browser supervisor CI failure caused by websockets dependency/API drift: missing websockets.proxy or uri.Proxy on installed package surface.",
        "default_next": "bounded_dependency_or_compatibility_repair_proposal",
    },
    "unknown_residue": {
        "severity": "high",
        "description": "Dirty path is not recognized as bounded operation residue.",
        "default_next": "block_and_request_operator_classification",
    },
    "current_script_gate_mismatch": {
        "severity": "high",
        "description": "Evidence script identity does not match the active All-One script.",
        "default_next": "stop_and_reissue_correct_script",
    },
    "secret_scan_trigger": {
        "severity": "critical",
        "description": "Staged diff contains a secret-like token trigger.",
        "default_next": "stop_remove_secret_rotate_if_needed",
    },
}


def registry() -> dict[str, Any]:
    return {
        "schema": RHP_WOUND_TAXONOMY_SCHEMA,
        "wound_classes": WOUND_CLASSES,
        "class_count": len(WOUND_CLASSES),
        "stable_class_names": sorted(WOUND_CLASSES),
        "non_claim_lock": "Wound taxonomy classifies failures only. It does not execute repair, rerun CI, mutate workflows, or grant authority.",
    }


def classify_text(text: str) -> dict[str, Any]:
    lowered = text.lower()
    rules = [
        ("secret_scan_trigger", ["secret", "credential", "private key"]),
        ("post_seal_residue_leak", ["post-seal", "post seal", "residue"]),
        ("compact_summary_boundary_leak", ["compact", "summary", "seal"]),
        ("render_hygiene_auditor_overmatch", ["auditor", "overmatch"]),
        ("render_hygiene_drift", ["literal \\\\n", "render", "newline"]),
        ("doctor_bootstrap_dirty_self_observation", ["doctor", "dirty", "bootstrap"]),
        ("ci_claim_subject_ambiguity", ["ci", "subject", "commit"]),
        ("remote_ci_red", ["ci", "red"]),
        ("remote_ci_pending", ["ci", "pending"]),
        ("evidence_api_break", ["evidence", "api", "break"]),
        ("alignment_guard_contract_drift", ["alignment", "guard"]),
        ("unknown_residue", ["unknown", "dirty"]),
    ]
    for wound_class, terms in rules:
        if all(term in lowered for term in terms):
            data = WOUND_CLASSES[wound_class].copy()
            data.update({"class": wound_class, "matched": True})
            return data
    data = WOUND_CLASSES["no_active_wound"].copy()
    data.update({"class": "no_active_wound", "matched": False})
    return data


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Render or classify RHP wound taxonomy")
    parser.add_argument("--classify", default="")
    parser.add_argument("--out", default="")
    args = parser.parse_args(argv)
    data = classify_text(args.classify) if args.classify else registry()
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.out:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
