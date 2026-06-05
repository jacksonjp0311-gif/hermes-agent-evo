# OPS-002 Rollback Plan

Rollback is docs/context-only:

- delete OPS-002 files under docs/context-layer/ops/
- delete OPS-002 generated ledger/report outputs if required
- or revert the OPS-002 commit after push

No runtime, CMS, API, memory, or dependency rollback is required because OPS-002 does not touch those surfaces.
