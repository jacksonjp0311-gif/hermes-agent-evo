# CMS-SA v0.3a2 - Pure Geometry Validation Boundary

## Purpose

Separate reflective geometry emission from reflective geometry validation.

## Boundary

A validator must not mutate the geometry it validates.

## Implementation

- `scripts/geometry/emit_reflective_git_geometry.py` writes latest geometry artifacts.
- `scripts/validation/validate_reflective_git_geometry_v0_3.py` reads existing geometry artifacts and validates them without rewriting the geometry field.

## API implication

Future API observe paths must be read-only. Future API propose paths may write only draft/diff/evidence surfaces. Future API write paths require validation, evidence package, and authorization.

## Non-claim lock

This improves repository evidence boundaries and API-readiness only.