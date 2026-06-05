# CMS-SA v0.4.7 — Authorized Apply Packet Schema and Diff Manifest

v0.4.7 evolves the apply gate into a packet/diff manifest surface.

It does not apply repairs. It defines the human authorization packet boundary, exact diff-entry grammar, and rollback binding requirement.

```text
No apply packet may authorize a repair unless it references a validated apply gate, includes a human authorization artifact, declares exact diff entries for every target write, binds rollback entries one-to-one with diff entries, preserves blocked actions, and passes pre-apply validation.
```

## Starting Threshold

v0.4.7 starts from sealed v0.4.6 stable state:

- pressure: `0.14`
- threshold: `0.25`
- threshold usage: `56%`
- headroom: `44%`
- state: `stable_green_loop`

## Learning Check

v0.4.7 promotes the v0.4.6 lesson that an apply gate is not apply authority. A future repair cannot advance from gate to apply without a packet, exact diff, rollback binding, validation stack, and human authorization artifact.

## Non-Claim Lock

Authorized apply packets and diff manifests are repository-bound authorization evidence and do not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, autonomous repair authority, or real-world correctness.
