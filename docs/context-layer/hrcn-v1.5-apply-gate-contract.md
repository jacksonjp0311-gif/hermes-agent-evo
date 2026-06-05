# HRCN v1.5 Apply-Gate Contract

- passed: true
- previous validated anchor: HRCN v1.4
- current checkpoint: HRCN v1.5
- next recommended phase: HRCN v1.6 - Limited Apply Executor
- mode: docs/context apply-gate contract
- runtime code changed: false
- dependency files changed: false
- dry-run executor implemented: false
- apply executor implemented: false
- apply executed: false
- authority granted: false

## Primary Law

```text
Apply is a gated human-authorized transition, not an agent decision and not a dry-run result.
```

## Apply Candidate Requirements

```text
passed dry-run result
expected diff manifest
evidence package
rollback plan
validation plan
human authorization record
scoped changed paths
secret scan requirement
clean worktree requirement
rebase-before-apply requirement
```

## Apply Gate Decision Classes

```text
eligible_for_future_limited_apply_executor
needs_more_evidence
needs_rollback_plan
needs_human_authorization
blocked
```

## Current Scope Rule

```text
docs/context-only candidates may become eligible for a future limited apply executor.
runtime, dependency, cms-write, memory-write, and api-write candidates remain blocked.
```

## Non-Claim Lock

HRCN v1.5 defines the Apply-Gate Contract as documentation/context only. It specifies how a future apply candidate must bind a passed dry-run result, evidence package, rollback plan, human authorization record, scoped changed paths, validation plan, and secret scan before any future apply executor may be requested. It does not implement a runtime loader, adapter, dry-run executor, apply executor, benchmark executor, repair executor, CMS writer, memory writer, API writer, live integration, or apply authority. Apply-gate contract presence is not apply permission.
