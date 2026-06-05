from __future__ import annotations

import json
from pathlib import Path

from cms.loop.drift_pressure import build_loop_drift_pressure

ROOT = Path(__file__).resolve().parents[2]


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_md(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# CMS-SA v0.4.2 Loop Drift Pressure Metrics",
        "",
        f"- passed: `{obj['passed']}`",
        f"- loop_drift_pressure: `{obj['loop_drift_pressure']}`",
        f"- threshold: `{obj['threshold']}`",
        f"- stability_state: `{obj['stability_state']}`",
        f"- recommended_action: `{obj['recommended_action']}`",
        f"- pressure_hash: `{obj['pressure_hash']}`",
        "",
        "## Components",
        "",
        "| Metric | Value |",
        "|---|---:|",
    ]
    for key, value in obj["components"].items():
        lines.append(f"| `{key}` | `{value}` |")
    lines.extend(["", "## Findings", ""])
    lines.extend([f"- `{x}`" for x in obj["findings"]] if obj["findings"] else ["- none"])
    lines.extend(["", "## Primary Lock", "", obj["primary_lock"], "", "## Non-Claim Lock", "", obj["non_claim_lock"], ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    validation_surfaces = {
        "loop": load_json(ROOT / "reports/loop/latest_cybernetic_memory_loop_validation.json"),
        "candidate_actions": load_json(ROOT / "reports/memory/latest_candidate_memory_actions_validation.json"),
        "rehydration_score": load_json(ROOT / "reports/rehydration/latest_thread_rehydration_score_validation.json"),
        "runtime_decision": load_json(ROOT / "reports/decision/latest_runtime_decision_validation.json"),
        "public_sync": load_json(ROOT / "reports/public_sync/latest_public_sync_report.json"),
    }

    obj = build_loop_drift_pressure(
        loop=load_json(ROOT / "outputs/loop/latest_cybernetic_memory_loop.json"),
        candidate_actions=load_json(ROOT / "outputs/memory/latest_candidate_memory_actions.json"),
        rehydration_score=load_json(ROOT / "outputs/rehydration/latest_thread_rehydration_score.json"),
        registry=load_json(ROOT / "outputs/version_registry/cms_version_registry.json"),
        public_sync=load_json(ROOT / "reports/public_sync/latest_public_sync_report.json"),
        runtime_decision=load_json(ROOT / "outputs/decision/latest_runtime_decision.json"),
        validation_surfaces=validation_surfaces,
    )

    write_json(ROOT / "outputs/loop/latest_loop_drift_pressure.json", obj)
    write_json(ROOT / "reports/loop/latest_loop_drift_pressure.json", obj)
    write_md(ROOT / "reports/loop/latest_loop_drift_pressure.md", obj)

    print(json.dumps({
        "schema": "CMS-SA-v0.4.2-loop-drift-pressure-emission",
        "passed": obj["passed"],
        "version": obj["version"],
        "loop_drift_pressure": obj["loop_drift_pressure"],
        "threshold": obj["threshold"],
        "stability_state": obj["stability_state"],
        "recommended_action": obj["recommended_action"],
        "findings": obj["findings"],
        "pressure_hash": obj["pressure_hash"],
        "non_claim_lock": obj["non_claim_lock"],
    }, indent=2, sort_keys=True))
    return 0 if obj["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
