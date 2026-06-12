# RHP Zero-Context Rebuild Packet

- schema: `RHP-ZERO-CONTEXT-REBUILD-v2.2`
- ok: `True`
- latest operation: `RHP-018.15`
- latest evidence: `docs/context-layer/ops/RHP-018-15-final-evidence.json`
- subject commit: `ddb24363e2fac630e7527a2c9eab31e6df50db52`
- observed CI status: `red`
- prior blocking state: `LOOP_GEOMETRY_ALIGNMENT_GUARD_ALIGNED_SUBJECT_UNRESOLVED`
- state: `ZERO_CONTEXT_AI_BOOTSTRAP_CONTRACT_ALIGNED_SUBJECT_UNRESOLVED`
- integration closed: `False`
- next operation: `operator_rerun_or_ingest_replacement_ci_before_repair`

## Zero-context source order

```text
README.md
AGENTS.md
docs/context-layer/latest-rhp.json
latest_evidence named by latest-rhp.json
docs/context-layer/RHP_ZERO_CONTEXT_REBUILD.md
docs/context-layer/hermes-operator-context.json
rhp/loop_geometry.py
```

Non-claim lock: Zero-context rebuild grants no authority.
