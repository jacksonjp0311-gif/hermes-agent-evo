from __future__ import annotations

import json
from hashlib import sha256
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TARGETS = {
    "origin": [
        "docs/theory",
        "docs/reflection/law_of_sufficient_form_v0_2b3.md",
        "README.md",
    ],
    "architecture": [
        "docs/architecture/cms_sa_v0_1_software_architecture.tex",
        "docs/architecture",
        "AGENTS.md",
        "README_90_SECONDS.md",
        "docs/context/repository_context_index.json",
        "docs/context/rcc_nexus_index.json",
        "rcc/nexus/route_map.json",
        "rcc/nexus/task_routing_matrix.md",
    ],
    "runtime": [
        "README.md",
        "outputs/version_registry/cms_version_registry.json",
        "reports/public_sync/latest_public_sync_report.md",
        "reports/decision/latest_runtime_decision_validation.md",
        "reports/controls/latest_negative_control_validation.md",
        "reports/memory/latest_memory_promotion_validation.md",
        "reports/loop/latest_cybernetic_memory_loop_validation.md",
        "outputs/memory/latest_candidate_memory_actions.json",
    ],
}


def exists(rel: str) -> bool:
    return (ROOT / rel).exists()


def main() -> int:
    missing: list[str] = []
    for group in TARGETS.values():
        for rel in group:
            if not exists(rel):
                missing.append(rel)

    stale_surface_risks = []
    registry_path = ROOT / "outputs/version_registry/cms_version_registry.json"
    if registry_path.exists():
        registry = json.loads(registry_path.read_text(encoding="utf-8"))
        versions = registry.get("versions", [])
        for entry in versions:
            if isinstance(entry, dict) and entry.get("version") == "v0.4.0" and entry.get("status") == "pending_validation":
                stale_surface_risks.append("v0.4.0_registry_entry_pending_validation")
    else:
        stale_surface_risks.append("missing_version_registry")

    origin_complete = all(exists(x) for x in TARGETS["origin"])
    architecture_complete = all(exists(x) for x in TARGETS["architecture"])
    runtime_complete = all(exists(x) for x in TARGETS["runtime"])
    version_ready = origin_complete and architecture_complete and runtime_complete and not missing

    score_parts = [origin_complete, architecture_complete, runtime_complete, version_ready]
    rehydration_score = round(sum(1 for x in score_parts if x) / len(score_parts), 3)

    obj = {
        "schema": "CMS-SA-v0.4.1-thread-rehydration-score",
        "version": "v0.4.1",
        "passed": version_ready,
        "origin_scan_complete": origin_complete,
        "architecture_scan_complete": architecture_complete,
        "runtime_scan_complete": runtime_complete,
        "version_ready": version_ready,
        "missing_surfaces": missing,
        "stale_surface_risks": stale_surface_risks,
        "rehydration_score": rehydration_score,
        "core_rule": "theory tells why; architecture tells how; runtime tells now",
        "non_claim_lock": "Thread rehydration scoring is repository-bound and does not prove code correctness.",
    }
    stable = json.dumps(obj, sort_keys=True)
    obj["rehydration_hash"] = sha256(stable.encode("utf-8")).hexdigest()

    for rel in ["outputs/rehydration/latest_thread_rehydration_score.json", "reports/rehydration/latest_thread_rehydration_score.json"]:
        path = ROOT / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    lines = [
        "# CMS-SA v0.4.1 Thread Rehydration Score",
        "",
        f"- passed: `{obj['passed']}`",
        f"- origin_scan_complete: `{origin_complete}`",
        f"- architecture_scan_complete: `{architecture_complete}`",
        f"- runtime_scan_complete: `{runtime_complete}`",
        f"- version_ready: `{version_ready}`",
        f"- rehydration_score: `{rehydration_score}`",
        f"- rehydration_hash: `{obj['rehydration_hash']}`",
        "",
        "## Stale Surface Risks",
        "",
    ]
    lines.extend([f"- `{x}`" for x in stale_surface_risks] if stale_surface_risks else ["- none"])
    lines.extend(["", "## Non-Claim Lock", "", obj["non_claim_lock"], ""])
    md = ROOT / "reports/rehydration/latest_thread_rehydration_score.md"
    md.parent.mkdir(parents=True, exist_ok=True)
    md.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps({
        "schema": "CMS-SA-v0.4.1-thread-rehydration-score-emission",
        "passed": obj["passed"],
        "version_ready": obj["version_ready"],
        "rehydration_score": obj["rehydration_score"],
        "stale_surface_risks": stale_surface_risks,
        "non_claim_lock": obj["non_claim_lock"],
    }, indent=2, sort_keys=True))
    return 0 if obj["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
