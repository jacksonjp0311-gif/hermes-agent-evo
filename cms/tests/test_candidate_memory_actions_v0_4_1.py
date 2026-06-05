import unittest

from cms.memory.actions import build_candidate_memory_actions


class TestCandidateMemoryActionsV041(unittest.TestCase):
    def test_actions_are_candidate_level(self):
        memory = {
            "candidate_count": 1,
            "promotion_hash": "abc",
            "candidates": [{
                "candidate_id": "x",
                "memory_decision": "promote_memory",
                "evidence_utility": 0.9,
                "negative_control_passed": True,
                "falsification_condition": "fails if no evidence",
                "non_claim_lock": "does not prove code correctness",
            }],
        }
        loop = {"loop_hash": "def"}
        report = build_candidate_memory_actions(memory, loop)
        self.assertEqual(report["candidate_action_count"], 1)
        self.assertEqual(report["actions"][0]["allowed_next_action"], "may_influence_next_cycle_after_rehydration_scan")
        self.assertTrue(report["actions"][0]["rehydration_visible"])


if __name__ == "__main__":
    unittest.main()
