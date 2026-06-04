# HRCN v0.3 Agent Rehydration Packet Contract

Status: docs/context contract only.

## Primary Law

```text
A rehydration packet orients an agent; it does not authorize an agent.
```

## Purpose

HRCN v0.3 defines the exact packet a future Hermes/CMS-aware agent must load before proposing work.

This is a contract, not a loader.

```text
packet -> orientation -> classification -> proposal boundary -> human authorization requirement
```

## Required Packet Fields

The machine-readable contract lists the full required packet field set, authority classes, required scans, blocked actions, and runtime mutation gate.

Primary artifact:

```text
docs/context-layer/hrcn-v0.3-agent-rehydration-packet-contract.json
```

## Authority Classes

| Class | Current v0.3 status | Meaning |
|---|---|---|
| docs_only | allowed when validation passes | README/context/navigation edits. |
| read_only_context | allowed | Inspect, map, summarize, or classify surfaces. |
| dry_run | future phase | Simulate proposed actions without applying them. |
| apply_write | blocked | Runtime/dependency/bridge/tool/provider/UI/CMS mutation. |
| cms_intake | future phase | Add, mirror, or activate CMS surfaces. |

## v0.3 Blocked Actions

```text
no runtime loader
no runtime mutation
no dependency mutation
no CMS import
no API write authority
no CMS write authority
no repair apply
no security or production claim
no autonomy, consciousness, sentience, AGI, or ASI claim
```

## Non-Claim Lock

HRCN v0.3 is a docs/context packet-contract layer. It defines the packet a future agent must load before proposing work. It does not create a loader, modify Hermes runtime behavior, prompts, tools, skills, plugins, providers, gateways, TUI, web runtime, package dependencies, memory authority, API write authority, CMS write authority, CMS folder state, security posture, production readiness, autonomy, consciousness, sentience, AGI/ASI status, or external validation.
