# OPS-009 Rollback Notes

OPS-009 does not execute rollback. It records a rollback path for the evidence/documentation scope.

## Rollback candidate scope

- `README.md`
- `docs/context-layer/ops/**`
- `docs/context-layer/hrcn-v2.0-nexus-reports/**`

## Preferred rollback method

Use Git history and revert the specific OPS commit if a post-commit validation problem is found.

```powershell
git log --oneline -10
git revert <OPS_COMMIT_SHA>
git status --short
```

## Hard boundary

Do not rollback runtime source, dependencies, provider configuration, environment files, CMS runtime files, or memory stores through this OPS-009 pack.

## Non-claim lock

A rollback plan is not rollback execution. Human review is required before any live revert/push.
