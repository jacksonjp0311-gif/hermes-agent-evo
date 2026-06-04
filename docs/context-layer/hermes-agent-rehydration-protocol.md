# Hermes Agent Rehydration Protocol — HRCN v0.5

Status: docs/context/navigation protocol only.

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

HRCN v0.5 is a docs/context memory-permission adapter design layer. It defines permission classes and gates for future memory use. It does not create a loader, adapter, runtime bridge, CMS folder, memory writer, repair applier, API writer, or live integration. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
