# RHP Zero-Context Rebuild Packet

- schema: `RHP-ZERO-CONTEXT-REBUILD-v1.7`
- ok: `True`
- latest operation: `RHP-016.0`
- latest evidence: `docs/context-layer/ops/RHP-016-0-final-evidence.json`
- operation base commit: `1fb6a62f178f7a9cf112fc44e939c2e8290a1451`
- observed previous sealed commit: `1fb6a62f178f7a9cf112fc44e939c2e8290a1451`
- green reconciled subject commit: `1fb6a62f178f7a9cf112fc44e939c2e8290a1451`
- green reconciled subject CI status: `green`
- green reconciled subject integration closed: `True`
- green reconciled subject state: `RECONCILED`
- current operation commit: `unobservable-from-inside-same-commit`
- current operation remote CI status: `unknown_until_next_observation`
- next operation: `RHP-016.1 Current commit CI observation and doctor CLI wrapper`

## Green reconciliation law

- Green CI claims must name a subject commit.
- Integration closure applies to the subject commit only.
- A new reconciliation commit cannot claim its own remote CI state from inside itself.

Non-claim lock: Zero-context rebuild grants no authority.
