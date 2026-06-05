# HRCN v1.7 Governed Operational Loop

- passed: true
- previous validated anchor: HRCN v1.6
- current checkpoint: HRCN v1.7
- next recommended phase: HRCN v1.8 - Replay and Rollback Hardening
- governed loop controller created: true
- loop tool path: `scripts/hrcn/governed_operational_loop_v1_7.py`
- limited apply executor dependency verified: true
- allowed scope: `README.md`, `docs/context-layer/**`
- self-authorization enabled: false
- automatic apply enabled: false
- apply authority granted: false
- runtime integration created: false
- CMS write authority granted: false
- API write authority granted: false

## Primary Law

```text
A governed operational loop may coordinate gates; it may not bypass them, self-authorize, or widen apply scope.
```

## Loop Sequence

```text
observe -> propose -> classify -> dry-run -> evidence -> authorize -> limited apply -> validate -> ledger
```

## Non-Claim Lock

HRCN v1.7 creates a governed operational loop controller for docs/context operations. The loop coordinates observe, propose, classify, dry-run planning, evidence, authorization, limited apply handoff, validation, and ledger stages. It does not widen v1.6 scope, does not self-authorize, does not mutate Hermes runtime, does not touch cms/, does not change dependencies, does not call APIs, and does not grant autonomous authority.
