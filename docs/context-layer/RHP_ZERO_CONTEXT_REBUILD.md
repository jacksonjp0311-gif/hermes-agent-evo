# RHP Zero-Context Rebuild Packet

- schema: `RHP-ZERO-CONTEXT-REBUILD-v1.3`
- ok: `True`
- latest operation: `RHP-015.6`
- latest evidence: `docs/context-layer/ops/RHP-015-6-final-evidence.json`
- operation base commit: `2c5b2b62e041ac8972110becb5a14085c1c1a080`
- observed previous sealed commit: `2c5b2b62e041ac8972110becb5a14085c1c1a080`
- previous CI subject commit: `fe7c310e1cebb32e0b3b497231ed87cb254be992`
- previous CI status: `green`
- current head commit at operation start: `2c5b2b62e041ac8972110becb5a14085c1c1a080`
- current head CI status: `pending`
- current head integration closed: `False`
- current operation commit: `unobservable-from-inside-same-commit`
- next operation: `RHP-015.7 RHP doctor cockpit and explicit state machine`

## Claim accounting law

- Every claim must name its subject, source, observation time, status, and authority flag.
- Remote CI status must always name which commit it describes.
- Previous green does not automatically imply current HEAD green.
- Evidence fields are public API unless marked private/deprecated.

Non-claim lock: Zero-context rebuild grants no authority.
