# HRCN v0.4 CMS Read-Only Bridge Design

Status: docs/context design only.

## Primary Law

```text
A CMS bridge may inform Hermes; it may not command Hermes.
```

## Purpose

HRCN v0.4 defines how a future Hermes/CMS bridge may expose CMS context as read-only orientation.

This is a design boundary, not an implementation.

```text
CMS context -> read-only orientation -> proposal classification -> human authorization requirement
```

## What v0.4 Allows

```text
read-only bridge design
interface contract definition
source/provenance requirements
claim-boundary requirements
future gate sequence
```

## What v0.4 Blocks

```text
no runtime implementation
no adapter implementation
no loader
no CMS import
no CMS writes
no memory authority
no API write authority
no repair apply
no dependency mutation
```

## Future Read-Only Inputs

A future bridge may expose these as read-only context only:

```text
validated CMS state summaries
lesson ledgers
claim-boundary notes
repository governance rules
evidence-package references
rollback requirements
human authorization requirements
```

## Interface Contract

A future bridge record must carry:

| Field | Meaning |
|---|---|
| source | Where the context came from. |
| timestamp_utc | When it was emitted or validated. |
| validation_tier | Whether the record is validated, provisional, or narrative. |
| claim_boundary | What the record can and cannot support. |
| allowed_use | How Hermes may use the context. |
| blocked_use | What Hermes must not infer or do. |
| human_authorization_requirement | Whether human approval is required before action. |

## Non-Claim Lock

HRCN v0.4 is a docs/context bridge-design layer. It defines a future CMS read-only bridge boundary. It does not create a loader, adapter, runtime bridge, CMS folder, memory writer, repair applier, API writer, or live integration. It does not modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
