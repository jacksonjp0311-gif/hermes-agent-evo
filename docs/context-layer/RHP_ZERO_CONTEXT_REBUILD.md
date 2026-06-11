# RHP Zero-Context Rebuild Packet

- schema: `RHP-ZERO-CONTEXT-REBUILD-v0.7`
- ok: `True`
- latest operation: `RHP-015.0`
- latest evidence: `docs/context-layer/ops/RHP-015-0-final-evidence.json`
- latest commit/base: `49976691ca1cff470cb7bb0bfa72e106c0f5311e`
- next operation: `RHP-015.1 CI green verification + autoheal proposal review`

## Critical lesson
- RHP evidence keys are API surfaces.
- New pointer-aware geometry must preserve legacy boot/alignment keys.
- Local scripts must fail closed on command invocation and parser errors.

Non-claim lock: Zero-context rebuild grants no authority.
