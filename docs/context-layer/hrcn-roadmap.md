# HRCN Roadmap

## Current

HRCN v2.0 - Operational Hermes-CMS Nexus

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
| HRCN v1.9 | Operator Dashboard / Command Surface | Human-facing command surface; no apply, rollback, API, or self-authorization. |
| HRCN v2.0 | Operational Hermes-CMS Nexus | Bounded docs/context governance is operational and human-gated; runtime/CMS/API/dependency writes remain blocked. |
| HRCN v2.1 | Runtime Adapter Readiness Boundary | Future boundary for simulated runtime adapter readiness; no runtime mutation by default. |

## Next Anchor

HRCN v2.1 - Runtime Adapter Readiness Boundary.

## Current Operational Boundary

HRCN v2.0 is operational for bounded docs/context governance only. Human authorization remains required. Hermes runtime, `cms/`, dependency files, memory write surfaces, and external APIs remain blocked.

## Non-Claim Lock

HRCN v2.0 seals Hermes-CMS as operational only for bounded docs/context governance. The operational nexus can report status across the CMS mirror/context packet, permission bridge, read-only bridge, dry-run contract, apply gate, limited apply executor, governed loop, replay/rollback hardening, and operator surface. It does not grant runtime mutation, CMS write authority, memory write authority, API authority, dependency mutation, autonomous authority, or self-authorization.
