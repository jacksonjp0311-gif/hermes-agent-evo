# OPS-002 Rollback Plan

Rollback is docs/context-only.

Options:

1. Delete OPS-002 and OPS-002.1 files under docs/context-layer/ops/.
2. Delete generated OPS-002.1 ledger/report files if needed.
3. Revert the OPS-002.1 commit after push.

No runtime, CMS, API, memory, or dependency rollback is required because OPS-002.1 does not touch those surfaces.