# HRCN v1.8 Replay and Rollback Hardening

- passed: true
- previous validated anchor: HRCN v1.7
- current checkpoint: HRCN v1.8
- next recommended phase: HRCN v1.9 - Operator Dashboard / Command Surface
- replay/rollback hardening created: true
- hardening tool path: `scripts/hrcn/replay_rollback_hardening_v1_8.py`
- governed loop dependency verified: true
- limited apply executor dependency verified: true
- allowed scope: `README.md`, `docs/context-layer/**`
- automatic rollback enabled: false
- self-authorization enabled: false
- apply authority granted: false
- runtime integration created: false
- CMS write authority granted: false
- API write authority granted: false

## Primary Law

```text
A governed operation is not operationally safe until it can be replayed, audited, and rolled back within its authorized scope.
```

## Required Replay/Rollback Checks

```text
expected base commit
operation before/after hashes
all paths inside scope
limited apply audit reference
rollback packet reference
post-apply validation reference
automatic rollback disabled
self-authorization disabled
```

## Non-Claim Lock

HRCN v1.8 adds replay and rollback hardening for the governed docs/context loop. It defines how ledger entries, limited-apply audits, expected base commits, operation hashes, rollback packets, and replay manifests are checked before an operation is trusted. It does not perform automatic rollback, does not self-authorize, does not widen v1.6 scope, does not mutate Hermes runtime, does not touch cms/, does not change dependencies, and does not call APIs.
