from pathlib import Path
import json
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
required = [
    "src/cms/observation/repository_observer.py",
    "src/cms/metrics/metric_contracts.py",
    "src/cms/comparator/drift_reporter.py",
    "src/cms/evidence/package_writer.py",
    "configs/metrics/cms_metric_contracts_v0_2.json",
    "outputs/evidence/latest_evidence_package.json",
    "reports/runtime_observation/latest_observation_manifest.md",
    "reports/metric_contracts/latest_metric_evaluation.md",
    "reports/drift/latest_drift_report.md",
    "reports/evidence/latest_evidence_package.md",
]

missing = [p for p in required if not (ROOT / p).exists()]

compile_checks = [
    "src/cms/core/runtime.py",
    "src/cms/cli.py",
    "src/cms/observation/repository_observer.py",
    "src/cms/metrics/metric_contracts.py",
    "src/cms/comparator/drift_reporter.py",
    "src/cms/evidence/package_writer.py",
]

compile_failures = []
for rel in compile_checks:
    proc = subprocess.run([sys.executable, "-m", "py_compile", str(ROOT / rel)], cwd=ROOT)
    if proc.returncode != 0:
        compile_failures.append(rel)

passed = not missing and not compile_failures
report = {
    "schema": "CMS-SA-v0.2-runtime-observation-validation",
    "passed": passed,
    "missing": missing,
    "compile_failures": compile_failures,
    "non_claim_lock": "runtime validation is repository-bound and does not prove correctness"
}

out_json = ROOT / "reports" / "release" / "latest_v0_2_runtime_observation_validation.json"
out_md = ROOT / "reports" / "release" / "latest_v0_2_runtime_observation_validation.md"
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=2), encoding="utf-8")
out_md.write_text(
    "# CMS-SA v0.2 Runtime Observation Validation\n\n"
    f"- passed: `{passed}`\n"
    f"- missing: `{missing}`\n"
    f"- compile_failures: `{compile_failures}`\n\n"
    "Non-claim lock: runtime validation is repository-bound and does not prove correctness.\n",
    encoding="utf-8",
)

print(json.dumps(report, indent=2))
raise SystemExit(0 if passed else 1)