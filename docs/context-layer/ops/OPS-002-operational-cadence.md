# OPS-002 Operational Cadence

- operation: OPS-002
- base commit: 75b85118410ce5cac7d82068d014902bd1b73510
- timestamp utc: 20260605T121458Z
- purpose: convert OPS-001 proof into repeatable morning operation
- HRCN version: v2.0 sealed baseline
- version churn: false
- runtime mutation: false
- cms write: false
- memory write: false
- api write: false
- dependency mutation: false

## Cadence

1. Confirm clean worktree.
2. Pull/rebase latest main.
3. Verify HRCN v2.0 validation.
4. Verify OPS-001 evidence.
5. Run operator status.
6. Run nexus status.
7. Choose one bounded docs/context task.
8. Build packet.
9. Apply only through governed limited apply.
10. Write evidence, replay/rollback report, and final OPS record.

## Rule

Versions define authority. OPS runs prove capability. Patches repair tooling. Releases showcase stable milestones.
