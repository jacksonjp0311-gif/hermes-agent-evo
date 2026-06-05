from __future__ import annotations

import unittest

from cms.loop.repair_dry_apply_sandbox import build_dry_apply_sandbox


class AuthorizedDryApplySandboxTests(unittest.TestCase):
    def test_dry_apply_sandbox_never_writes_live_targets(self) -> None:
        report = build_dry_apply_sandbox({
            "apply_packet_manifest_hash": "abc",
            "source_pressure_state": "stable",
            "apply_packet_count": 1,
            "packets": [
                {
                    "apply_packet_id": "CMS-APPLY-PACKET-1",
                    "source_apply_gate_id": "CMS-GATE-1",
                    "packet_state": "blocked_missing_human_authorization_packet",
                    "human_authorization_artifact_present": False,
                    "diff_entry_count": 0,
                    "diff_manifest": [],
                    "blocked_actions_preserved": [],
                }
            ],
        })
        self.assertTrue(report["passed"])
        self.assertEqual(report["dry_apply_run_count"], 1)
        self.assertEqual(report["live_target_writes_performed"], 0)
        self.assertEqual(report["api_writes_performed"], 0)
        self.assertEqual(report["git_commits_performed"], 0)
        run = report["runs"][0]
        self.assertFalse(run["apply_authority"])
        self.assertTrue(run["rollback_simulation_passed"])
        self.assertIn("live_target_write", run["blocked_actions_preserved"])

    def test_dry_apply_sandbox_counts_virtual_operations_only(self) -> None:
        report = build_dry_apply_sandbox({
            "apply_packet_manifest_hash": "abc",
            "source_pressure_state": "warning",
            "apply_packet_count": 1,
            "packets": [
                {
                    "apply_packet_id": "CMS-APPLY-PACKET-2",
                    "source_apply_gate_id": "CMS-GATE-2",
                    "packet_state": "blocked_missing_human_authorization_packet",
                    "human_authorization_artifact_present": False,
                    "diff_entry_count": 1,
                    "diff_manifest": [
                        {
                            "target": "README.md",
                            "operation": "replace_text",
                            "before_hash": "before",
                            "after_hash": "after",
                            "diff_preview": "--- a/README.md",
                        }
                    ],
                    "blocked_actions_preserved": [],
                }
            ],
        })
        self.assertTrue(report["passed"])
        self.assertEqual(report["virtual_target_writes_performed"], 1)
        self.assertEqual(report["live_target_writes_performed"], 0)
        run = report["runs"][0]
        self.assertEqual(run["sandbox_operation_count"], 1)
        self.assertEqual(run["rollback_simulation_count"], 1)
        self.assertTrue(run["rollback_simulation_passed"])


if __name__ == "__main__":
    unittest.main()