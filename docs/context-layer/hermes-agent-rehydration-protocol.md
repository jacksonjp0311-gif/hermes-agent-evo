# Hermes Agent Rehydration Protocol - Current through HRCN v2.0

Status: docs/context/navigation protocol only.
Current HRCN state: HRCN v2.0.
Next anchor: HRCN v2.1 - Runtime Adapter Readiness Boundary.

## Purpose

A fresh human or AI agent thread must recover repository identity, runtime boundaries, current HRCN state, target-folder role, and authorization class before proposing changes.

This protocol prevents version-eager, runtime-eager, or CMS-eager changes before orientation.

## Core Rule

```text
No fresh-thread Hermes work may propose runtime, tool, skill, provider,
gateway, memory, CMS, dependency, or apply/write changes until it completes
identity, boundary, state, target, and authority scans.
```

## Rehydration Scans

### 1. Identity Scan

Read:

- `README.md`
- `AGENTS.md`
- `docs/context-layer/rcc-cms-hrcn.md`

Recover:

- Hermes actor/runtime identity.
- RCC repository-orientation role.
- CMS governed permission role.
- HRCN bridge-contract role.
- Human write-authorization boundary.

### 2. Boundary Scan

Read:

- `docs/context-layer/hrcn-profile-map.json`
- `docs/context-layer/hermes-surface-boundary-map.json`
- `docs/context-layer/hermes-surface-boundary-map.md`
- `docs/context-layer/hrcn-roadmap.md`
- target folder `README.md`

Recover:

- current checkpoint
- current phase boundary
- mapped surface class
- blocked runtime/dependency/CMS surfaces
- mini README profile source
- whether the task is docs-only, read-only, dry-run, or apply/write

### 3. State Scan

Read:

- `docs/context-layer/rcc-cms-hrcn.validation.json`
- `docs/context-layer/rcc-cms-hrcn.lesson-injection.validation.json`
- `docs/context-layer/hrcn-v0.1.3.validation.json`
- `docs/context-layer/hrcn-v0.1.4.validation.json`
- `docs/context-layer/hrcn-v0.2.validation.json`
- `docs/context-layer/hrcn-v0.2.4.public-surface-coherence.validation.json`
- `docs/context-layer/hrcn-v0.3-agent-rehydration-packet-contract.json`
- `docs/context-layer/hrcn-v0.3.validation.json`
- `docs/context-layer/hrcn-v0.4-cms-read-only-bridge-design.json`
- `docs/context-layer/hrcn-v0.4.validation.json`
- `docs/context-layer/hrcn-v0.5-memory-permission-adapter-design.json`
- `docs/context-layer/hrcn-v0.5.validation.json`
- `docs/context-layer/hrcn-v0.6-repair-recommendation-adapter-design.json`
- `docs/context-layer/hrcn-v0.6.validation.json`
- `docs/context-layer/hrcn-v0.7-dry-run-adapter-design.json`
- `docs/context-layer/hrcn-v0.7.validation.json`
- `docs/context-layer/hrcn-v0.8-apply-gate-adapter-design.json`
- `docs/context-layer/hrcn-v0.8.validation.json`
- `docs/context-layer/hrcn-v0.9-evidence-package-benchmark-harness.json`
- `docs/context-layer/hrcn-v0.9.validation.json`
- `docs/context-layer/hrcn-v1.0-governed-hermes-cms-nexus-plan.json`
- `docs/context-layer/hrcn-v1.1.2-context-surface-coherence-closure.json`
- `docs/context-layer/hrcn-v1.1.2.validation.json`
- `docs/context-layer/hrcn-v1.2-permission-bridge-dry-run-design.json`
- `docs/context-layer/hrcn-v1.2.validation.json`
- `docs/context-layer/hrcn-v1.3-cms-hermes-read-only-bridge-prototype.json`
- `docs/context-layer/hrcn-v1.3.validation.json`
- `docs/context-layer/hrcn-v1.4-dry-run-execution-harness-contract.json`
- `docs/context-layer/hrcn-v1.4.validation.json`
- `docs/context-layer/hrcn-v1.5-apply-gate-contract.json`
- `docs/context-layer/hrcn-v1.5.validation.json`
- `docs/context-layer/hrcn-v1.6-limited-apply-executor.json`
- `docs/context-layer/hrcn-v1.6.validation.json`
- `docs/context-layer/hrcn-v1.7-governed-operational-loop.json`
- `docs/context-layer/hrcn-v1.7.validation.json`
- `docs/context-layer/hrcn-v1.8-replay-rollback-hardening.json`
- `docs/context-layer/hrcn-v1.8.validation.json`
- `docs/context-layer/hrcn-v1.9-operator-dashboard-command-surface.json`
- `docs/context-layer/hrcn-v1.9.validation.json`
- `docs/context-layer/hrcn-v2.0-operational-hermes-cms-nexus.json`
- `docs/context-layer/hrcn-v2.0.validation.json`
- `scripts/hrcn/operational_nexus_status_v2_0.py`
- `scripts/hrcn/operator_command_surface_v1_9.py`
- `scripts/hrcn/replay_rollback_hardening_v1_8.py`
- `scripts/hrcn/governed_operational_loop_v1_7.py`
- `scripts/hrcn/limited_apply_executor_v1_6.py`
- `docs/context-layer/hrcn-v1.0.validation.json`
- `docs/context-layer/hrcn-v1.0.1-cms-read-only-mirror-import-authorization-path.json`
- `docs/context-layer/hrcn-v1.0.1.validation.json`
- `git status --short`

