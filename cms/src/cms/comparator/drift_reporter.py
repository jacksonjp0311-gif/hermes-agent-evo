from __future__ import annotations

from typing import Any


class DriftReporter:
    """Computes CMS-SA v0.2 drift report from metric evaluation."""

    def compute(self, observation: dict[str, Any], metric_eval: dict[str, Any]) -> dict[str, Any]:
        metrics = metric_eval.get("metrics", {})

        d_route = 1.0 - float(metrics.get("mini_readme_presence", 0.0))
        d_validation = 0.0 if metric_eval.get("passed") else 0.25
        d_memory = 1.0 - float(metrics.get("version_memory_presence", 0.0))
        d_narrative = 1.0 - float(metrics.get("required_surface_coverage", 0.0))
        d_public = 0.0

        drift_terms = {
            "goal_drift": 0.0,
            "lock_drift": 0.0,
            "route_drift": max(0.0, min(1.0, d_route)),
            "validation_drift": max(0.0, min(1.0, d_validation)),
            "memory_drift": max(0.0, min(1.0, d_memory)),
            "correction_drift": 0.0,
            "narrative_surface_drift": max(0.0, min(1.0, d_narrative)),
            "public_surface_drift": d_public,
        }

        d_cms = sum(drift_terms.values()) / len(drift_terms)
        return {
            "schema": "CMS-SA-v0.2-drift-report",
            "drift": drift_terms,
            "D_CMS": d_cms,
            "K_CMS": 1.0 - d_cms,
            "findings": metric_eval.get("findings", []),
            "non_claim_lock": "low drift is not truth or code correctness",
        }