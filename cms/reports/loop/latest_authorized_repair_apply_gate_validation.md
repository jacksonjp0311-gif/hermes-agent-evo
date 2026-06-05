# CMS-SA v0.4.6 Authorized Repair Apply Gate Validation

- passed: `true`
- errors: `0`
- apply gate count: `1`
- rollback ledger count: `1`
- target writes performed: `0`
- api writes performed: `0`
- git commits performed: `0`

## Primary Lock

No repair apply may execute unless it references a validated dry-run id, carries explicit human authorization, declares exact target writes, includes rollback entries for every target, preserves blocked actions, and passes the required validation stack before and after apply.

## Findings

- none

## Non-Claim Lock

Authorized apply gate validation is repository-bound and does not prove code correctness.
