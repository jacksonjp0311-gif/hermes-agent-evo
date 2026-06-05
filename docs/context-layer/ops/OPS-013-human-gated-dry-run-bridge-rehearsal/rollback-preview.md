# OPS-013 Rollback Preview

OPS-013 does not apply the proposed OPS-014 changes. Therefore there is no runtime rollback to execute.

## If OPS-013 documentation needs to be reverted

Use Git revert on the OPS-013 commit only.

```powershell
git log --oneline -5
git revert <OPS-013_COMMIT_SHA>
git push origin main
```

## Hard boundary

Do not revert runtime source, CMS runtime files, memory stores, API configuration, dependency files, or environment files through this preview.

## Non-claim lock

A rollback preview is not rollback execution. Human review is required before any revert.
