from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json
from typing import Any


@dataclass
class MetricContract:
    name: str
    surface: str
    scale: str
    threshold: float | None
    decision_use: str
    non_claim_boundary: str


DEFAULT_CONTRACTS = [
    MetricContract(
        name="required_surface_coverage",
        surface="repository.required_surfaces",
        scale="[0,1]",
        threshold=1.0,
        decision_use="block_if_below_threshold",
        non_claim_boundary="surface coverage is not code correctness",
    ),
    MetricContract(
        name="mini_readme_presence",
        surface="repository.readme_surfaces",
        scale="[0,1]",
        threshold=1.0,
        decision_use="warn_or_block_navigation_drift",
        non_claim_boundary="navigation is not validation",
    ),
    MetricContract(
        name="version_memory_presence",
        surface="repository.version_memory",
        scale="[0,1]",
        threshold=1.0,
        decision_use="block_if_missing_version_trace",
        non_claim_boundary="version registry is not truth",
    ),
    MetricContract(
        name="python_source_presence",
        surface="repository.python_source",
        scale="[0,1]",
        threshold=0.01,
        decision_use="inform_runtime_scaffold",
        non_claim_boundary="source presence is not runtime correctness",
    ),
]


class MetricContractLoader:
    """Loads and evaluates CMS metric contracts."""

    def __init__(self, repo: str | Path) -> None:
        self.repo = Path(repo).resolve()

    def write_default_contracts(self, path: Path) -> list[dict[str, Any]]:
        payload = {
            "schema": "CMS-SA-v0.2-metric-contract-set",
            "contracts": [asdict(c) for c in DEFAULT_CONTRACTS],
            "non_claim_lock": "metric contracts declare measurement surfaces only",
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return payload["contracts"]

    def load(self, path: str | Path | None = None) -> list[dict[str, Any]]:
        if path is None:
            contract_path = self.repo / "configs" / "metrics" / "cms_metric_contracts_v0_2.json"
        else:
            contract_path = Path(path)

        if not contract_path.exists():
            return self.write_default_contracts(contract_path)

        data = json.loads(contract_path.read_text(encoding="utf-8"))
        return data.get("contracts", [])

    def evaluate(self, observation: dict[str, Any], contracts: list[dict[str, Any]]) -> dict[str, Any]:
        required = observation.get("required_surfaces", {})
        required_coverage = sum(1 for v in required.values() if v) / max(1, len(required))

        mini_readmes = [
            s for s in observation.get("surfaces", [])
            if s.get("path", "").endswith("README.md")
        ]
        major_dirs = [
            "docs", "docs/context", "docs/architecture", "docs/protocols", "docs/theory",
            "docs/versions", "docs/injections", "docs/release_seals", "docs/roadmap",
            "rcc", "rcc/nexus", "src", "src/cms", "src/cms/core", "src/cms/observation",
            "src/cms/metrics", "src/cms/comparator", "src/cms/feedback", "src/cms/planning",
            "src/cms/validation", "src/cms/memory", "src/cms/correction", "src/cms/evidence",
            "src/cms/schemas", "src/cms/artifacts", "src/cms/utils", "configs", "examples",
            "scripts", "tests", "outputs", "reports",
        ]
        mini_paths = {s.get("path") for s in mini_readmes}
        mini_expected = {f"{d}/README.md" for d in major_dirs}
        mini_expected.add("README.md")
        mini_coverage = len(mini_paths & mini_expected) / max(1, len(mini_expected))

        version_memory_paths = [
            "outputs/version_registry/cms_version_registry.json",
            "outputs/lineage/cms_lineage_ledger.jsonl",
            "outputs/injections/cms_injection_ledger.jsonl",
        ]
        version_memory_presence = sum(1 for p in version_memory_paths if (self.repo / p).exists()) / len(version_memory_paths)

        py_count = observation.get("role_counts", {}).get("python_source", 0)
        file_count = max(1, observation.get("file_count", 1))
        python_source_presence = py_count / file_count

        metrics = {
            "required_surface_coverage": required_coverage,
            "mini_readme_presence": mini_coverage,
            "version_memory_presence": version_memory_presence,
            "python_source_presence": python_source_presence,
        }

        findings = []
        for contract in contracts:
            name = contract["name"]
            threshold = contract.get("threshold")
            value = metrics.get(name)
            passed = True if threshold is None else value >= threshold
            if not passed:
                findings.append({
                    "metric": name,
                    "value": value,
                    "threshold": threshold,
                    "decision_use": contract.get("decision_use"),
                    "non_claim_boundary": contract.get("non_claim_boundary"),
                })

        return {
            "schema": "CMS-SA-v0.2-metric-evaluation",
            "metrics": metrics,
            "contracts": contracts,
            "findings": findings,
            "passed": len(findings) == 0,
            "non_claim_lock": "metric pass is not code correctness",
        }