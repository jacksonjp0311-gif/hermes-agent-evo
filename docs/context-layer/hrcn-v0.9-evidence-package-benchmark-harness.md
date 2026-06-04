# HRCN v0.9 Evidence Package and Benchmark Harness

Status: docs/context design only.

## Primary Law

```text
No claim or action graduates without an evidence package.
```

## Purpose

HRCN v0.9 defines the evidence package and benchmark harness required before future governed Hermes-CMS nexus work or CMS import work.

```text
claim/action -> evidence package -> benchmark contract -> audit record -> rollback binding -> authorization record -> promotion decision
```

## Geometry

| Layer | Meaning |
|---|---|
| claim or action | What is being asserted or requested. |
| evidence package | Artifact bundle supporting the claim/action. |
| benchmark contract | Repeatable check suite required for evaluation. |
| audit record | Immutable summary of what was checked. |
| rollback binding | How reversal is tied to the evidence package. |
| authorization record | Human authorization if a dangerous transition is requested. |
| promotion decision | Whether the claim/action may advance to future nexus work. |

## Evidence Package Classes

| Class | Meaning |
|---|---|
| insufficient | Evidence package is missing or incomplete. |
| documentation_evidence | Docs/context evidence only. |
| dry_run_evidence | Simulation evidence only; no live mutation proof. |
| apply_gate_evidence | Evidence required before future apply-gate consideration. |
| cms_import_evidence | Evidence required before any future CMS folder copy or read-only mirror. |
| runtime_evidence_candidate | Evidence candidate for future runtime nexus work; blocked from execution in v0.9. |
| blocked_live_authority | Any evidence package attempting to grant live authority is blocked. |

## CMS Import Evidence Gate

CMS is near, but not copied in v0.9.

A future CMS copy requires:

```text
source repository or local source path
import method decision
provenance record
file manifest
license/provenance note
secret scan
read-only boundary statement
blocked-authority statement
rollback/removal plan
post-import validation commands
human authorization
```

Initial future mode:

```text
read_only_mirror_candidate
```

Disallowed initial modes:

```text
runtime_integration
CMS write authority
API authority
memory authority
repair apply authority
autonomous authority
```

## Benchmark Harness Requirements

```text
must be repeatable
must declare inputs and outputs
must separate expected outputs from actual outputs
must include path-boundary checks
must include secret-scan result before any future commit or import
must include rollback or cleanup requirements
must record failure as evidence, not hide it
must classify synthetic evidence separately from runtime validation
must not claim production/security/external validation from docs-only checks
```

## v0.9 Blocks

```text
no adapter implementation
no runtime loader
no dry-run executor
no apply executor
no benchmark executor
no repair execution
no CMS copy
no runtime mutation
no dependency mutation
no CMS writes
no API write authority
no live apply authority
```

## Non-Claim Lock

HRCN v0.9 is a docs/context evidence package and benchmark harness design layer. It defines evidence artifacts, benchmark boundaries, audit requirements, and CMS import evidence gates for future nexus work. It does not create a loader, adapter, runtime bridge, dry-run executor, apply executor, benchmark executor, CMS folder, memory writer, repair applier, API writer, live integration, or apply authority. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