Recover:

- latest checkpoint
- current local dirty state
- excluded artifacts
- validation state
- next anchor
- whether public surfaces agree

### 4. Target Scan

Read:

- target folder `README.md`
- relevant source files
- relevant tests
- relevant docs
- applicable surface entry in `docs/context-layer/hermes-surface-boundary-map.json`

Recover:

- target role
- inbound/outbound hooks
- local claim boundary
- mapped authority class
- required validation

### 5. Authority Scan

Classify requested work:

| Class | Meaning | Current HRCN authority |
|---|---|---|
| `docs_only` | README/context/navigation edits | allowed when validation passes |
| `read_only_context` | inspect/map/describe surfaces | allowed |
| `dry_run` | simulate a proposed action | future phase |
| `apply_write` | mutate runtime/dependency/bridge behavior | blocked |
| `cms_intake` | add or activate CMS root/bridge surfaces | future phase |

### 6. Packet Contract Scan

Read:

- `docs/context-layer/hrcn-v0.3-agent-rehydration-packet-contract.json`
- `docs/context-layer/hrcn-v0.3-agent-rehydration-packet-contract.md`

Recover:

- packet required fields
- authority class vocabulary
- blocked actions
- runtime mutation gate
- human authorization requirement
- non-claim lock

Core rule:

```text
A rehydration packet orients an agent; it does not authorize an agent.
```

### 7. CMS Read-Only Bridge Design Scan

Read:

- `docs/context-layer/hrcn-v0.4-cms-read-only-bridge-design.json`
- `docs/context-layer/hrcn-v0.4-cms-read-only-bridge-design.md`

Recover:

- CMS read-only input contract
- provenance requirements
- blocked CMS write behaviors
- bridge authority class
- human authorization boundary

Core rule:

```text
A CMS bridge may inform Hermes; it may not command Hermes.
```

### 8. Memory Permission Adapter Design Scan

Read:

- `docs/context-layer/hrcn-v0.5-memory-permission-adapter-design.json`
- `docs/context-layer/hrcn-v0.5-memory-permission-adapter-design.md`

Recover:

- permission classes
- required memory record fields
- decision rules
- blocked memory behaviors
- human authorization boundary

Core rule:

```text
Memory may surface context; permission determines use; humans authorize action.
```

### 9. Repair Recommendation Adapter Design Scan

Read:

- `docs/context-layer/hrcn-v0.6-repair-recommendation-adapter-design.json`
- `docs/context-layer/hrcn-v0.6-repair-recommendation-adapter-design.md`

Recover:

