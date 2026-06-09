# RHP-012.1 CLI Visible Rehydration Text Alignment

RHP-012.1 repairs the live Hermes CLI surface after RHP-012.

## Observed issue

Hermes displayed green RHP startup locks, but the operator-visible line still said:

```text
RHP rehydration complete: ok | phase=pre-interaction | evidence=RHP-010
```

The compact CLI banner also did not show the Rehydration Protocol strip.

## Fix

- Runtime operator status now uses `evidence=RHP-012`.
- The boot preflight packet marker is `RHP-BOOT-PREFLIGHT-PACKET-v0.3`.
- The CLI stream receives:
  - `HERMES_RHP_PROTOCOL_STRIP`
  - `HERMES_RHP_PROTOCOL_LOCKS`
- Banner helper now reports `evidence=RHP-012` and recognizes `degraded`.

Boundary: visible display/text alignment only. No provider call, model call, tool call, CMS write, memory promotion, API write, external ingestion, autonomy, or self-authorization.