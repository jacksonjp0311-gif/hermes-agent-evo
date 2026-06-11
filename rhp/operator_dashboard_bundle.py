from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

RHP_OPERATOR_DASHBOARD_BUNDLE_SCHEMA = "RHP-OPERATOR-DASHBOARD-BUNDLE-v0.1"

AXES = ["evidence", "transcript", "wound", "dry_run", "residue", "authority", "tools", "geometry"]

def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))

def build_bundle(root: str | Path = ".") -> dict[str, Any]:
    root = Path(root)
    latest = load_json(root / "docs" / "context-layer" / "latest-rhp.json")
    evidence_rel = latest.get("latest_evidence", "")
    evidence = load_json(root / evidence_rel)
    authority_keys = [
        "provider_call_executed", "model_call_executed", "tool_use_executed",
        "cms_runtime_execution", "cms_write", "memory_write", "memory_promotion",
        "api_write", "dependency_mutation_committed", "external_ingestion",
        "autonomous_authority", "self_authorization",
    ]
    authority = {k: bool(evidence.get(k, False)) for k in authority_keys}
    return {
        "schema": RHP_OPERATOR_DASHBOARD_BUNDLE_SCHEMA,
        "operation": evidence.get("operation", latest.get("latest_operation", "unknown")),
        "evidence": {
            "latest_pointer": "docs/context-layer/latest-rhp.json",
            "latest_evidence": evidence_rel,
            "validation_passed": bool(evidence.get("validation_passed", False)),
            "focused_tests_passed": bool(evidence.get("focused_tests_passed", False)),
        },
        "transcript": {"surface": "docs/context-layer/ops/RHP-014-7-transcript-index.json", "policy": "raw streams are summarized; volatile post-seal streams remain outside committed repo state"},
        "wound": {"surface": "docs/context-layer/ops/RHP-014-7-wound-packet.json", "known_classes": ["generated_source_escape_bug", "powershell_path_normalization_regex_bug", "post_staging_command_stream_residue"]},
        "dry_run": {"surface": "docs/context-layer/ops/RHP-014-7-dry-run-plan.json", "mode": "propose_only"},
        "residue": {"surface": "docs/context-layer/ops/RHP-014-7-residue-snapshot.json", "policy": "classify before cleanup; unknown dirty paths block"},
        "authority": {"ok": all(v is False for v in authority.values()), "locks": authority, "human_authorization_boundary": True},
        "tools": {"surface": "docs/context-layer/ops/RHP-014-7-tool-integration-map.json", "principle": "tools display and classify; All-One performs bounded human-authorized mutation"},
        "geometry": {"surface": "docs/context-layer/ops/RHP-014-7-loop-geometry.json", "axes": AXES, "plain_english": "The dashboard makes the loop geometry visible: origin evidence, bounded axes, authority boundary, next legal delta."},
        "next": evidence.get("next_recommended_operation", "unknown"),
        "non_claim_lock": "Operator dashboard bundle is an orientation and evidence surface only. It grants no autonomy, no provider calls, no memory writes, no CMS writes, and no self-authorization.",
    }

def render_markdown(bundle: dict[str, Any]) -> str:
    rows = [
        "| Axis | Surface | Purpose |",
        "|---|---|---|",
        "| evidence | latest pointer + final evidence | establish origin truth |",
        "| transcript | transcript index | preserve command/replay surfaces |",
        "| wound | wound packet | name failure classes and repairs |",
        "| dry_run | dry-run plan | propose next bounded action |",
        "| residue | residue snapshot | classify dirty state before action |",
        "| authority | authority locks | keep human boundary explicit |",
        "| tools | tool integration map | show what can display/classify/report |",
        "| geometry | loop geometry | make the system shape readable |",
    ]
    return "\n".join([
        "# RHP-014.7 Operator Dashboard Bundle",
        "",
        f"Schema: `{bundle['schema']}`",
        f"Operation: `{bundle['operation']}`",
        f"Authority ok: `{bundle['authority']['ok']}`",
        "",
        "## Geometry",
        bundle["geometry"]["plain_english"],
        "",
        "## Dashboard Axes",
        *rows,
        "",
        "## Next",
        f"`{bundle['next']}`",
        "",
        f"Non-claim lock: {bundle['non_claim_lock']}",
        "",
    ])

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Build or render the RHP operator dashboard bundle")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--out-json", default="")
    parser.add_argument("--out-md", default="")
    args = parser.parse_args(argv)
    bundle = build_bundle(args.repo_root)
    if args.out_json:
        out = Path(args.out_json); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.out_md:
        out = Path(args.out_md); out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_markdown(bundle), encoding="utf-8", newline="\n")
    print(json.dumps(bundle, indent=2, ensure_ascii=False) if args.json else render_markdown(bundle))
    return 0 if bundle.get("authority", {}).get("ok") else 1

if __name__ == "__main__":
    raise SystemExit(main())