- recommendation classes
- required recommendation fields
- decision rules
- blocked repair behaviors
- dry-run and apply-gate boundaries
- human authorization boundary

Core rule:

```text
A repair recommendation may describe a path; it may not apply the path.
```

### 10. Dry-Run Adapter Design Scan

Read:

- `docs/context-layer/hrcn-v0.7-dry-run-adapter-design.json`
- `docs/context-layer/hrcn-v0.7-dry-run-adapter-design.md`

Recover:

- dry-run classes
- required dry-run fields
- sandbox boundary requirements
- expected diff and evidence package requirements
- rollback plan requirements
- blocked apply/write behaviors
- human authorization boundary

Core rule:

```text
A dry-run may simulate a change; it may not become the change.
```

### 11. Apply-Gate Adapter Design Scan

Read:

- `docs/context-layer/hrcn-v0.8-apply-gate-adapter-design.json`
- `docs/context-layer/hrcn-v0.8-apply-gate-adapter-design.md`

Recover:

- apply-gate classes
- required apply-gate fields
- human authorization requirements
- rollback plan requirements
- validation plan requirements
- evidence package requirements
- staged-scope requirements
- blocked live-apply behaviors

Core rule:

```text
Apply is a gated transition, not an agent decision.
```

### 12. Evidence Package and Benchmark Harness Scan

Read:

- `docs/context-layer/hrcn-v0.9-evidence-package-benchmark-harness.json`
- `docs/context-layer/hrcn-v0.9-evidence-package-benchmark-harness.md`

Recover:

- evidence package classes
- required evidence package fields
- benchmark harness requirements
- CMS import evidence gate
- provenance and manifest requirements
- secret scan requirement
- rollback/removal requirements
- human authorization boundary

Core rule:

```text
No claim or action graduates without an evidence package.
```

### 13. Governed Hermes-CMS Nexus Planning Scan

Read:

- `docs/context-layer/hrcn-v1.0-governed-hermes-cms-nexus-plan.json`
- `docs/context-layer/hrcn-v1.0-governed-hermes-cms-nexus-plan.md`

Recover:

- core H/R/C/N/E/U relation
- nexus modes
- current allowed planning-only mode
- blocked live-authority modes
- CMS read-only mirror authorization path
- future required CMS import evidence
- human authorization boundary

Core rule:

```text
The nexus may coordinate; it may not self-authorize.
```

### 14. CMS Read-Only Mirror Authorization Path Scan

Read:

- `docs/context-layer/hrcn-v1.0.1-cms-read-only-mirror-import-authorization-path.json`
- `docs/context-layer/hrcn-v1.0.1-cms-read-only-mirror-import-authorization-path.md`

Recover:

- CMS source candidates
- required authorization fields
- allowed future import methods
- disallowed initial authorities
- pre-copy gate sequence
- future post-import gate sequence
- explicit human authorization boundary

Core rule:

```text
CMS may be mirrored only as evidence-bounded read-only context, never as immediate authority.
```

### 15. CMS Read-Only Mirror Scan

Read:

- `cms/MIRROR_READONLY_BOUNDARY.md`
- `cms/.hrcn-read-only-mirror.json`
- `docs/context-layer/hrcn-v1.0.2-cms-mirror-preflight-manifest.json`
- `docs/context-layer/hrcn-v1.0.3-cms-read-only-mirror-copy-evidence.json`

Recover:

- CMS mirror source provenance
- pre-copy manifest
- secret scan result
- read-only mirror boundary
- rollback/removal command
- blocked authority list
- next bounded context packet path

Core rule:

```text
A CMS mirror is readable evidence, not executable authority.
```

### 16. Bounded CMS Context Packet Scan

Read:

- `docs/context-layer/hrcn-v1.1-bounded-cms-context-packet.json`
- `docs/context-layer/hrcn-v1.1-bounded-cms-context-packet.md`
- `docs/context-layer/hrcn-v1.1.validation.json`

Recover:

- bounded CMS read set
- blocked runtime roots
- blocked authority table
- packet use rules
- next permission bridge design target

