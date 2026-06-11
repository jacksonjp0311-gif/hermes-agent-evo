# RHP Zero-Context Rebuild Packet

- schema: `RHP-ZERO-CONTEXT-REBUILD-v0.6`
- ok: `True`
- latest operation: `RHP-014.9`
- latest evidence: `docs/context-layer/ops/RHP-014-9-final-evidence.json`
- latest commit/base: `c4a9d75f658a6d029e9ee9e1b68c05bebfeb8132`
- next operation: `RHP-015.0 Autoheal proposal evaluator + CI log ingestion`

## New operator grammar
- `RHPLOAD` command boxes include `heading`, `command`, and `why` fields.
- `RHPDIAG` boxes classify runtime failures and point to raw artifacts.
- Autoheal remains dry-run only until a later gate explicitly enables execution.

Non-claim lock: Zero-context rebuild grants no authority.
