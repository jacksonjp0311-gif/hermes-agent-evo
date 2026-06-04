# HRCN v0.1.2 Lesson Injection Validation

- passed: `true`
- docs only: `true`
- lesson count: `10`
- runtime blocked paths detected: `[]`
- excluded local artifacts: `['package-lock.json', 'assets/hermes_caduceus_icon.ico']`
- package-lock policy: `excluded_unless_explicitly_authorized`
- icon policy: `excluded_unless_explicitly_authorized`

## Injected Lessons

- `HRCN-L-004` — Evidence-level lessons must become public surface memory.
- `HRCN-L-005` — Final verifier residue must be committed or discarded.
- `HRCN-L-006` — Agent proposal is not authority.
- `HRCN-L-007` — Read-only context is not runtime integration.
- `HRCN-L-008` — Dry-run is not write authority.
- `HRCN-L-009` — Apply gate, apply packet, and dry-apply sandbox are not live authority.
- `HRCN-L-010` — Validation order is part of system geometry.
- `HRCN-L-011` — Registry/history must not lag current checkpoint.
- `HRCN-L-012` — File-run scripts prevent interactive paste drift.
- `HRCN-L-013` — Profile adoption is not validation.

## Boundary Repair

The original v0.1.2 validation treated `package-lock.json` as a runtime blocker even though the staging boundary excluded it from the docs commit. This repair records `package-lock.json` and the optional icon as excluded local artifacts, not HRCN runtime mutations.

## Non-Claim Lock

HRCN v0.1.2 validation boundary repair is docs/context/navigation evidence hygiene. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
