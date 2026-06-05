# HRCN v1.9 Operator Dashboard / Command Surface

- passed: true
- previous validated anchor: HRCN v1.8
- current checkpoint: HRCN v1.9
- next recommended phase: HRCN v2.0 - Operational Hermes-CMS Nexus
- operator command surface created: true
- command surface path: `scripts/hrcn/operator_command_surface_v1_9.py`
- status command defined: true
- gate matrix command defined: true
- next commands defined: true
- packet template command defined: true
- allowed scope: `README.md`, `docs/context-layer/**`
- operator can apply: false
- operator can automatically rollback: false
- operator can self-authorize: false
- operator can call APIs: false

## Primary Law

```text
An operator surface may make governed actions visible and selectable; it may not become the operator.
```

## Commands

```text
status
gates
next-commands
make-packet-template
```

## Non-Claim Lock

HRCN v1.9 adds a local operator command surface for governed docs/context operations. It can show status, gate readiness, bounded scope, and generate packet templates for human review. It does not apply changes, does not rollback automatically, does not self-authorize, does not widen v1.6 scope, does not mutate Hermes runtime, does not touch cms/, does not change dependencies, and does not call APIs.
