
import unittest
from cms.controls import build_negative_control_harness

class NegativeControlHarnessTests(unittest.TestCase):
    def test_harness_passes(self):
        report = build_negative_control_harness()
        self.assertTrue(report["passed"])
        self.assertTrue(report["false_promote_rejected"])
        self.assertTrue(report["downgrade_preserved"])
        self.assertTrue(report["observe_only_preserved"])

    def test_false_promote_does_not_promote(self):
        report = build_negative_control_harness()
        false_cases = [item for item in report["controls"] if item["control_class"] == "false_promote_control"]
        self.assertTrue(false_cases)
        for item in false_cases:
            self.assertNotEqual(item["observed_decision"], "promote")

if __name__ == "__main__":
    unittest.main()
