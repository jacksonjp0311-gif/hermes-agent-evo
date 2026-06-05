# CMS-SA v0.4.6 Authorized Repair Apply Gate and Rollback Ledger

| Field | Value |
|---|---|
| passed | `true` |
| source pressure state | `stable` |
| source dry-run count | `1` |
| apply gate count | `1` |
| rollback ledger count | `1` |
| target writes performed | `0` |
| api writes performed | `0` |
| git commits performed | `0` |
| git pushes performed | `0` |
| release tags created | `0` |
| apply gate hash | `eaccd18fa45a9e553acb0d668bfca4a67c952bececc0c0c25ba79f91e55a0df0` |

## Primary Lock

No repair apply may execute unless it references a validated dry-run id, carries explicit human authorization, declares exact target writes, includes rollback entries for every target, preserves blocked actions, and passes the required validation stack before and after apply.

## Gates

### CMS-APPLY-GATE-6319f003ce

- source dry-run: `CMS-DRYRUN-c78d107b05`
- repair class: `REGISTRY_REPAIR`
- gate state: `blocked_pending_explicit_human_authorization`
- apply authority: `false`
- human authorization present: `false`
- rollback required: `true`
- rollback ready: `false`
- touched surfaces: `outputs/version_registry/cms_version_registry.json, outputs/roadmap/next_anchor.md, reports/public_sync`
- pre-apply validation: `validate_surface_alignment, emit_multilevel_alignment, validate_multilevel_alignment, validate_public_sync`

## Non-Claim Lock

Authorized repair apply gates are repository-bound authorization ledgers and do not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, autonomous repair authority, or real-world correctness.

