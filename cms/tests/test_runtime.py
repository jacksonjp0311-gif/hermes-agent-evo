import unittest
from pathlib import Path

from cms.core.runtime import CMSRuntime


class TestCMSRuntime(unittest.TestCase):
    def test_runtime_cycle(self):
        runtime = CMSRuntime(Path(__file__).resolve().parents[1], "CMS-Core")
        result = runtime.run_cycle()
        self.assertGreaterEqual(result.k_cms, 0.0)
        self.assertLessEqual(result.k_cms, 1.0)
        self.assertTrue((Path(result.artifacts) / "evidence" / "latest_evidence_package.json").exists())


if __name__ == "__main__":
    unittest.main()