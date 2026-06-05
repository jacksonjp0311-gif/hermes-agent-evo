# CMS-SA v0.2b1 — Injection Record

## Injection Name

Public Anchor and Directory Table Render Repair.

## Injection Target

Cybernetic Memory System repository.

## Injection Reason

v0.2b added the correct concept but failed validation because the audit required
anchors that had not been inserted, and the directory table did not render as
literal inspectable path rows.

## Injected Surfaces

- `README.md`
- `scripts/rcc/audit_readme_surface.py`
- `scripts/validation/validate_directory_box_v0_2b.py`
- `docs/directory/cms_full_directory_box_v0_2b1.json`
- `docs/versions/v0_2b1/cms_sa_v0_2b1_public_anchor_directory_table_repair.md`
- `docs/injections/v0_2b1/cms_sa_v0_2b1_injection_record.md`
- `docs/release_seals/cms_sa_v0_2b1_release_seal.md`

## New Operating Law

```text
Do not upgrade an audit before the README contains the anchors the audit will require.
```

## Next Anchor

CMS-SA v0.3 — Feedback Quality and Lifecycle Engine.

## Non-Claim Lock

Audit repair is not code correctness.