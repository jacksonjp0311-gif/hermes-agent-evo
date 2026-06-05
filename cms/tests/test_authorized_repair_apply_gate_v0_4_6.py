from __future__ import annotations

import unittest

from cms.loop.repair_apply_gate import build_apply_gate


class AuthorizedRepairApplyGateTests(unittest.TestCase):
    def test_apply_gate_blocks_without_authorization(self) -> None:
        report = build_apply_gate({
            "dry_run_hash": "abc",
            "source_pressure_state": "stable",
            "dry_run_count": 1,
            "dry_runs": [
                {
                    "dry_run_id": "CMS-DRYRUN-1",
                    "source_plan_id": "CMS-PLAN-1",
                    "source_recommendation_id": "CMS-RR-1",
                    "repair_class": "NO_REPAIR",
                    "target_surface_writes": [],
                    "required_validation_evidence": ["validate_public_sync"],
                    "blocked_actions_preserved": ["autonomous_patch"],
                    "touched_surface_boundary": ["reports/loop"],
                }
            ],
        })
        self.assertTrue(report["passed"])
        self.assertEqual(report["apply_gate_count"], 1)
        gate = report["gates"][0]
        self.assertFalse(gate["apply_authority"])
        self.assertFalse(gate["human_authorization_present"])
        self.assertEqual(gate["target_writes_performed"], 0)
        self.assertTrue(gate["rollback_required"])
        self.assertFalse(gate["rollback_ready"])

    def test_apply_gate_preserves_no_silent_write_actions(self) -> None:
        report = build_apply_gate({
            "dry_run_hash": "abc",
            "source_pressure_state": "warning",
            "dry_run_count": 1,
            "dry_runs": [
                {
                    "dry_run_id": "CMS-DRYRUN-2",
                    "source_plan_id": "CMS-PLAN-2",
                    "source_recommendation_id": "CMS-RR-2",
                    "repair_class": "SURFACE_REPAIR",
                    "target_surface_writes": ["README.md"],
                    "required_validation_evidence": ["validate_surface_alignment"],
                    "blocked_actions_preserved": [],
                    "touched_surface_boundary": ["README.md"],
                }
            ],
        })
        gate = report["gates"][0]
        blocked = gate["blocked_actions_preserved"]
        self.assertIn("silent_target_write", blocked)
        self.assertIn("unreviewed_git_commit", blocked)
        self.assertIn("unreviewed_git_push", blocked)
        self.assertEqual(report["target_writes_performed"], 0)
        self.assertEqual(report["git_commits_performed"], 0)


if __name__ == "__main__":
    unittest.main()