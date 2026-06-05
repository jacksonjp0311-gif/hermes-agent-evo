
# CMS-SA v0.3b4 - Negative Control and Downgrade Harness

v0.3b4 adds a repository-bound negative control and downgrade harness.

It tests whether CMS can reject false promote states, preserve downgrade cases, keep incomplete evidence in observe-only status, and prevent future memory promotion from becoming success-only narrative accumulation.

Core rule:

```text
A system is not promoted because it passes happy-path validators.
It is promoted only if negative controls fail correctly, downgrade paths are preserved,
and false promote states are rejected.
```

Decision lifecycle:

```text
feedback item
-> positive case
-> negative control
-> downgrade path
-> falsification condition
-> decision kernel
-> promote/block/downgrade/observe_only
-> replay ledger
```

Non-claim lock: v0.3b4 improves repository-bound control discipline. It does not prove code correctness, truth, AGI, consciousness, production readiness, security, external validation, or real-world correctness.
