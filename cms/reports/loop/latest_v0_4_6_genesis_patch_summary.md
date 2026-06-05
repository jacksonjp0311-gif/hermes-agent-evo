# CMS-SA v0.4.6 Genesis Patch Summary

- passed: `true`
- current version: `v0.4.6`
- previous version: `v0.4.5`
- threshold usage: `56%`
- headroom: `44%`

## Primary Lock

No repair apply may execute unless it references a validated dry-run id, carries explicit human authorization, declares exact target writes, includes rollback entries for every target, preserves blocked actions, and passes the required validation stack before and after apply.

## Non-Claim Lock

Authorized repair apply gates are repository-bound authorization ledgers and do not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, autonomous repair authority, or real-world correctness.
