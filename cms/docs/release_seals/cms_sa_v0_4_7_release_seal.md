# CMS-SA v0.4.7 Release Seal Draft

Status: preseal development.

Current checkpoint: CMS-SA v0.4.7 - Authorized Apply Packet Schema and Diff Manifest
Previous seal: CMS-SA v0.4.6 - Authorized Repair Apply Gate and Rollback Ledger

## Primary Lock

No apply packet may authorize a repair unless it references a validated apply gate, includes a human authorization artifact, declares exact diff entries for every target write, binds rollback entries one-to-one with diff entries, preserves blocked actions, and passes pre-apply validation.

## Non-Claim Lock

Authorized apply packets and diff manifests are repository-bound authorization evidence and do not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, autonomous repair authority, or real-world correctness.
