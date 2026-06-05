from __future__ import annotations

import unittest

from cms.loop.repair_closure import build_repair_closure_plan

class RepairClosurePlanTests(unittest.TestCase):
    def test_no_repair_recommendation_closes_noop(self) -> None:
        report = build_repair_closure_plan({
            "pressure_state": "stable",
            "source_stability_state": "stable_green_loop",
            "recommendation_count": 1,
            "recommendation_hash": "abc",
            "recommendations": [
                {
                    "id": "CMS-RR-NOOP",
                    "repair_class": "NO_REPAIR",
                    "pressure_source": "none",
                    "allowed_repair_action": "continue_after_validation",
                    "blocked_actions": ["autonomous_patch"],
                    "required_validation_stack": ["validate_loop_drift_pressure"],
                    "downgrade_path": "if_pressure_reappears_emit_typed_repair_recommendation",
                }
            ],
        })
        self.assertTrue(report["passed"])
        self.assertEqual(report["plans"][0]["closure_state"], "closed_no_op")
        self.assertFalse(report["plans"][0]["authorization_required"])

    def test_registry_repair_requires_authorization(self) -> None:
        report = build_repair_closure_plan({
            "pressure_state": "warning",
            "source_stability_state": "green_with_repair_recommendation",
            "recommendation_count": 1,
            "recommendation_hash": "abc",
            "recommendations": [
                {
                    "id": "CMS-RR-REG",
                    "repair_class": "REGISTRY_REPAIR",
                    "pressure_source": "registry_status_drift",
                    "allowed_repair_action": "normalize_version_registry_lifecycle_previous_seal_or_next_anchor",
                    "blocked_actions": ["runtime_code_patch", "api_write"],
                    "required_validation_stack": ["validate_surface_alignment", "validate_public_sync"],
                    "downgrade_path": "mark_version_preseal_or_pending_until_registry_agrees",
                }
            ],
        })
        self.assertTrue(report["passed"])
        self.assertEqual(report["plans"][0]["closure_state"], "planned_not_executed")
        self.assertTrue(report["plans"][0]["authorization_required"])

if __name__ == "__main__":
    unittest.main()
