
# CMS-SA v0.3b5 Release Seal

Status: pending final public sync

Required local gates:

```powershell
python scripts/memory/emit_memory_promotion_v0_3b5.py
python scripts/validation/validate_memory_promotion_v0_3b5.py
python scripts/rcc/audit_readme_surface.py
python scripts/validation/validate_readme_render_hygiene_v0_2b2.py
python scripts/validation/validate_markdown_structure_v0_2b3.py
python scripts/validation/validate_surface_alignment_v0_3b2.py
python scripts/alignment/emit_multilevel_alignment_v0_3b2.py
python scripts/validation/validate_multilevel_alignment_v0_3b2.py
python -m unittest discover -s tests
python scripts/validate_release.py
```

Non-claim lock: release sealing is repository-bound and does not prove code correctness.
