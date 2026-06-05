# HRCN v1.3 CMS-Hermes Read-Only Bridge Prototype

- passed: true
- previous validated anchor: HRCN v1.2
- current checkpoint: HRCN v1.3
- next recommended phase: HRCN v1.4 - Dry-Run Execution Harness
- mode: docs/context reference prototype
- runtime code changed: false
- dependency files changed: false
- CMS copy performed: false
- authority granted: false

## Primary Law

```text
A read-only bridge may translate bounded CMS context into Hermes orientation; it may not command Hermes or execute CMS.
```

## Prototype Inputs

```text
docs/context-layer/hrcn-v1.1-bounded-cms-context-packet.json
docs/context-layer/hrcn-v1.2-permission-bridge-dry-run-design.json
cms/MIRROR_READONLY_BOUNDARY.md
cms/.hrcn-read-only-mirror.json
```

## Request Contract

```text
bridge_request_id
proposal_id
requested_operation
requested_surface
requested_authority
cms_read_refs
evidence_refs
human_request_text
```

## Response Contract

```text
bridge_request_id
decision_class
resolved_read_refs
unresolved_read_refs
evidence_summary
blocked_actions
authority_granted: false
dry_run_executed: false
apply_executed: false
cms_executed: false
runtime_mutated: false
```

## Prototype Algorithm

```text
load HRCN v1.1 bounded CMS context packet
load HRCN v1.2 permission bridge design
reject authority outside none/read_context/summarize/classify
reject CMS refs outside v1.1 bounded_read_set
reject cms/src, cms/scripts, cms/tests, dependency, secret, and runtime roots
map request to observe_only/read_only_context/summarize_evidence/blocked
return response with authority_granted=false
```

## Non-Claim Lock

HRCN v1.3 defines a CMS-Hermes Read-Only Bridge Prototype as a documentation/context reference contract only. The prototype may describe how Hermes reads the bounded CMS context packet and permission bridge design, resolves allowed read references, and emits an orientation response with authority_granted=false. It does not wire CMS into Hermes runtime, does not create a runtime loader, adapter, writer, dry-run executor, apply executor, benchmark executor, repair executor, API writer, live integration, or apply authority. Bridge prototype presence is not bridge execution authority.
