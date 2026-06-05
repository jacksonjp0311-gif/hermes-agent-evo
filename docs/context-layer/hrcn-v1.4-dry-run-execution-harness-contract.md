# HRCN v1.4 Dry-Run Execution Harness Contract

- passed: true
- previous validated anchor: HRCN v1.3
- current checkpoint: HRCN v1.4
- next recommended phase: HRCN v1.5 - Apply-Gate Contract
- mode: docs/context harness contract
- runtime code changed: false
- dependency files changed: false
- dry-run executor implemented: false
- apply executor implemented: false
- authority granted: false

## Primary Law

```text
A dry-run harness may simulate and score a proposed change; it may not apply the change, mutate runtime, or grant authority.
```

## Harness Inputs

```text
docs/context-layer/hrcn-v1.2-permission-bridge-dry-run-design.json
docs/context-layer/hrcn-v1.3-cms-hermes-read-only-bridge-prototype.json
docs/context-layer/hrcn-v1.1-bounded-cms-context-packet.json
```

## Dry-Run Request Contract

```text
dry_run_request_id
proposal_id
decision_class
requested_surface
requested_authority
target_paths
expected_change_summary
evidence_refs
cms_read_refs
rollback_plan_ref
human_authorization_ref
```

## Sandbox Plan Contract

```text
sandbox_mode
allowed_write_scope: []
blocked_write_scope
filesystem_mutation_allowed: false
git_stage_allowed: false
git_commit_allowed: false
git_push_allowed: false
```

## Dry-Run Result Contract

```text
simulated: true
applied: false
runtime_mutated: false
cms_mutated: false
memory_mutated: false
api_called: false
git_committed: false
git_pushed: false
authority_granted: false
```

## Non-Claim Lock

HRCN v1.4 defines the Dry-Run Execution Harness Contract as documentation/context only. It specifies how a future harness would receive a classified proposal, create a sandbox plan, compute an expected diff, bind evidence and rollback requirements, and emit a dry-run result with applied=false. It does not implement a runtime loader, adapter, dry-run executor, apply executor, benchmark executor, repair executor, CMS writer, memory writer, API writer, live integration, or apply authority. Dry-run contract presence is not dry-run execution authority.
