# RHP-013 RuntimeBootState v0.1 Plan

## Purpose

RuntimeBootState will become the single typed state object for RHP boot truth.

```text
one verified runtime boot state
-> operator startup status
-> compact CLI protocol strip
-> startup packet truth
-> prompt boot context
-> tests / smoke checks
```

## Planned Home

```text
rhp/startup_context_packet.py
```

## Planned Schema

```text
RHP-RUNTIME-BOOT-STATE-v0.1
```

## Planned Fields

- ok
- schema
- evidence
- repo_root
- phase
- status
- degraded
- degraded_reason
- entrypoint
- interface
- profile
- session_id
- boot_preflight_packet_schema
- startup_context_packet_schema
- locks
- authority
- operator_status_text
- protocol_strip
- protocol_locks
- prompt_context_json
- env
- non_claim_lock

## Implementation Boundary

RHP-013.1 may add a typed dataclass and direct tests. It must not grant authority or change provider/model/tool, CMS/memory/API, external ingestion, or autonomy behavior.
