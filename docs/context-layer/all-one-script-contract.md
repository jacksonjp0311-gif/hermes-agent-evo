# All-One Script Contract

Every future All-One PowerShell operation must:
1. Anchor to the expected repo root.
2. Verify ENTRYPOINT-GATE: run by file path, not pasted/dot-sourced.
3. Run RESIDUE-MANAGER before cleanup.
4. Verify CURRENT-SCRIPT-GATE: actual script and evidence operator script match.
5. Run AUTOHEAL-PREFLIGHT before pull/rebase.
6. Pull/rebase before authorization.
7. Require an exact human authorization phrase.
8. Apply only bounded mutation.
9. Run focused validation.
10. Write final evidence before current-script gate.
11. Scan staged additions for secret triggers.
12. Use captured command runner for noisy commands.
13. Collapse streams and write raw streams to evidence.
14. Render ERROR-BOX on failures with raw artifact path.
15. Commit, pull-rebase, push, and seal only after gates pass.
16. Return to repo root on every success/failure path.
17. Update README, AGENTS, rhp/README, latest-rhp, and zero-context rebuild surfaces.
