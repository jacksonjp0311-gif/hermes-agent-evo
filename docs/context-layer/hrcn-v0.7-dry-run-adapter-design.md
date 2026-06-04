# HRCN v0.7 Dry-Run Adapter Design

Status: docs/context design only.

## Primary Law

```text
A dry-run may simulate a change; it may not become the change.
```

## Purpose

HRCN v0.7 defines how future proposals and repair recommendations may be simulated without live mutation.

```text
proposal -> dry-run plan -> sandbox boundary -> expected diff/evidence -> rollback plan -> human authorization
```

## Geometry

| Layer | Meaning |
|---|---|
| proposal | The bounded change idea. |
| dry-run plan | The simulation protocol without live mutation. |
| sandbox boundary | Where the simulation may occur. |
| expected diff | Forecast of what would change. |
| evidence package | Artifacts required to evaluate simulation output. |
| rollback plan | Reversal requirement for any future apply gate. |
| authorization | Human-controlled transition boundary. |

## Dry-Run Classes

| Class | Meaning |
|---|---|
| not_eligible | Proposal cannot enter dry-run design. |
| docs_only_simulation | Simulate documentation/context changes only. |
| test_only_simulation | Simulate tests or validation commands without runtime edits. |
| sandbox_file_simulation | Future disposable sandbox simulation only. |
| runtime_dry_run_candidate | Runtime simulation candidate only; no runtime write in v0.7. |
| blocked_apply_attempt | Any attempt to use dry-run as apply/write authority is blocked. |

## Required Dry-Run Fields

```text
source
timestamp_utc
proposal_id
proposal_summary
target_surface
dry_run_class
sandbox_boundary
expected_diff
expected_evidence
forbidden_side_effects
validation_commands
rollback_plan
human_authorization_requirement
```

## Decision Rules

```text
No dry-run can apply itself.
No dry-run can mutate live runtime, dependencies, CMS, API config, secrets, or package state in v0.7.
No dry-run output can be treated as production validation.
No dry-run evidence can grant apply authority without a later apply gate.
A dry-run plan must define sandbox boundary, expected diff, evidence package, and rollback plan.
If the sandbox boundary is missing, classify as not_eligible.
If an action attempts staging, commit, push, or live mutation, classify as blocked_apply_attempt.
```

## v0.7 Blocks

```text
no adapter implementation
no runtime loader
no dry-run executor
no repair execution
no runtime mutation
no dependency mutation
no CMS import
no CMS writes
no API write authority
no apply authority
```

## Non-Claim Lock

HRCN v0.7 is a docs/context dry-run adapter design layer. It defines simulation boundaries and evidence requirements for future dry-runs. It does not create a loader, adapter, runtime bridge, dry-run executor, CMS folder, memory writer, repair applier, API writer, live integration, or apply authority. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
