# CMS Badge / Status / Render Hygiene Rule

## Rule

Every checkpoint must update, in the same commit:

1. README badges.
2. Current Public Metrics.
3. Full Directory Box if any durable surface changed.
4. README render hygiene report.
5. README audit report.
6. Release readiness report.
7. Version registry and next anchor.

## Validator

Run:

    python scripts/validation/validate_readme_render_hygiene_v0_2b2.py

## Non-Claim Lock

Badge/status accuracy and render hygiene improve traceability. They do not prove
code correctness, truth, security, AGI, consciousness, or production readiness.