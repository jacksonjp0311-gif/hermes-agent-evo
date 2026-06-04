# HRCN v0.6 Repair Recommendation Adapter Design

Status: docs/context design only.

## Primary Law

```text
A repair recommendation may describe a path; it may not apply the path.
```

## Purpose

HRCN v0.6 defines how future memory/CMS/context may produce bounded repair recommendations without applying changes.

This is a recommendation boundary, not an implementation.

```text
observation -> diagnosis -> recommendation -> dry-run candidate -> apply-gate candidate -> human authorization
```

## Geometry

| Layer | Meaning |
|---|---|
| observation | What failed or drifted. |
| diagnosis | Why it likely failed, with uncertainty. |
| recommendation | What could be changed. |
| dry-run candidate | What may be simulated in a future phase. |
| apply candidate | What remains blocked until apply-gate exists. |
| authorization | The human-controlled transition boundary. |

## Recommendation Classes

| Class | Meaning |
|---|---|
| none | No recommendation should be made. |
| observe_only | Describe condition without proposing repair. |
| diagnostic | Describe probable cause and evidence boundary. |
| documentation_repair | Recommend docs/context update only. |
| test_recommendation | Recommend tests or validation commands without runtime edits. |
| dry_run_recommendation | Recommend future dry-run simulation only. |
| apply_gate_candidate | Recommend future apply-gate review only. |
| blocked_runtime_repair | Runtime/dependency/CMS/API repair is out of phase and must not be applied. |

## Required Recommendation Fields

```text
source
timestamp_utc
observed_condition
diagnosis
recommendation_class
target_surface
authority_class
evidence_boundary
risk_level
allowed_output
blocked_output
required_validation
rollback_requirement
human_authorization_requirement
```

## Decision Rules

```text
No recommendation can apply itself.
No recommendation can stage, commit, push, or mutate files.
No recommendation can upgrade to dry-run without future dry-run phase authorization.
No recommendation can upgrade to apply/write without apply-gate authorization.
Runtime, dependency, CMS, API, secret, and package changes are blocked in v0.6.
Every recommendation must include evidence boundary, validation requirement, and rollback requirement.
If evidence is missing, classify as diagnostic or observe_only.
```

## v0.6 Blocks

```text
no adapter implementation
no runtime loader
no repair execution
no dry-run executor
no runtime mutation
no dependency mutation
no CMS import
no CMS writes
no API write authority
no apply authority
```

## Non-Claim Lock

HRCN v0.6 is a docs/context repair-recommendation adapter design layer. It defines recommendation classes and gates for future repair advice. It does not create a loader, adapter, runtime bridge, CMS folder, memory writer, repair applier, API writer, dry-run executor, or live integration. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
