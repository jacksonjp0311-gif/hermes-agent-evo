# HRCN v1.8 Validation

- passed: true
- checkpoint: Replay and Rollback Hardening
- previous validated anchor: HRCN v1.7
- replay rollback hardening created: true
- replay rollback tool path: `scripts/hrcn/replay_rollback_hardening_v1_8.py`
- governed loop dependency verified: true
- limited apply executor dependency verified: true
- manifest schema defined: true
- replay report schema defined: true
- rollback packet requirement defined: true
- operation hash requirement defined: true
- allowed scope: `README.md`, `docs/context-layer/**`
- automatic rollback enabled: false
- self-authorization enabled: false
- runtime code changes allowed: false
- dependency changes allowed: false
- CMS write authority granted: false
- memory write authority granted: false
- API write authority granted: false
- apply authority granted: false
- apply executed: false
- live runtime integration created: false
- autonomous authority granted: false
- roadmap current: HRCN v1.8
- roadmap next: HRCN v1.9

## Primary Law

```text
A governed operation is not operationally safe until it can be replayed, audited, and rolled back within its authorized scope.
```

## Non-Claim Lock

HRCN v1.8 adds replay and rollback hardening for the governed docs/context loop. It defines how ledger entries, limited-apply audits, expected base commits, operation hashes, rollback packets, and replay manifests are checked before an operation is trusted. It does not perform automatic rollback, does not self-authorize, does not widen v1.6 scope, does not mutate Hermes runtime, does not touch cms/, does not change dependencies, and does not call APIs.
