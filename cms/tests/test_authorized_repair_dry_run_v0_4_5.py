from __future__ import annotations

import unittest

from cms.loop.repair_dry_run import build_authorized_dry_run

class AuthorizedRepairDryRunTests(unittest.TestCase):
    def test_dry_run_never_writes_target_surfaces(self) -> None:
        report = build_authorized_dry_run({
            "closure_hash": "abc",
            "source_pressure_state": "stable",
            "plan_count": 1,
            "plans": [
                {
                    "plan_id": "CMS-PLAN-1",
                    "source_recommendation_id": "CMS-RR-1",
                    "repair_class": "NO_REPAIR",
                    "touched_surface_boundary": ["reports/loop"],
                    "required_validation_evidence": ["validate_loop_drift_pressure"],
                    "blocked_actions_preserved": ["autonomous_patch"],
                    "closure_state": "closed_no_op",
                }
            ],
        })
        self.assertTrue(report["passed"])
        self.assertEqual(report["target_writes_performed"], 0)
        self.assertEqual(report["dry_runs"][0]["target_surface_writes"], [])
        self.assertFalse(report["dry_runs"][0]["write_authority"])

    def test_dry_run_preserves_blocked_actions(self) -> None:
        report = build_authorized_dry_run({
            "closure_hash": "abc",
            "source_pressure_state": "warning",
            "plan_count": 1,
            "plans": [
                {
                    "plan_id": "CMS-PLAN-2",
                    "source_recommendation_id": "CMS-RR-2",
                    "repair_class": "REGISTRY_REPAIR",
                    "touched_surface_boundary": ["outputs/version_registry/cms_version_registry.json"],
                    "required_validation_evidence": ["validate_public_sync"],
                    "blocked_actions_preserved": ["runtime_code_patch"],
                    "closure_state": "planned_not_executed",
                }
            ],
        })
        blocked = report["dry_runs"][0]["blocked_actions_preserved"]
        self.assertIn("autonomous_patch", blocked)
        self.assertIn("api_write", blocked)
        self.assertIn("git_commit", blocked)
        self.assertTrue(report["dry_runs"][0]["human_authorization_required_for_write"])

if __name__ == "__main__":
    unittest.main()