# CMS-SA v0.4.7 Genesis Patch Summary

- passed: `true`
- current version: `v0.4.7`
- previous version: `v0.4.6`
- threshold usage: `56%`
- headroom: `44%`

## Learning Repairs

- added v0.4.6 lessons to root README
- advanced stale API inactive tokens to v0.4.7
- advanced RCC-N echo location version to v0.4.7
- corrected alignment layer count to 13
- added apply packet diff manifest validation surfaces

## Primary Lock

No apply packet may authorize a repair unless it references a validated apply gate, includes a human authorization artifact, declares exact diff entries for every target write, binds rollback entries one-to-one with diff entries, preserves blocked actions, and passes pre-apply validation.

## Non-Claim Lock

Authorized apply packets and diff manifests are repository-bound authorization evidence and do not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, autonomous repair authority, or real-world correctness.