Core rule:

```text
A bounded CMS context packet orients Hermes; it does not authorize Hermes.
```

### 17. Python Format Technique Scan

Read:

- `docs/context-layer/hrcn-v1.1.1-python-format-technique-lock.json`
- `docs/context-layer/hrcn-v1.1.1.validation.json`

Recover:

- canonical all-one script shape
- PowerShell/Python role split
- Base64 transport-only rule
- validation-before-write rule

Core rule:

```text
PowerShell orchestrates; Python computes, writes, and validates; Base64 is transport only, not canonical source style.
```

### 18. Context Surface Coherence Scan

Read:

- `docs/context-layer/hrcn-v1.1.2-context-surface-coherence-closure.json`
- `docs/context-layer/hrcn-v1.1.2.validation.json`
- `docs/context-layer/README.md`
- `docs/context-layer/hrcn-roadmap.md`

Recover:

- current context-layer boundary
- current rehydration title/current-state line
- current validation path
- next permission bridge design target

Core rule:

```text
Context surfaces must agree on the current HRCN state before permission bridge design begins.
```

### 19. Permission Bridge Design Scan

Read:

- `docs/context-layer/hrcn-v1.2-permission-bridge-dry-run-design.json`
- `docs/context-layer/hrcn-v1.2.validation.json`

Recover:

- proposal contract fields
- requested-surface classes
- requested-authority classes
- decision classes
- evidence, rollback, dry-run, and human-authorization flags
- blocked action list

Core rule:

```text
Permission bridge design classifies requested authority before action; it does not execute CMS, run dry-runs, apply repairs, or grant authority.
```

### 20. Read-Only Bridge Prototype Scan

Read:

- `docs/context-layer/hrcn-v1.3-cms-hermes-read-only-bridge-prototype.json`
- `docs/context-layer/hrcn-v1.3.validation.json`

Recover:

- bridge request contract
- bridge response contract
- allowed read-only operations
- bounded CMS read-ref resolution rule
- authority_granted=false invariant
- blocked runtime/CMS execution list

Core rule:

```text
A read-only bridge may translate bounded CMS context into Hermes orientation; it may not command Hermes or execute CMS.
```

### 21. Dry-Run Harness Contract Scan

Read:

- `docs/context-layer/hrcn-v1.4-dry-run-execution-harness-contract.json`
- `docs/context-layer/hrcn-v1.4.validation.json`

Recover:

- dry-run request contract
- sandbox plan contract
- expected diff manifest contract
- dry-run result contract
- applied=false invariant
- no filesystem/git mutation boundary
- evidence, rollback, and human authorization requirements

Core rule:

```text
A dry-run harness may simulate and score a proposed change; it may not apply the change, mutate runtime, or grant authority.
```

### 22. Apply-Gate Contract Scan

Read:

- `docs/context-layer/hrcn-v1.5-apply-gate-contract.json`
- `docs/context-layer/hrcn-v1.5.validation.json`

Recover:

- apply candidate contract
- apply gate decision contract
- required gate checks
- scope rules
- human authorization requirement
- rollback and validation requirements
- authority_granted=false invariant

Core rule:

```text
Apply is a gated human-authorized transition, not an agent decision and not a dry-run result.
```

## Version-Readiness Lock

```text
No HRCN version step may advance unless README checkpoint, roadmap,
context layer, profile map, surface boundary map, rehydration protocol,
mini README profiles, validation report, and non-claim locks agree.
```

## Script-Run Lock

```text
Every script must verify location/root and clean status before writer logic.
Every writer must validate candidate content before writing files.
If a writer or validator fails, staging, commit, and push are forbidden.
```

## Non-Claim Lock

HRCN v2.0 seals Hermes-CMS as operational only for bounded docs/context governance. The operational nexus can report status across the CMS mirror/context packet, permission bridge, read-only bridge, dry-run contract, apply gate, limited apply executor, governed loop, replay/rollback hardening, and operator surface. It does not grant runtime mutation, CMS write authority, memory write authority, API authority, dependency mutation, autonomous authority, or self-authorization.
