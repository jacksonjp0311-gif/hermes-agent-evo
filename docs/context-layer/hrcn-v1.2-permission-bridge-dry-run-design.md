# HRCN v1.2 Permission Bridge Dry-Run Design

- passed: true
- previous validated anchor: HRCN v1.1.2
- current checkpoint: HRCN v1.2
- next recommended phase: HRCN v1.3 - CMS-Hermes Read-Only Bridge Prototype
- mode: design only
- runtime code changed: false
- dependency files changed: false
- CMS copy performed: false
- authority granted: false

## Primary Law

```text
Permission bridge design classifies requested authority before action; it does not execute CMS, run dry-runs, apply repairs, or grant authority.
```

## Proposal Fields

```text
proposal_id
proposal_type
requested_surface
requested_authority
target_paths
cms_read_refs
evidence_refs
human_request_text
non_claim_lock
```

## Decision Classes

```text
observe_only
read_only_context
summarize_evidence
dry_run_required
human_review_required
blocked
```

## Required Classification Outputs

```text
decision_class
evidence_required
dry_run_required
rollback_required
human_authorization_required
blocked_actions
allowed_next_phase
reason
authority_granted: false
```

## Blocked Actions

```text
import cms/src as Hermes runtime
execute cms/scripts
treat CMS outputs as permission grants
write CMS memory
write external APIs
apply repairs
create runtime adapters
create runtime loaders
mutate dependencies
commit local secrets or machine state
```

## Non-Claim Lock

HRCN v1.2 defines the Permission Bridge Dry-Run Design as a machine-readable contract for proposal classification, authority requests, evidence requirements, dry-run requirements, rollback requirements, and human authorization requirements. It does not wire CMS into Hermes runtime, does not create a loader, adapter, writer, dry-run executor, apply executor, benchmark executor, repair executor, API writer, live integration, or apply authority. Design presence is not execution authority.
