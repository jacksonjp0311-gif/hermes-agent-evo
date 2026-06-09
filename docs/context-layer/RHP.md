# RHP v0.1 — Repository / Runtime Rehydration Protocol

Status: diagnostic-only.

RHP is a proposed rehydration protocol for verifying repository state, runtime posture, and authority boundaries before continuing work after context loss.

## Current Repository State

- Repository: Hermes Agent
- Version: 0.12.0
- Last verified rehydration baseline: `bfece1356`
- Terminal stdout capture repair commit: `f959d9e43`
- Previous clean anchor: `349d0da07`
- `rhp_runtime_bridge.py`: absent
- Runtime wiring: absent

## Scope

RHP v0.1 is limited to:

- repository identity verification
- branch and commit verification
- working tree cleanliness checks
- runtime/tool access checks
- RHP/HRCN surface classification
- drift/risk reporting
- authority boundary declaration

## Non-Goals

RHP v0.1 does not:

- execute automatically
- mutate files
- alter Hermes runtime behavior
- add imports
- add CLI commands
- add gateway commands
- write memory
- call external APIs
- grant autonomous authority

## Classification Vocabulary

RHP/HRCN surfaces may be classified as:

- absent
- partial/stale
- present but inactive
- present and wired
- unknown

## Authority Boundary

Runtime source authority: read-only until authorized  
RHP authority: diagnostic only  
CMS write authority: false  
Memory promotion authority: false  
External ingestion authority: false  
Autonomous authority: false  
Human authorization required: true

## Future Runtime Bridge Criteria

A runtime bridge must not be added unless:

- a human-approved design exists
- a concrete runtime problem is documented
- docs-only operation is insufficient
- integration points are identified
- failure modes are documented
- tests are planned
- default behavior remains unchanged
- write authority remains false by default
