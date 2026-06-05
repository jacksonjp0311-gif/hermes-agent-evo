from __future__ import annotations

import unittest

from cms.loop.drift_pressure import build_loop_drift_pressure


class LoopDriftPressureTests(unittest.TestCase):
    def test_green_loop_with_preseal_public_sync_pressure_passes_but_finds_boundary(self):
        obj = build_loop_drift_pressure(
            loop={
                "loop_closed": True,
                "loop_hash": "loop",
                "memory_counts": {"candidate_count": 1, "promoted_count": 1, "downgraded_count": 0, "observe_only_count": 0},
                "next_cycle_influence": {"allowed": True},
            },
            candidate_actions={
                "candidate_action_count": 1,
                "action_hash": "action",
                "non_claim_lock": "Candidate memory actions are repository-bound and do not prove code correctness.",
                "actions": [{
                    "candidate_id": "x",
                    "downgrade_path": "d",
                    "required_evidence_next": "e",
                    "allowed_next_action": "a",
                    "rehydration_visible": True,
                    "non_claim_lock": "This is repository-bound and does not prove code correctness.",
                }],
            },
            rehydration_score={"version_ready": True, "missing_surfaces": [], "stale_surface_risks": [], "rehydration_hash": "r"},
            registry={"current_version": "v0.4.2", "previous_version": "v0.4.1", "next_anchor": "CMS-SA v0.4.3", "versions": [{"version": "v0.4.1", "status": "validated_sealed_public_sync_passed"}]},
            public_sync={"passed": True, "registry_current_version": "v0.4.1", "head_origin_match": True, "release_tag_status": "present_and_ancestor_of_head"},
            runtime_decision={"decision": "promote", "decision_hash": "d"},
            validation_surfaces={"loop": {"passed": True}},
        )
        self.assertTrue(obj["passed"])
        self.assertIn("public_sync_preseal_pending_until_v0_4_2_tag", obj["findings"])
        self.assertLessEqual(obj["loop_drift_pressure"], obj["threshold"])


if __name__ == "__main__":
    unittest.main()
