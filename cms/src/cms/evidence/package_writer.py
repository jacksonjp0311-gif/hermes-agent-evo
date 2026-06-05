from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def write_md(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class EvidencePackageWriter:
    def __init__(self, repo: str | Path) -> None:
        self.repo = Path(repo).resolve()
        self.outputs = self.repo / "outputs"
        self.reports = self.repo / "reports"

    def write(self, observation: dict[str, Any], metric_eval: dict[str, Any], drift: dict[str, Any]) -> dict[str, Any]:
        package = {
            "schema": "CMS-SA-v0.2-evidence-package",
            "repository": self.repo.name,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "observation": {
                "file_count": observation.get("file_count"),
                "role_counts": observation.get("role_counts"),
                "suffix_counts": observation.get("suffix_counts"),
                "required_surfaces": observation.get("required_surfaces"),
            },
            "metric_evaluation": metric_eval,
            "drift_report": drift,
            "classification": {
                "class": "CMS-B" if metric_eval.get("passed") else "CMS-C",
                "release_allowed": bool(metric_eval.get("passed")),
                "boundary": "repository-bound local measurement only",
            },
            "non_claim_locks": {
                "measurement_is_not_truth": True,
                "navigation_is_not_validation": True,
                "metric_pass_is_not_code_correctness": True,
                "evidence_package_is_not_external_validation": True,
            },
        }

        write_json(self.outputs / "state" / "latest_observation_manifest.json", observation)
        write_json(self.outputs / "metrics" / "latest_metric_evaluation.json", metric_eval)
        write_json(self.outputs / "drift" / "latest_drift_report.json", drift)
        write_json(self.outputs / "evidence" / "latest_evidence_package.json", package)

        write_json(self.reports / "runtime_observation" / "latest_observation_manifest.json", observation)
        write_json(self.reports / "metric_contracts" / "latest_metric_evaluation.json", metric_eval)
        write_json(self.reports / "drift" / "latest_drift_report.json", drift)
        write_json(self.reports / "evidence" / "latest_evidence_package.json", package)

        write_md(
            self.reports / "runtime_observation" / "latest_observation_manifest.md",
            "# CMS-SA v0.2 Observation Manifest\n\n"
            f"- repository: `{self.repo.name}`\n"
            f"- file_count: `{observation.get('file_count')}`\n"
            f"- git_head: `{observation.get('git_head')}`\n\n"
            "Non-claim lock: repository observation is not code correctness.\n",
        )
        write_md(
            self.reports / "metric_contracts" / "latest_metric_evaluation.md",
            "# CMS-SA v0.2 Metric Evaluation\n\n"
            f"- passed: `{metric_eval.get('passed')}`\n"
            f"- findings: `{len(metric_eval.get('findings', []))}`\n"
            f"- metrics: `{metric_eval.get('metrics')}`\n\n"
            "Non-claim lock: metric pass is not code correctness.\n",
        )
        write_md(
            self.reports / "drift" / "latest_drift_report.md",
            "# CMS-SA v0.2 Drift Report\n\n"
            f"- D_CMS: `{drift.get('D_CMS')}`\n"
            f"- K_CMS: `{drift.get('K_CMS')}`\n"
            f"- findings: `{len(drift.get('findings', []))}`\n\n"
            "Non-claim lock: low drift is not truth.\n",
        )
        write_md(
            self.reports / "evidence" / "latest_evidence_package.md",
            "# CMS-SA v0.2 Evidence Package\n\n"
            f"- classification: `{package['classification']['class']}`\n"
            f"- release_allowed: `{package['classification']['release_allowed']}`\n"
            "- boundary: `repository-bound local measurement only`\n\n"
            "Non-claim lock: evidence package is not external validation.\n",
        )
        return package