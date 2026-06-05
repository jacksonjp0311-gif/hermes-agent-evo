# CMS-SA v0.2b3d - Validator Expectation Alignment

## Purpose

Align README-facing validators with the active public checkpoint and stable public-sync badge semantics.

## Problem

v0.2b3c successfully repaired stable public-sync evidence, but two validators still expected v0.2b3a-era public tokens:

- audit_readme_surface.py expected the old checkpoint token.
- validate_readme_render_hygiene_v0_2b2.py expected the old CMS badge and local public-sync badge.

## Repair

- Update README audit expectation to the active checkpoint.
- Update render hygiene badge expectations.
- Preserve v0.2b3c stable public-sync semantics.
- Record CMS-L-010.

## Lesson

Validators must advance their expected public tokens whenever checkpoint badges and README status advance.

## Non-claim lock

Validator alignment improves repository-state traceability only.