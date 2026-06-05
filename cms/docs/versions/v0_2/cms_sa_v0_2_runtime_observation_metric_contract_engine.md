# CODEX ΔΦ — CMS-SA v0.2
## Runtime Observation and Metric Contract Engine

### Purpose

CMS-SA v0.2 is the first executable measurement layer for the Cybernetic Memory
System repository.

### What v0.2 Adds

1. Repository observer.
2. File surface inventory.
3. SHA-256 file surface hashing.
4. Role classification for repository files.
5. Metric contract loader.
6. Default metric contracts.
7. Metric evaluation report.
8. Drift report writer.
9. Evidence package writer.
10. v0.2 validation command and tests.

### Runtime Spine

```text
repository -> observation manifest -> metric contracts -> metric evaluation
-> drift report -> evidence package -> validation report
```

### New Commands

```powershell
$env:PYTHONPATH = ".\src"
python -m cms observe --repo .
python -m cms metrics --repo .
python -m cms drift --repo .
python -m cms cycle --repo . --profile CMS-Core
python scripts/validation/validate_runtime_observation_v0_2.py
python -m unittest discover -s tests
```

### Metric Contracts

- required_surface_coverage
- mini_readme_presence
- version_memory_presence
- python_source_presence

### Non-Claim Lock

Metric contracts measure repository surfaces only. They do not prove code
correctness, truth, external validation, AGI, consciousness, or production
readiness.