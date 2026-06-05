
# CMS-SA v0.3b4 Release Seal

Status: pending final public sync

Required local gates:

```powershell
python scripts/controls/emit_negative_control_harness_v0_3b4.py
python scripts/validation/validate_negative_control_harness_v0_3b4.py
python scripts/rcc/audit_readme_surface.py
python scripts/validation/validate_surface_alignment_v0_3b2.py
python scripts/alignment/emit_multilevel_alignment_v0_3b2.py
python scripts/validation/validate_multilevel_alignment_v0_3b2.py
python -m unittest discover -s tests
python scripts/validate_release.py
```

Non-claim lock: release sealing is repository-bound and does not prove code correctness.
