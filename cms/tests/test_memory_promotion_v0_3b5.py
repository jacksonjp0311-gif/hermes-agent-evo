
import unittest
from cms.memory import build_memory_promotion_report


class MemoryPromotionTests(unittest.TestCase):
    def test_memory_promotion_report_passes(self):
        report = build_memory_promotion_report()
        self.assertTrue(report["passed"])
        self.assertGreaterEqual(report["promoted_count"], 1)
        self.assertGreaterEqual(report["downgraded_count"], 1)
        self.assertGreaterEqual(report["observe_only_count"], 1)

    def test_promoted_candidates_have_controls(self):
        report = build_memory_promotion_report()
        for item in report["candidates"]:
            if item["memory_decision"] == "promote_memory":
                self.assertTrue(item["negative_control_passed"])
                self.assertGreaterEqual(item["evidence_utility"], 0.80)
                self.assertIn("does not prove", item["non_claim_lock"])


if __name__ == "__main__":
    unittest.main()
