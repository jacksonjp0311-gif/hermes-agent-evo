from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from cms.core.runtime import CMSRuntime
from cms.observation.repository_observer import RepositoryObserver
from cms.metrics.metric_contracts import MetricContractLoader
from cms.comparator.drift_reporter import DriftReporter


def main() -> None:
    parser = argparse.ArgumentParser(prog="cms", description="Cybernetic Memory System CLI")
    sub = parser.add_subparsers(dest="command")

    cycle = sub.add_parser("cycle", help="Run the CMS v0.2 observation/metric/drift/evidence cycle")
    cycle.add_argument("--repo", default=".")
    cycle.add_argument("--profile", default="CMS-Core")

    observe = sub.add_parser("observe", help="Observe repository state")
    observe.add_argument("--repo", default=".")

    metrics = sub.add_parser("metrics", help="Load/evaluate metric contracts")
    metrics.add_argument("--repo", default=".")

    drift_cmd = sub.add_parser("drift", help="Compute drift from current observation and metrics")
    drift_cmd.add_argument("--repo", default=".")

    args = parser.parse_args()

    if args.command == "cycle":
        result = CMSRuntime(args.repo, args.profile).run_cycle()
        print(json.dumps(asdict(result), indent=2, ensure_ascii=False))
        return

    if args.command == "observe":
        payload = RepositoryObserver(args.repo).observe()
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if args.command == "metrics":
        repo = Path(args.repo)
        observation = RepositoryObserver(repo).observe()
        loader = MetricContractLoader(repo)
        payload = loader.evaluate(observation, loader.load())
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    if args.command == "drift":
        repo = Path(args.repo)
        observation = RepositoryObserver(repo).observe()
        loader = MetricContractLoader(repo)
        metric_eval = loader.evaluate(observation, loader.load())
        payload = DriftReporter().compute(observation, metric_eval)
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    parser.print_help()


if __name__ == "__main__":
    main()