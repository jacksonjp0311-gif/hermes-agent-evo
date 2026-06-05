from __future__ import annotations

import unittest

from cms.loop.repair_apply_packet import build_apply_packet_manifest


class AuthorizedApplyPacketManifestTests(unittest.TestCase):
    def test_packet_blocks_without_human_authorization(self) -> None:
        report = build_apply_packet_manifest({
            "apply_gate_hash": "abc",
            "source_pressure_state": "stable",
            "apply_gate_count": 1,
            "gates": [
                {
                    "apply_gate_id": "CMS-APPLY-GATE-1",
                    "source_dry_run_id": "CMS-DRYRUN-1",
                    "source_plan_id": "CMS-PLAN-1",
                    "source_recommendation_id": "CMS-RR-1",
                    "repair_class": "NO_REPAIR",
                    "target_writes_allowed": [],
                    "pre_apply_validation_required": ["validate_public_sync"],
                    "post_apply_validation_required": ["validate_public_sync"],
                    "blocked_actions_preserved": ["autonomous_patch"],
                }
            ],
        })
        self.assertTrue(report["passed"])
        self.assertEqual(report["apply_packet_count"], 1)
        packet = report["packets"][0]
        self.assertFalse(packet["apply_authority"])
        self.assertFalse(packet["human_authorization_artifact_present"])
        self.assertEqual(packet["target_writes_performed"], 0)
        self.assertTrue(packet["rollback_binds_every_diff"])

    def test_packet_binds_rollback_to_every_diff_entry(self) -> None:
        report = build_apply_packet_manifest({
            "apply_gate_hash": "abc",
            "source_pressure_state": "warning",
            "apply_gate_count": 1,
            "gates": [
                {
                    "apply_gate_id": "CMS-APPLY-GATE-2",
                    "source_dry_run_id": "CMS-DRYRUN-2",
                    "repair_class": "SURFACE_REPAIR",
                    "target_writes_allowed": ["README.md", "reports/loop/example.json"],
                    "pre_apply_validation_required": ["validate_surface_alignment"],
                    "post_apply_validation_required": ["validate_surface_alignment"],
                    "blocked_actions_preserved": [],
                }
            ],
        })
        packet = report["packets"][0]
        self.assertEqual(packet["diff_entry_count"], 2)
        self.assertEqual(packet["rollback_entry_count"], 2)
        self.assertTrue(packet["rollback_binds_every_diff"])
        self.assertIn("silent_target_write", packet["blocked_actions_preserved"])
        self.assertEqual(report["target_writes_performed"], 0)


if __name__ == "__main__":
    unittest.main()