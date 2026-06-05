# CMS Validation Surface

## Required Local Validation

```powershell
$env:PYTHONPATH = ".\src"
python scripts/rcc/audit_readme_surface.py
python scripts/rcc/check_rcc_nexus.py
python scripts/validation/validate_architecture_contracts.py
python scripts/validation/validate_runtime_observation_v0_2.py
python scripts/validation/validate_directory_box_v0_2b.py
python scripts/validation/validate_readme_render_hygiene_v0_2b2.py
python scripts/validation/validate_markdown_structure_v0_2b3.py
python scripts/validation/validate_public_sync_v0_2b3.py
python -m cms cycle --repo . --profile CMS-Core
python -m unittest discover -s tests
python scripts/validate_release.py
```

## Boundary

This validation surface is repository-bound. It does not prove code correctness,
truth, AGI, consciousness, production readiness, external validation, security,
or real-world correctness.