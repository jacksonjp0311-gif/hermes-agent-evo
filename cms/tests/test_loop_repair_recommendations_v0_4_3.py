from __future__ import annotations

import unittest

from cms.loop.repair_recommendation import build_loop_repair_recommendations

class LoopRepairRecommendationTests(unittest.TestCase):
    def test_stable_green_loop_emits_noop(self) -> None:
        report = build_loop_repair_recommendations({
            "version": "v0.4.2",
            "pressure_hash": "abc",
            "loop_drift_pressure": 0.0,
            "threshold": 0.25,
            "stability_state": "stable_green_loop",
            "components": {
                "memory_action_drift": 0.0,
                "public_surface_delta": 0.0,
                "registry_status_drift": 0.0,
                "validator_expectation_drift": 0.0,
            },
            "findings": [],
            "validation_failures": [],
        })
        self.assertTrue(report["passed"])
        self.assertEqual(report["recommendation_count"], 1)
        self.assertEqual(report["recommendations"][0]["repair_class"], "NO_REPAIR")

    def test_public_sync_legacy_preseal_finding_maps_to_report_refresh(self) -> None:
        report = build_loop_repair_recommendations({
            "version": "v0.4.2",
            "pressure_hash": "abc",
            "loop_drift_pressure": 0.168,
            "threshold": 0.25,
            "stability_state": "green_with_repair_recommendation",
            "components": {"public_surface_delta": 1.0, "validator_expectation_drift": 0.2},
            "findings": ["public_sync_preseal_pending_until_v0_4_2_tag"],
            "validation_failures": [],
        })
        self.assertTrue(report["passed"])
        classes = {item["repair_class"] for item in report["recommendations"]}
        self.assertIn("REPORT_REFRESH", classes)
        self.assertIn("SURFACE_REPAIR", classes)
        self.assertIn("VALIDATOR_REPAIR", classes)

    def test_validator_pressure_maps_to_validator_repair(self) -> None:
        report = build_loop_repair_recommendations({
            "version": "v0.4.2",
            "pressure_hash": "abc",
            "loop_drift_pressure": 0.1,
            "threshold": 0.25,
            "stability_state": "green_with_repair_recommendation",
            "components": {"validator_expectation_drift": 0.4},
            "findings": [],
            "validation_failures": [],
        })
        self.assertTrue(report["passed"])
        self.assertEqual(report["dominant_repair_class"], "VALIDATOR_REPAIR")

    def test_unknown_finding_requires_human_review_but_is_typed(self) -> None:
        report = build_loop_repair_recommendations({
            "version": "v0.4.2",
            "pressure_hash": "abc",
            "loop_drift_pressure": 0.1,
            "threshold": 0.25,
            "stability_state": "green_with_repair_recommendation",
            "components": {},
            "findings": ["unknown_pressure"],
            "validation_failures": [],
        })
        self.assertTrue(report["passed"])
        self.assertEqual(report["unknown_findings"], ["unknown_pressure"])
        self.assertEqual(report["recommendations"][0]["repair_class"], "HUMAN_REVIEW_REQUIRED")

if __name__ == "__main__":
    unittest.main()
