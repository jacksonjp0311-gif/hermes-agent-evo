# HRCN Roadmap

## Current

HRCN v1.8 - Replay and Rollback Hardening

## Phase Map

| Phase | Name | Boundary |
|---|---|---|
| HRCN v1.0.3 | CMS Read-Only Mirror Copy With Evidence Package | CMS copied under `cms/` as read-only context/evidence only. |
| HRCN v1.1 | Bounded CMS Context Packet | Bounded read-only packet from CMS mirror into Hermes context; no loader or authority. |
| HRCN v1.2 | Permission Bridge Dry-Run Design | Classifies requested authority before action; design only. |
| HRCN v1.3 | CMS-Hermes Read-Only Bridge Prototype | Reference prototype contract; no runtime loader, adapter, or execution authority. |
| HRCN v1.4 | Dry-Run Execution Harness Contract | Simulation contract only; no filesystem, git, runtime, CMS, memory, API, or apply mutation. |
| HRCN v1.5 | Apply-Gate Contract | Defines future apply candidate gate; no apply executor or apply authority. |
| HRCN v1.6 | Limited Apply Executor | Bounded local executor for README.md and docs/context-layer/** only; no self-authorization. |
| HRCN v1.7 | Governed Operational Loop | Coordinates observe/propose/classify/dry-run/evidence/authorize/limited-apply/validate/ledger without bypassing gates. |
| HRCN v1.8 | Replay and Rollback Hardening | Requires replay manifest, audit chain, rollback packet, operation hashes, and validation evidence. |
| HRCN v1.9 | Operator Dashboard / Command Surface | Future human-facing operation panel or packet surface. |
| HRCN v2.0 | Operational Hermes-CMS Nexus | Future operational nexus only after all prior gates validate. |

## Next Anchor

HRCN v1.9 - Operator Dashboard / Command Surface.

## Current Replay/Rollback Boundary

HRCN v1.8 hardens the governed loop with replay and rollback evidence. It does not automatically rollback, self-authorize, widen scope, mutate runtime, write CMS, write memory, call APIs, or change dependencies.

## Non-Claim Lock

HRCN v1.8 adds replay and rollback hardening for the governed docs/context loop. It defines how ledger entries, limited-apply audits, expected base commits, operation hashes, rollback packets, and replay manifests are checked before an operation is trusted. It does not perform automatic rollback, does not self-authorize, does not widen v1.6 scope, does not mutate Hermes runtime, does not touch cms/, does not change dependencies, and does not call APIs.
