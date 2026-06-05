import unittest

from cms.loop import build_cybernetic_memory_loop


class TestCyberneticMemoryLoopV040(unittest.TestCase):
    def test_loop_closes_with_memory_and_controls(self):
        memory = {"candidate_count": 4, "promoted_count": 2, "downgraded_count": 1, "observe_only_count": 1, "promotion_hash": "abc"}
        decision = {"decision": "promote", "decision_hash": "def"}
        controls = {"false_promote_rejected": True, "downgrade_preserved": True, "observe_only_preserved": True, "harness_hash": "ghi"}
        report = build_cybernetic_memory_loop(memory, decision, controls)
        self.assertTrue(report["passed"])
        self.assertTrue(report["loop_closed"])
        self.assertTrue(report["next_cycle_influence"]["allowed"])
        self.assertIn("loop_hash", report)


if __name__ == "__main__":
    unittest.main()
