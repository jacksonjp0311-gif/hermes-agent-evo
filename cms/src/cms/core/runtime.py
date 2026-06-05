from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from cms.observation.repository_observer import RepositoryObserver
from cms.metrics.metric_contracts import MetricContractLoader
from cms.comparator.drift_reporter import DriftReporter
from cms.evidence.package_writer import EvidencePackageWriter


@dataclass
class CMSRunResult:
    repository: str
    profile: str
    k_cms: float
    d_cms: float
    release_allowed: bool
    classification: str
    file_count: int
    findings: int
    artifacts: str


class CMSRuntime:
    """CMS-SA v0.2 runtime observation + metric contract engine."""

    def __init__(self, repo: str | Path = ".", profile: str = "CMS-Core") -> None:
        self.repo = Path(repo).resolve()
        self.profile = profile

    def observe_repository(self) -> dict[str, Any]:
        return RepositoryObserver(self.repo).observe()

    def run_cycle(self) -> CMSRunResult:
        observation = self.observe_repository()
        loader = MetricContractLoader(self.repo)
        contracts = loader.load()
        metric_eval = loader.evaluate(observation, contracts)
        drift = DriftReporter().compute(observation, metric_eval)
        evidence = EvidencePackageWriter(self.repo).write(observation, metric_eval, drift)

        return CMSRunResult(
            repository=self.repo.name,
            profile=self.profile,
            k_cms=float(drift["K_CMS"]),
            d_cms=float(drift["D_CMS"]),
            release_allowed=bool(evidence["classification"]["release_allowed"]),
            classification=evidence["classification"]["class"],
            file_count=int(observation.get("file_count", 0)),
            findings=len(metric_eval.get("findings", [])),
            artifacts=str((self.repo / "outputs").resolve()),
        )

    def run(self) -> CMSRunResult:
        return self.run_cycle()