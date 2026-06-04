# HRCN v0.8 Apply-Gate Adapter Design

Status: docs/context design only.

## Primary Law

```text
Apply is a gated transition, not an agent decision.
```

## Purpose

HRCN v0.8 defines the gate required before any future write/apply transition can be requested.

```text
apply request -> authority classification -> human authorization -> rollback plan -> validation plan -> evidence package -> staged scope -> future apply phase
```

## Geometry

| Layer | Meaning |
|---|---|
| apply request | The proposed write/apply transition. |
| authority classification | Risk and surface classification for the request. |
| human authorization | Explicit authorization by the human operator. |
| rollback plan | Reversal path if apply fails or is rejected. |
| validation plan | Commands/checks required before and after apply. |
| evidence package | Artifacts required to evaluate the transition. |
| staged scope | Exact paths/surfaces allowed for a future apply attempt. |
| live apply | Still blocked in v0.8. |

## Apply-Gate Classes

| Class | Meaning |
|---|---|
| not_allowed | Request cannot enter apply-gate review. |
| docs_apply_candidate | Future docs/context apply candidate only. |
| test_apply_candidate | Future test/validation apply candidate only. |
| runtime_apply_candidate | Future runtime apply candidate; blocked from execution in v0.8. |
| dependency_apply_candidate | Future dependency/package apply candidate; blocked from execution in v0.8. |
| cms_apply_candidate | Future CMS/memory apply candidate; blocked from execution in v0.8. |
| blocked_live_apply | Any live apply/write attempt during v0.8 is blocked. |

## Required Apply-Gate Fields

```text
source
timestamp_utc
apply_request_id
proposal_reference
dry_run_reference
target_surface
authority_classification
allowed_paths
blocked_paths
expected_diff
evidence_package
validation_plan
rollback_plan
human_authorization_record
post_apply_audit_plan
```

## Decision Rules

```text
No apply request can authorize itself.
No apply request can mutate live runtime, dependencies, CMS, API config, secrets, package state, or docs in v0.8.
No dry-run output can become apply authority by itself.
No memory record can grant apply authority.
Human authorization must be explicit, scoped, and tied to an apply_request_id.
Rollback plan and validation plan are required before any future apply transition can be considered.
If target surface or allowed_paths are ambiguous, classify as not_allowed.
If a request attempts staging, commit, push, or live mutation in v0.8, classify as blocked_live_apply.
```

## v0.8 Blocks

```text
no adapter implementation
no runtime loader
no dry-run executor
no apply executor
no repair execution
no runtime mutation
no dependency mutation
no CMS import
no CMS writes
no API write authority
no live apply authority
```

## Non-Claim Lock

HRCN v0.8 is a docs/context apply-gate adapter design layer. It defines the authorization, rollback, validation, evidence, and staged-scope requirements for future apply/write transitions. It does not create a loader, adapter, runtime bridge, dry-run executor, apply executor, CMS folder, memory writer, repair applier, API writer, live integration, or apply authority. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
