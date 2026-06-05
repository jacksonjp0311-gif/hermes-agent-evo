# AGENTS.md — CMS AI Operating Contract

## Read Order

Before editing:

1. README.md
2. README_90_SECONDS.md
3. AGENTS.md
4. rcc/nexus/route_map.json
5. rcc/nexus/task_routing_matrix.md
6. docs/architecture/cms_sa_v0_1_software_architecture.tex
7. target folder README.md
8. relevant source and tests

## Patch Rules

- Do not weaken non-claim locks.
- Do not claim AGI, consciousness, truth, or code correctness.
- Do not promote memory without control utility.
- Do not release if README/RCC/public surfaces are stale.
- Every code patch must run compile/import/tests.
- Every architecture patch must update README/RCC surfaces if meaning changes.

## Validation

```powershell
$env:PYTHONPATH = ".\src"
python -m py_compile src/cms/core/runtime.py
python -c "from cms.core.runtime import CMSRuntime; print('CMSRuntime import OK')"
python scripts/validate_release.py
python -m unittest discover -s tests
```

## Thread Rehydration Protocol

Before proposing a new version in a fresh thread, scan:

1. Origin theory.
2. Software architecture.
3. Runtime state.

Core rule: theory tells why; architecture tells how; runtime tells now.

No fresh-thread versioning without Origin Scan, Architecture Scan, and Runtime State Scan.
