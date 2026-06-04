# HRCN v0.5 Memory Permission Adapter Design

Status: docs/context design only.

## Primary Law

```text
Memory may surface context; permission determines use; humans authorize action.
```

## Purpose

HRCN v0.5 defines the permission matrix a future adapter must obey before memory or CMS context can influence Hermes proposals.

This is a design boundary, not an implementation.

```text
memory visibility -> permitted use -> proposal boundary -> human authorization
```

## Geometry

| Layer | Meaning |
|---|---|
| visibility | What memory/context can be seen. |
| use | What memory/context may be used for. |
| proposal | What Hermes may suggest. |
| dry-run | What may be simulated in a future phase. |
| apply | What remains blocked until explicit authorization and rollback evidence. |
| authorization | The human-controlled transition boundary. |

## Permission Classes

| Class | Meaning |
|---|---|
| blocked | Cannot be used. |
| visible_only | May be seen for orientation only. |
| context_only | May provide bounded background context. |
| evidence_reference | May be cited internally when provenance and validation tier exist. |
| proposal_allowed | May support a proposal but not dry-run or apply/write. |
| dry_run_candidate | May support future dry-run design only after dry-run phase exists. |
| apply_candidate | May be considered only after apply-gate, rollback, validation, and human authorization exist. |

## Required Record Fields

```text
source
timestamp_utc
record_type
validation_tier
permission_class
claim_boundary
allowed_use
blocked_use
target_surface
human_authorization_requirement
rollback_requirement
```

## Decision Rules

```text
No memory record can upgrade its own permission class.
No memory record can authorize runtime mutation.
No memory record can authorize CMS writes.
No memory record can override repository state.
No unvalidated memory record can be treated as evidence.
No evidence reference can become apply authority without human authorization.
If permission is ambiguous, classify as blocked or visible_only.
```

## v0.5 Blocks

```text
no adapter implementation
no runtime loader
no runtime mutation
no dependency mutation
no CMS import
no CMS writes
no API write authority
no repair apply
```

## Non-Claim Lock

HRCN v0.5 is a docs/context memory-permission adapter design layer. It defines permission classes and gates for future memory use. It does not create a loader, adapter, runtime bridge, CMS folder, memory writer, repair applier, API writer, or live integration. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
