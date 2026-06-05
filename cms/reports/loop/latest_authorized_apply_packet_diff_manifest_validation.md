# CMS-SA v0.4.7 Authorized Apply Packet Diff Manifest Validation

- passed: `true`
- errors: `0`
- apply packet count: `1`
- diff manifest count: `1`
- target writes performed: `0`
- api writes performed: `0`
- git commits performed: `0`

## Primary Lock

No apply packet may authorize a repair unless it references a validated apply gate, includes a human authorization artifact, declares exact diff entries for every target write, binds rollback entries one-to-one with diff entries, preserves blocked actions, and passes pre-apply validation.

## Findings

- none

## Non-Claim Lock

Authorized apply packet validation is repository-bound and does not prove code correctness.
