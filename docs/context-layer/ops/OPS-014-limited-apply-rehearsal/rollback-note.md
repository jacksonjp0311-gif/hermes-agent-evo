# OPS-014 Rollback Note

OPS-014 applies only docs/context evidence and README alignment.

## Rollback scope

- `README.md`
- `docs/context-layer/ops/OPS-014-*`

## Preferred rollback

Use Git revert on the OPS-014 commit only.

```powershell
git log --oneline -5
git revert <OPS-014_COMMIT_SHA>
git push origin main
```

## Hard boundary

Do not rollback or mutate runtime source, CMS runtime files, CMS memory stores, API configuration, dependency files, or environment files through this operation.

## Non-Claim Lock

This rollback note is documentation only. It does not execute rollback or grant runtime/CMS/memory/API/dependency authority.
