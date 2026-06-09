# RHP-011 Operator-Visible Startup Lock Sequence

RHP-011 proves that Hermes displays the human-visible rehydration lock sequence before interaction.

## Visible sequence

```text
RHP rehydration sequence:
[OK] repo root found
[OK] RHP-010 evidence green
[OK] HRCN boundary green
[OK] alignment guard green
[OK] startup packet created
[OK] authority=false
[OK] external_ingestion=false
[OK] provider/model/tool execution=false
[OK] CMS/memory/API write=false
RHP rehydration complete: ok | phase=pre-interaction | evidence=RHP-010
RHP authority boundary: provider/model/tool=false | CMS/memory/API=false | external_ingestion=false | autonomy=false
```

## Boundary

RHP-011 is visual/operator status only. It grants no provider/model/tool authority, no CMS write, no memory promotion, no API write, no external ingestion, no autonomy, and no self-authorization.