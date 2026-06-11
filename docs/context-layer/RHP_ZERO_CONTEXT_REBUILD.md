# RHP Zero-Context Rebuild Packet

- schema: `RHP-ZERO-CONTEXT-REBUILD-v1.2`
- ok: `True`
- latest operation: `RHP-015.5`
- latest evidence: `docs/context-layer/ops/RHP-015-5-final-evidence.json`
- operation base commit: `fe7c310e1cebb32e0b3b497231ed87cb254be992`
- observed previous sealed commit: `fe7c310e1cebb32e0b3b497231ed87cb254be992`
- current operation commit: `unobservable-from-inside-same-commit`
- remote CI status: `green`
- integration closed: `True`
- wait state: `False`
- next operation: `RHP-015.6 Evidence API compatibility gate and replay scaffold`

## Render hygiene law

- Text surfaces must contain real line breaks.
- Literal `\n` escape drift in README/context surfaces is a render wound.
- Final JSON summaries should be closed behind `RHPDROP [closed]`; full JSON belongs in evidence files or raw indexes.

## Green seal law

- Integration closure requires local validation and verified remote CI green.
- Pending or unknown CI means wait-state, not green-seal closure.

Non-claim lock: Zero-context rebuild grants no authority.
