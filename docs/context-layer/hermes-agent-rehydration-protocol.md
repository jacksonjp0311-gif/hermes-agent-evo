# Hermes Agent Rehydration Protocol — HRCN v0.1.3

Status: docs/context/navigation protocol only.

## Purpose

A fresh human or AI agent thread must recover repository identity, runtime boundaries, current HRCN state, target-folder role, and authorization class before proposing changes.

This protocol prevents version-eager or runtime-eager changes before orientation.

## Core Rule

```text
No fresh-thread Hermes work may propose runtime, tool, skill, provider, gateway, memory, or apply/write changes until it completes identity, boundary, state, target, and authority scans.
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
- `docs/context-layer/hrcn-roadmap.md`
- target folder `README.md`

Recover:

- allowed phase boundary
- blocked runtime surfaces
- mini README profile
- whether the task is docs-only, read-only, dry-run, or apply/write

### 3. State Scan

Read:

- `docs/context-layer/rcc-cms-hrcn.validation.json`
- `docs/context-layer/rcc-cms-hrcn.lesson-injection.validation.json`
- `docs/context-layer/hrcn-v0.1.3.validation.json`
- `git status --short`

Recover:

- latest checkpoint
- current local dirty state
- excluded artifacts
- validation state
- next anchor

### 4. Target Scan

Read:

- target folder `README.md`
- relevant source files
- relevant tests
- relevant docs

Recover:

- target role
- inbound/outbound hooks
- local claim boundary
- required validation

### 5. Authority Scan

Classify requested work:

| Class | Meaning | HRCN v0.1.3 authority |
|---|---|---|
| `docs_only` | README/context/navigation edits | allowed |
| `read_only_context` | inspect/map/describe surfaces | allowed |
| `dry_run` | simulate a proposed action | future phase |
| `apply_write` | mutate runtime/dependency/bridge behavior | blocked |

## Version-Readiness Lock

```text
No HRCN version step may advance unless README checkpoint, roadmap, context layer,
profile map, rehydration protocol, mini README profiles, validation report,
and non-claim locks agree.
```

## Non-Claim Lock

HRCN v0.1.3 is a docs/context/navigation coherence and compression layer. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
