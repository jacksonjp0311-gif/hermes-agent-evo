# RHP-004 Repair — Test Contract Alignment

- operation: RHP-004 repair
- previous failure: bridge anchor updated while existing HRCN tests still encoded v0.2 expectations
- repair lesson: RHP-L-005
- bridge anchor after: `docs/context-layer/ops/OPS-027-final-evidence.json`
- HRCN bridge tag after: `hrcn-ops-v0.3.0`
- test contract migrated: true
- POSIX relative evidence path normalized: true
- py_compile passed: true
- focused tests passed: true
- direct anchor alignment smoke passed: true
- failed tests are commit blockers: true
- next: RHP-005 generated-source compile-check guard

## RHP-L-005

Rehydration is orientation, not implementation coercion. Version-anchor changes must preserve or deliberately migrate existing test contracts before commit.

## Boundary

RHP-004 repair aligns a read-only evidence anchor and its test contract only. It does not execute CMS, write CMS, write memory, write APIs, change dependencies, call a provider/model, grant tool authority, operate autonomously, or self-authorize.
