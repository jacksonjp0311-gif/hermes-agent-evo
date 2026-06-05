# OPS-002 Morning Runbook

Morning operating sequence:

1. Set location to the repository root.
2. Confirm git status is clean.
3. Pull/rebase main.
4. Verify HRCN v2.0 validation.
5. Verify OPS-001 and OPS-002 evidence.
6. Run operator status.
7. Run nexus status.
8. Select one bounded docs/context task.
9. Build a limited apply packet.
10. Apply only through the v1.6 limited apply executor.
11. Write loop, replay, nexus, and final evidence.
12. Stage only allowed OPS evidence paths.
13. Run staged secret scan.
14. Commit, pull/rebase, push.
15. Confirm final git status is clean.

Stop conditions:

- dirty worktree before operation
- blocked path appears
- secret marker appears
- v2.0 validation drift
- OPS-001 or OPS-002 evidence missing
- runtime, CMS, memory, API, dependency, self-authorization, or autonomous authority becomes true