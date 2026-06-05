# CMS-SA v0.2b2 — Injection Record

## Injection Name

README Render Hygiene and Badge Status Guard.

## Injection Target

Cybernetic Memory System repository.

## Injection Reason

The screenshot showed stale badges, and README inspection showed corrupted render
tokens. The system needed a validator that checks public readability, not only
anchor presence.

## Injected Surfaces

- `README.md`
- `scripts/validation/validate_readme_render_hygiene_v0_2b2.py`
- `scripts/validation/validate_directory_box_v0_2b.py`
- `scripts/rcc/audit_readme_surface.py`
- `reports/render_hygiene/latest_readme_render_hygiene.md`
- `docs/directory/cms_full_directory_box_v0_2b2.json`
- `docs/versions/v0_2b2/cms_sa_v0_2b2_readme_render_hygiene_badge_guard.md`
- `docs/injections/v0_2b2/cms_sa_v0_2b2_injection_record.md`
- `docs/release_seals/cms_sa_v0_2b2_release_seal.md`

## New Operating Law

```text
Every checkpoint must update badges, public metrics, README render hygiene,
directory box state, and validation reports in the same promotion cycle.
```

## Next Anchor

CMS-SA v0.3 — Feedback Quality and Lifecycle Engine.

## Non-Claim Lock

Render hygiene and badge correctness are not code correctness.