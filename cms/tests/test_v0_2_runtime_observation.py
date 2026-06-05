import unittest
from pathlib import Path

from cms.observation.repository_observer import RepositoryObserver
from cms.metrics.metric_contracts import MetricContractLoader
from cms.comparator.drift_reporter import DriftReporter
from cms.core.runtime import CMSRuntime


ROOT = Path(__file__).resolve().parents[1]


class TestCMSV02Runtime(unittest.TestCase):
    def test_observer_emits_manifest(self):
        observation = RepositoryObserver(ROOT).observe()
        self.assertIn("file_count", observation)
        self.assertIn("required_surfaces", observation)

    def test_metric_contracts_evaluate(self):
        observation = RepositoryObserver(ROOT).observe()
        loader = MetricContractLoader(ROOT)
        contracts = loader.load()
        evaluation = loader.evaluate(observation, contracts)
        self.assertIn("metrics", evaluation)
        self.assertIn("passed", evaluation)

    def test_drift_report(self):
        observation = RepositoryObserver(ROOT).observe()
        loader = MetricContractLoader(ROOT)
        evaluation = loader.evaluate(observation, loader.load())
        drift = DriftReporter().compute(observation, evaluation)
        self.assertGreaterEqual(drift["K_CMS"], 0.0)
        self.assertLessEqual(drift["K_CMS"], 1.0)

    def test_runtime_cycle(self):
        result = CMSRuntime(ROOT).run_cycle()
        self.assertGreaterEqual(result.k_cms, 0.0)
        self.assertTrue((ROOT / "outputs/evidence/latest_evidence_package.json").exists())


if __name__ == "__main__":
    unittest.main()